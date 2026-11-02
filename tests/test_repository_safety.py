"""Static checks that do not require Telegram credentials or network access."""
import ast
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositorySafetyTests(unittest.TestCase):
    def test_python_files_parse(self):
        for name in ("new_utagbot.py", "session_gen.py"):
            with self.subTest(file=name):
                ast.parse((ROOT / name).read_text(encoding="utf-8"))

    def test_session_generator_does_not_embed_credentials(self):
        source = (ROOT / "session_gen.py").read_text(encoding="utf-8")
        self.assertNotRegex(source, r"(?m)^\s*api_hash\s*=\s*['\"][0-9a-fA-F]{32}['\"]")
        self.assertNotRegex(source, r"(?m)^\s*api_id\s*=\s*\d+\s*$")

    def test_ignore_local_credentials(self):
        patterns = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for expected in (".env", "*.session", "*.session-journal"):
            with self.subTest(pattern=expected):
                self.assertIn(expected, patterns)


if __name__ == "__main__":
    unittest.main()
