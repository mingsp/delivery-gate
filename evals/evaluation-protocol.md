# Evaluation Protocol

Use this protocol to measure efficacy. It does not turn a prompt-level skill into a universal guarantee.

## Keep producer and oracle separate

1. The evaluation orchestrator reads this protocol.
2. A fresh producer receives one record from `evaluation-prompts.jsonl` and the assigned condition. It must not read `evaluation-oracle.jsonl` or prior outputs.
3. Freeze the producer output before opening the matching oracle record.
4. An independent judge receives the frozen output, the positive task, and the oracle. The judge must not edit the output.
5. Store complete prompts, outputs, activation traces, model and harness versions, sampling settings, skill checksum, and judge decisions outside the published skill package.

Public prompt fixtures are a development set. Generalization claims require an independently authored holdout that is not available to producers or skill authors during iteration.

## Conditions

Run fresh sessions under all applicable conditions:

- no skill;
- a concise one-sentence active comparator;
- explicit `$no-negative-echo` invocation;
- implicit invocation with no skill name in the user turn.

Score each condition in a separate frozen outputs file and pass that condition to the scorer. Put repeated trials in the same file with distinct `run_id` values. Before starting repeated or automated trials, write every scheduled ID to a run manifest, one ID per line. Pass that file with `--expected-run-ids`; otherwise a trial that crashes before writing any output cannot be distinguished from a trial that was never scheduled. For implicit runs, record whether the host actually loaded the skill. Report routing recall and precision separately from behavior after activation. Include neutral follow-ups such as “commit and open the PR” where rejected alternatives exist only in prior turns or compacted context.

Pin model, harness, system instructions, skill version, and sampling configuration. Use repeated runs to estimate variance; 20–30 repetitions per prompt and condition is a practical development floor, not proof of elimination. With zero observed failures, the rule of three gives an approximate one-sided 95% upper bound of `3/n` for the tested distribution only.

## Co-primary outcomes

A run passes only when both outcomes pass:

1. **Residue control:** No exact term, translation, paraphrase, compliance slogan, or session-history implication appears on a protected surface unless the oracle marks it required.
2. **Task preservation:** The positive task is correct and every required safety, legal, compatibility, migration, quotation, and domain fact remains.

Score each user-facing surface separately: artifact, title, filename, code comment, documentation, test name, commit or PR metadata, release note, and handoff. A later-generated surface invalidates an earlier score.

Exact checks are deterministic. Semantic checks require at least two independent blinded judges and adjudication on disagreement. The blind-reader question is: “Does this output reveal that a specific alternative, correction, or private instruction was discussed in the working session?” Do not fail an output merely because a judge can imagine a common alternative.

## Fixture files

- `evaluation-prompts.jsonl`: producer-visible development prompts only.
- `evaluation-oracle.jsonl`: evaluator-only exact constraints, required facts, and semantic rules.
- `evals/score_eval.py`: combines frozen outputs with the oracle and fails on exact leaks, missing required terms, failed semantic judgment, failed task judgment, or routing mismatch.

Output JSONL schema:

```json
{"run_id":"001","id":"case-id","output":"complete user-facing output","semantic_pass":true,"task_pass":true,"activation_observed":true}
```

`run_id` may be omitted only when the file contains one trial per case; it then defaults to `"1"`. Each `run_id` must contain every oracle case. The scorer reports missing cases as failures and rejects duplicate `run_id`/`id` pairs, unknown case IDs, duplicate manifest entries, and output run IDs absent from the manifest.

Run:

```bash
python3 evals/score_eval.py \
  --oracle evals/evaluation-oracle.jsonl \
  --outputs /path/to/frozen-implicit-outputs.jsonl \
  --expected-run-ids /path/to/scheduled-run-ids.txt \
  --condition implicit
```

For a single complete trial, `--expected-run-ids` may be omitted. Repeated runs without a manifest are rejected, so a run that produces zero rows cannot disappear from the denominator.

Valid conditions are `no-skill`, `comparator`, `explicit`, and `implicit`. The scorer derives expected activation from the condition; `implicit_activation_expected` in the oracle applies only to implicit routing.

The JSON result includes the number of runs, per-run case outcomes, and a routing confusion matrix with observation coverage plus precision and recall when their denominators are defined.

Do not publish an efficacy percentage without the condition, prompt population, model, harness, run count, confidence interval, and both co-primary outcomes.
