from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "delivery-gate"


class BalancedSkillTests(unittest.TestCase):
    def test_runtime_preserves_core_skill_resources(self) -> None:
        files = sorted(
            path.relative_to(SKILL_ROOT).as_posix()
            for path in SKILL_ROOT.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        )
        self.assertEqual(
            files,
            [
                "SKILL.md",
                "agents/openai.yaml",
                "assets/decision-boundary.png",
                "assets/icon-400.png",
                "assets/icon.png",
                "scripts/check_surface.py",
            ],
        )

    def test_repository_keeps_background_and_behavior_evaluation(self) -> None:
        for path in (
            ROOT / "BACKGROUND.md",
            ROOT / "evals" / "evaluation-prompts.jsonl",
            ROOT / "evals" / "evaluation-oracle.jsonl",
            ROOT / "evals" / "evaluation-protocol.md",
            ROOT / "evals" / "score_eval.py",
            ROOT / "tests" / "evaluation-cases.md",
            ROOT / "tests" / "test_eval_integrity.py",
            ROOT / "tests" / "test_scanner.py",
            ROOT / "tests" / "test_scripts.py",
        ):
            with self.subTest(path=path):
                self.assertTrue(path.is_file())

    def test_custom_installer_and_provenance_stay_removed(self) -> None:
        for path in (
            ROOT / "scripts" / "install_skill.py",
            SKILL_ROOT / ".delivery-gate-provenance.json",
            ROOT / "tests" / "test_installer_scanner.py",
        ):
            with self.subTest(path=path):
                self.assertFalse(path.exists())

    def test_skill_balances_efficiency_with_delivery_context(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        words = re.findall(r"[A-Za-z0-9_-]+|[\u4e00-\u9fff]", text)

        self.assertLessEqual(len(words), 1200)
        for phrase in (
            "交付验收一下",
            "最少充分验证",
            "权威基线",
            "会话残留",
            "任务开始前",
            "外部操作",
            "有条件通过",
            "scripts/check_surface.py",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertNotIn("普通任务通常只需一个最相关的检查", text)

    def test_install_guide_is_short_and_uses_standard_installation(self) -> None:
        text = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 80)
        self.assertNotIn("provenance", text.casefold())
        self.assertNotIn("sha256", text.casefold().replace("-", ""))
        self.assertNotIn("install_skill.py", text)


if __name__ == "__main__":
    unittest.main()
