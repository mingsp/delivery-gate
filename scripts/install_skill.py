#!/usr/bin/env python3
"""Install the local no-negative-echo runtime package into Codex."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPOSITORY_ROOT / "no-negative-echo"


def default_skills_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    root = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
    return root / "skills"


def install_skill(source: Path, skills_dir: Path) -> Path:
    source = source.expanduser().resolve()
    skills_dir = skills_dir.expanduser().resolve()
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise ValueError(f"invalid Skill source: {source}")

    skills_dir.mkdir(parents=True, exist_ok=True)
    target = skills_dir / "no-negative-echo"
    with TemporaryDirectory(prefix=".no-negative-echo-install-", dir=skills_dir) as temp:
        temporary_root = Path(temp)
        staged = temporary_root / "staged"
        backup = temporary_root / "previous"
        shutil.copytree(
            source,
            staged,
            ignore=shutil.ignore_patterns("__pycache__", "*.py[cod]", ".DS_Store"),
        )

        had_previous = target.exists() or target.is_symlink()
        try:
            if had_previous:
                target.rename(backup)
            staged.rename(target)
        except Exception:
            if target.exists() or target.is_symlink():
                if target.is_dir() and not target.is_symlink():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            if had_previous and (backup.exists() or backup.is_symlink()):
                backup.rename(target)
            raise

    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--skills-dir", type=Path, default=default_skills_dir())
    args = parser.parse_args()

    try:
        target = install_skill(args.source, args.skills_dir)
    except (OSError, ValueError) as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        return 1

    print(f"Installed no-negative-echo to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
