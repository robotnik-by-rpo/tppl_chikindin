import subprocess
import sys
from pathlib import Path


MAIN = Path(__file__).parent.parent / "plib" / "main.py"


def run_cli(*args):
    result = subprocess.run(
        [sys.executable, str(MAIN), *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


class TestCLI:
    def test_normal_run(self):
        code, out, _ = run_cli("3 4 +")
        assert code == 0
        assert "7" in out

    def test_help_flag(self):
        code, out, _ = run_cli("-h")
        assert code == 0
        assert "stack machine" in out.lower()
        assert "~" in out

    def test_wrong_number_of_args(self):
        code, out, _ = run_cli()
        assert code == 0
        assert "Wrong arguments" in out

    def test_too_many_args(self):
        code, out, _ = run_cli("3 4 +", "extra")
        assert code == 0
        assert "Wrong arguments" in out

    def test_error_inside_expression(self):
        code, out, _ = run_cli("5 0 /")
        assert code == 0
        assert "Something happend" in out
        assert "division by zero" in out

    def test_empty_line(self):
        code, out, _ = run_cli("")
        assert code == 0
        assert "Something happend" in out