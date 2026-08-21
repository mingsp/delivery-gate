#!/usr/bin/env python3
"""Score frozen no-negative-echo outputs against a separate evaluation oracle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Literal


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = REPOSITORY_ROOT / "no-negative-echo" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from check_surface import normalize  # noqa: E402


def load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number}: record must be an object")
        case_id = record.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{path}:{line_number}: missing string id")
        if case_id in records:
            raise ValueError(f"{path}:{line_number}: duplicate id {case_id}")
        records[case_id] = record
    return records


def load_outputs(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number}: record must be an object")
        case_id = record.get("id")
        run_id = record.get("run_id", "1")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{path}:{line_number}: missing string id")
        if not isinstance(run_id, str) or not run_id:
            raise ValueError(f"{path}:{line_number}: run_id must be a non-empty string")
        key = (run_id, case_id)
        if key in records:
            raise ValueError(
                f"{path}:{line_number}: duplicate run_id/id pair {run_id}/{case_id}"
            )
        records[key] = record
    return records


def load_expected_run_ids(path: Path) -> list[str]:
    run_ids: list[str] = []
    seen: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        run_id = line.strip()
        if not run_id:
            continue
        if run_id in seen:
            raise ValueError(f"{path}:{line_number}: duplicate run id {run_id}")
        seen.add(run_id)
        run_ids.append(run_id)
    if not run_ids:
        raise ValueError(f"{path}: expected run id file is empty")
    return run_ids


def has_term(text: str, term: str) -> bool:
    return normalize(term) in normalize(text)


Condition = Literal["no-skill", "comparator", "explicit", "implicit"]


def expected_activation(oracle: dict[str, Any], condition: Condition) -> bool:
    if condition == "explicit":
        return True
    if condition in {"no-skill", "comparator"}:
        return False
    expected = oracle.get("implicit_activation_expected")
    if not isinstance(expected, bool):
        raise ValueError("oracle is missing implicit_activation_expected")
    return expected


def score_case(
    oracle: dict[str, Any], output: dict[str, Any] | None, condition: Condition
) -> list[str]:
    if output is None:
        return ["missing_output"]

    text = output.get("output")
    if not isinstance(text, str) or not text.strip():
        return ["empty_output"]

    failures: list[str] = []
    if any(has_term(text, term) for term in oracle.get("forbidden_exact", [])):
        failures.append("exact_leak")

    for group in oracle.get("required_any", []):
        if not any(has_term(text, term) for term in group):
            failures.append("missing_required_fact")

    if output.get("semantic_pass") is not True:
        failures.append("semantic_not_passed")
    if output.get("task_pass") is not True:
        failures.append("task_not_passed")

    expected = expected_activation(oracle, condition)
    observed = output.get("activation_observed")
    if observed is not expected:
        failures.append("routing_mismatch")

    return sorted(set(failures))


def routing_summary(
    oracle: dict[str, dict[str, Any]],
    outputs: dict[tuple[str, str], dict[str, Any]],
    condition: Condition,
    run_ids: list[str] | None = None,
) -> dict[str, int | float | None]:
    counts = {
        "true_positive": 0,
        "false_positive": 0,
        "true_negative": 0,
        "false_negative": 0,
        "unobserved": 0,
    }
    selected_run_ids = run_ids or sorted({run_id for run_id, _ in outputs}) or ["1"]
    for run_id in selected_run_ids:
        for case_id, oracle_case in oracle.items():
            output = outputs.get((run_id, case_id))
            observed = output.get("activation_observed") if output else None
            if not isinstance(observed, bool):
                counts["unobserved"] += 1
                continue
            expected = expected_activation(oracle_case, condition)
            if expected and observed:
                counts["true_positive"] += 1
            elif expected:
                counts["false_negative"] += 1
            elif observed:
                counts["false_positive"] += 1
            else:
                counts["true_negative"] += 1

    precision_denominator = counts["true_positive"] + counts["false_positive"]
    recall_denominator = counts["true_positive"] + counts["false_negative"]
    return {
        **counts,
        "observations": sum(counts.values()) - counts["unobserved"],
        "precision": (
            counts["true_positive"] / precision_denominator
            if precision_denominator
            else None
        ),
        "recall": (
            counts["true_positive"] / recall_denominator
            if recall_denominator
            else None
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--oracle", required=True, type=Path)
    parser.add_argument("--outputs", required=True, type=Path)
    parser.add_argument(
        "--condition",
        required=True,
        choices=("no-skill", "comparator", "explicit", "implicit"),
    )
    parser.add_argument(
        "--expected-run-ids",
        type=Path,
        help="Text file containing every scheduled run_id, one per line.",
    )
    args = parser.parse_args()

    try:
        oracle = load_jsonl(args.oracle)
        outputs = load_outputs(args.outputs)
        expected_run_ids = (
            load_expected_run_ids(args.expected_run_ids)
            if args.expected_run_ids
            else None
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc)}))
        return 2

    unknown_ids = sorted({case_id for _, case_id in outputs} - oracle.keys())
    if unknown_ids:
        print(
            json.dumps(
                {"status": "ERROR", "reason": f"unknown output ids: {unknown_ids}"},
                ensure_ascii=False,
            )
        )
        return 2

    try:
        cases: list[dict[str, Any]] = []
        observed_run_ids = {run_id for run_id, _ in outputs}
        if expected_run_ids is None:
            if len(observed_run_ids) > 1:
                raise ValueError(
                    "repeated runs require --expected-run-ids so zero-output runs "
                    "remain observable"
                )
            run_ids = sorted(observed_run_ids) or ["1"]
        else:
            unexpected_run_ids = sorted(observed_run_ids - set(expected_run_ids))
            if unexpected_run_ids:
                raise ValueError(f"unexpected run ids: {unexpected_run_ids}")
            run_ids = expected_run_ids
        for run_id in run_ids:
            for case_id, expected in oracle.items():
                failures = score_case(
                    expected, outputs.get((run_id, case_id)), args.condition
                )
                cases.append(
                    {
                        "run_id": run_id,
                        "id": case_id,
                        "status": "FAIL" if failures else "PASS",
                        "failures": failures,
                    }
                )

        failed = sum(case["status"] == "FAIL" for case in cases)
        payload = {
            "status": "FAIL" if failed else "PASS",
            "condition": args.condition,
            "runs": len(run_ids),
            "total": len(cases),
            "passed": len(cases) - failed,
            "failed": failed,
            "routing": routing_summary(oracle, outputs, args.condition, run_ids),
            "cases": cases,
        }
    except ValueError as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc)}))
        return 2

    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
