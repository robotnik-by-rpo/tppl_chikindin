
import pytest
from plib import StackMachin

@pytest.fixture
def machine():
    return StackMachin()


@pytest.fixture
def run(machine):
    def _run(expr: str):
        return machine.start(expr)
    return _run

class TestArithmetic:
    def test_plus(self, run):
        assert run("3 4 +") == 7

    def test_plus_negative(self, run):
        assert run("-5 3 +") == -2

    def test_minus(self, run):
        assert run("10 3 -") == 7

    def test_minus_negative_result(self, run):
        assert run("3 10 -") == -7

    def test_mul(self, run):
        assert run("6 7 *") == 42

    def test_mul_by_zero(self, run):
        assert run("5 0 *") == 0

    def test_div(self, run):
        assert run("20 4 /") == 5

    def test_div_integer(self, run):
        assert run("7 2 /") == 3

    def test_div_negative(self, run):
        assert run("-10 2 /") == -5

class TestArithmeticErrors:
    def test_div_by_zero(self, machine):
        with pytest.raises(ZeroDivisionError):
            machine.start("5 0 /")

    def test_plus_empty_stack(self, machine):
        with pytest.raises(IndexError):
            machine.start("+")

    def test_plus_one_operand(self, machine):
        with pytest.raises(IndexError):
            machine.start("1 +")

class TestTilda:
    def test_tilda_both_nonzero(self, run):
        assert run("10 3 ~") == 7

    def test_tilda_both_nonzero_reverse(self, run):
        assert run("3 10 ~") == 7

    def test_tilda_negative(self, run):
        assert run("-5 3 ~") == 8

    def test_tilda_with_zero_empty_stack(self, run):
        assert run("5 0 ~") == 0

    def test_tilda_with_zero_nonempty_stack(self, run):
        assert run("1 2 3 0 ~") == 9

    def test_tilda_with_zero_many_values(self, run):
        assert run("5 5 5 0 ~") == 100

    def test_tilda_chained(self, run):
        assert run("3 0 4 ~ 2 ~") == 7

    def test_tilda_empty_stack(self, machine):
        with pytest.raises(IndexError):
            machine.start("~")

    def test_tilda_one_operand(self, machine):
        with pytest.raises(IndexError):
            machine.start("5 ~")

class TestComplexExpressions:
    def test_user_example(self, run):
        assert run("2 2 + 4 - 4 ~ 2 3 * +") == 6

    def test_all_operations(self, run):
        assert run("2 3 + 4 * 10 - 2 /") == 5

    def test_nested_tilda(self, run):
        assert run("1 2 3 ~ 4 ~") == 3

    def test_tilda_then_plus(self, run):
        assert run("10 5 ~ 3 +") == 8

    def test_double_tilda_with_zero(self, run):
        assert run("5 7 0 ~ 4 ~") == 21 

class TestIsEmpty:
    def test_empty_line_raises(self, machine):
        with pytest.raises(NameError):
            machine.start("")

    def test_whitespace_only(self, machine):
        with pytest.raises(NameError):
            machine.start(" ")

class TestParsing:
    def test_wrong_token(self, machine):
        with pytest.raises(ValueError):
            machine.start("abc")

    def test_float_token(self, machine):
        with pytest.raises(ValueError):
            machine.start("1.5 2 +")

    def test_extra_numbers_returns_top(self, run):
        assert run("5 6 7 +") == 13

class TestIsolation:
    def test_two_machines_independent(self):
        m1 = StackMachin()
        m2 = StackMachin()
        assert m1.start("3 4 +") == 7
        assert m2.start("10 2 -") == 8

    def test_same_machine_reuse(self, machine):
        assert machine.start("3 4 +") == 7
        assert machine.start("10 2 -") == 8