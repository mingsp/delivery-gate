# Delivery Gate

A lightweight, risk-adaptive, Chinese-first Codex Skill for deciding whether the current result is ready to deliver.

## Usage

```text
交付验收一下。
```

For explicit invocation:

```text
$delivery-gate 交付验收一下。
```

The Skill leads with `通过` (pass), `有条件通过` (conditional pass), or `未通过` (fail), followed only by the evidence and next action that matter.

## Principles

- Use the minimum check that could change the conclusion.
- Reuse applicable test or CI evidence instead of repeating equivalent work.
- Increase verification for production, money, sensitive data, irreversible actions, conflicting evidence, or test failures.
- Acceptance does not authorize edits, publication, deployment, or other external actions.

## Install

Ask Codex to install the `delivery-gate` directory from this repository into the user-level Skills directory. Back up an existing same-name directory instead of silently overwriting it.

Repository: <https://github.com/mingsp/delivery-gate>

## Development

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The runtime package contains only `SKILL.md`, OpenAI UI metadata, and icons.

## License

This project is derived from [LB623/no-negative-echo](https://github.com/LB623/no-negative-echo) under the MIT License and preserves the original copyright and license notice.
