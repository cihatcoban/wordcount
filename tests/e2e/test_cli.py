"""End-to-End tests for CLI presentation adapter."""

import unittest
import subprocess
import json
import sys


class TestCLI(unittest.TestCase):

    def test_cli_execution_with_argument(self):
        cmd = [
            sys.executable,
            "-m", "wordcount.presentation.cli",
            "This is a CLI test of the modern architecture.",
            "--json"
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd="/working_dir/c_b2b2ae150d6ff711/wordcount-v2/src"
        )
        self.assertEqual(result.returncode, 0, f"CLI error: {result.stderr}")
        data = json.loads(result.stdout)
        self.assertEqual(data["words_total"], 9)
        self.assertIn("readability", data)

    def test_cli_execution_stdin(self):
        cmd = [
            sys.executable,
            "-m", "wordcount.presentation.cli",
            "-",
            "--json"
        ]
        result = subprocess.run(
            cmd,
            input="Standard input stream analysis test.",
            capture_output=True,
            text=True,
            cwd="/working_dir/c_b2b2ae150d6ff711/wordcount-v2/src"
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["words_total"], 5)


if __name__ == "__main__":
    unittest.main()
