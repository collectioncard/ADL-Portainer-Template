import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calculator import calculate


class CalculatorTests(unittest.TestCase):
    def test_operations(self):
        self.assertEqual(calculate("add", 2, 3), 5)
        self.assertEqual(calculate("subtract", 10, 4), 6)
        self.assertEqual(calculate("multiply", 7, 8), 56)
        self.assertEqual(calculate("divide", 9, 3), 3)

    def test_division_by_zero(self):
        with self.assertRaisesRegex(ValueError, "divide by zero"):
            calculate("divide", 5, 0)

    def test_cli_writes_json_result(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "run.json"
            proc = subprocess.run(
                [sys.executable, str(ROOT / "calculator.py"), "multiply", "12", "8", "--output", str(output)],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn('"result": 96.0', proc.stdout)
            self.assertEqual(json.loads(output.read_text())["result"], 96)


if __name__ == "__main__":
    unittest.main()
