from pathlib import Path

from turinglab import SingleTapeTM

MACHINES_DIR = Path(__file__).parent.parent / "machines"


def run_machine(filename, input_string, max_steps=1000):
    tm = SingleTapeTM.from_yaml(str(MACHINES_DIR / filename))
    return tm.run(input_string, max_steps=max_steps)


class TestUnaryToBinary:
    def test_zero_unary_to_binary(self):
        result = run_machine("unary_to_binary.yaml", "")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "0"

    def test_one_unary_to_binary(self):
        result = run_machine("unary_to_binary.yaml", "1")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "1"

    def test_three_unary_to_binary(self):
        result = run_machine("unary_to_binary.yaml", "111")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "11"

    def test_five_unary_to_binary(self):
        result = run_machine("unary_to_binary.yaml", "11111")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "101"

    def test_eight_unary_to_binary(self):
        result = run_machine("unary_to_binary.yaml", "11111111")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "1000"


class TestBinaryCompare:
    def test_first_binary_is_greater(self):
        result = run_machine("binary_compare.yaml", "1100#1011")
        assert result.accepted is True

    def test_shorter_right_operand(self):
        result = run_machine("binary_compare.yaml", "10#1")
        assert result.accepted is True

    def test_equal_numbers_reject(self):
        result = run_machine("binary_compare.yaml", "101#101")
        assert result.accepted is False
        assert result.reason == "reject"

    def test_first_binary_is_smaller(self):
        result = run_machine("binary_compare.yaml", "1011#1100")
        assert result.accepted is False

    def test_zero_is_not_greater_than_one(self):
        result = run_machine("binary_compare.yaml", "0#1")
        assert result.accepted is False
