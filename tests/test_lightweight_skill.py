from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "delivery-gate"


class LightweightSkillTests(unittest.TestCase):
    def test_runtime_contains_only_skill_metadata_and_icons(self) -> None:
        files = sorted(
            path.relative_to(SKILL_ROOT).as_posix()
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        )
        self.assertEqual(
            files,
            [
                "SKILL.md",
                "agents/openai.yaml",
                "assets/icon-400.png",
                "assets/icon.png",
            ],
        )

    def test_repository_has_no_custom_install_or_evaluation_framework(self) -> None:
        for path in (
            ROOT / "INSTALL.md",
            ROOT / "BACKGROUND.md",
            ROOT / "scripts",
            ROOT / "evals",
            ROOT / "tests" / "test_eval_integrity.py",
            ROOT / "tests" / "test_installer_scanner.py",
            ROOT / "tests" / "test_scripts.py",
        ):
            with self.subTest(path=path):
                self.assertFalse(path.exists())

    def test_skill_is_concise_and_keeps_the_core_contract(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        words = re.findall(r"[A-Za-z0-9_-]+|[\u4e00-\u9fff]", text)

        self.assertLessEqual(len(words), 500)
        self.assertIn("交付验收一下", text)
        self.assertIn("最少充分验证", text)
        self.assertIn("有条件通过", text)


if __name__ == "__main__":
    unittest.main()
