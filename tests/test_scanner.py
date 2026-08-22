from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "delivery-gate" / "scripts" / "check_surface.py"


class ScannerTests(unittest.TestCase):
    def run_scan(
        self,
        root: Path,
        terms: bytes,
        filename: str,
        surface: bytes,
        *,
        scan_root: bool = False,
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        terms_path = root / "terms.txt"
        target = root / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        terms_path.write_bytes(terms)
        target.write_bytes(surface)
        command = [
            sys.executable,
            str(SCANNER),
            "--terms-file",
            str(terms_path),
        ]
        if scan_root:
            command.extend(["--root", str(root)])
        command.append(str(target))
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
        )
        return result, json.loads(result.stdout)

    def test_bom_terms_and_utf16_surface_fail(self) -> None:
        with TemporaryDirectory() as temp:
            result, payload = self.run_scan(
                Path(temp),
                b"\xef\xbb\xbfredis\n",
                "surface.txt",
                "Redis".encode("utf-16"),
            )
            self.assertEqual((result.returncode, payload["status"]), (1, "FAIL"))

    def test_filename_is_scanned_without_echoing_it(self) -> None:
        with TemporaryDirectory() as temp:
            result, payload = self.run_scan(
                Path(temp), b"SENSITIVE_CANARY\n", "SENSITIVE_CANARY.txt", b"clean"
            )
            self.assertEqual((result.returncode, payload["status"]), (1, "FAIL"))
            self.assertNotIn("SENSITIVE_CANARY", result.stdout)
            self.assertEqual(payload["failures"][0]["file_index"], 1)

    def test_root_relative_directory_name_is_scanned(self) -> None:
        with TemporaryDirectory() as temp:
            result, payload = self.run_scan(
                Path(temp),
                b"redis\n",
                "Redis/clean.txt",
                b"clean",
                scan_root=True,
            )
            self.assertEqual((result.returncode, payload["status"]), (1, "FAIL"))
            self.assertEqual(payload["failures"][0]["surfaces"], ["relative_path"])

    def test_root_scan_rejects_symlinked_ancestor(self) -> None:
        with TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "root"
            outside = base / "outside"
            root.mkdir()
            outside.mkdir()
            target = outside / "secret.txt"
            target.write_text("Redis", encoding="utf-8")
            alias = root / "alias"
            try:
                alias.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")
            terms = base / "terms.txt"
            terms.write_text("redis\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCANNER),
                    "--terms-file",
                    str(terms),
                    "--root",
                    str(root),
                    str(alias / "secret.txt"),
                ],
                capture_output=True,
                check=False,
                text=True,
            )
            payload = json.loads(result.stdout)

            self.assertEqual((result.returncode, payload["status"]), (2, "ERROR"))
            self.assertEqual(payload["reason_code"], "unsafe_path_component")

    def test_zero_width_requires_review(self) -> None:
        with TemporaryDirectory() as temp:
            result, payload = self.run_scan(
                Path(temp), b"redis\n", "surface.txt", "Re\u200bdis".encode()
            )
            self.assertEqual((result.returncode, payload["status"]), (1, "REVIEW"))

    def test_non_format_default_ignorable_requires_review(self) -> None:
        with TemporaryDirectory() as temp:
            result, payload = self.run_scan(
                Path(temp), b"redis\n", "surface.txt", "Re\u115fdis".encode()
            )
            self.assertEqual((result.returncode, payload["status"]), (1, "REVIEW"))

    def test_default_ignorable_in_terms_is_rejected(self) -> None:
        with TemporaryDirectory() as temp:
            result, payload = self.run_scan(
                Path(temp), "re\u200bdis\n".encode(), "surface.txt", b"Redis"
            )
            self.assertEqual((result.returncode, payload["status"]), (2, "ERROR"))
            self.assertEqual(payload["reason_code"], "unsafe_terms_characters")

    def test_invalid_encoding_is_structured_error(self) -> None:
        with TemporaryDirectory() as temp:
            result, payload = self.run_scan(
                Path(temp), b"redis\n", "surface.txt", b"\xff"
            )
            self.assertEqual((result.returncode, payload["status"]), (2, "ERROR"))
            self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
