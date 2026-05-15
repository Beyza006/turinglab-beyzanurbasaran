from pathlib import Path

import pytest

from turinglab import SingleTapeTM

MACHINES_DIR = Path(__file__).parent.parent / "machines"


def run_machine(filename, input_string, max_steps=2000):
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

    def test_nine_unary_to_binary(self):
        result = run_machine("unary_to_binary.yaml", "111111111")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "1001"

    def test_twelve_unary_to_binary(self):
        result = run_machine("unary_to_binary.yaml", "111111111111")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "1100"

    def test_sixteen_unary_to_binary(self):
        result = run_machine("unary_to_binary.yaml", "1111111111111111")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "10000"


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

    def test_fifteen_is_greater_than_zero(self):
        result = run_machine("binary_compare.yaml", "1111#0")
        assert result.accepted is True

    def test_eight_is_greater_than_seven(self):
        result = run_machine("binary_compare.yaml", "1000#111")
        assert result.accepted is True

    def test_three_is_not_greater_than_nine(self):
        result = run_machine("binary_compare.yaml", "11#1001")
        assert result.accepted is False

    def test_fourteen_is_not_greater_than_fifteen(self):
        result = run_machine("binary_compare.yaml", "1110#1111")
        assert result.accepted is False


class TestStringCopy:
    def test_copy_abba(self):
        result = run_machine("string_copy.yaml", "abba")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "abba#abba"

    def test_copy_single_a(self):
        result = run_machine("string_copy.yaml", "a")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "a#a"

    def test_copy_single_b(self):
        result = run_machine("string_copy.yaml", "b")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "b#b"

    def test_copy_mixed_string(self):
        result = run_machine("string_copy.yaml", "abab")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "abab#abab"

    def test_copy_empty_string(self):
        result = run_machine("string_copy.yaml", "")
        assert result.accepted is True
        assert result.final_tape.strip("B") == "#"


class TestStudentChoiceDivisibleByFour:
    def test_zero_is_divisible_by_four(self):
        result = run_machine("student_choice.yaml", "0")
        assert result.accepted is True

    def test_four_is_divisible_by_four(self):
        result = run_machine("student_choice.yaml", "100")
        assert result.accepted is True

    def test_twelve_is_divisible_by_four(self):
        result = run_machine("student_choice.yaml", "1100")
        assert result.accepted is True

    def test_two_is_not_divisible_by_four(self):
        result = run_machine("student_choice.yaml", "10")
        assert result.accepted is False
        assert result.reason == "reject"

    def test_empty_input_rejects(self):
        result = run_machine("student_choice.yaml", "")
        assert result.accepted is False


class TestExpandedMachineCoverage:
    @pytest.mark.parametrize("count", range(17))
    def test_unary_to_binary_all_supported_counts(self, count):
        result = run_machine("unary_to_binary.yaml", "1" * count)
        assert result.accepted is True
        assert result.final_tape.strip("B") == bin(count)[2:]

    @pytest.mark.parametrize("left", range(16))
    @pytest.mark.parametrize("right", range(16))
    def test_binary_compare_all_supported_pairs(self, left, right):
        left_bits = bin(left)[2:]
        right_bits = bin(right)[2:]
        result = run_machine("binary_compare.yaml", f"{left_bits}#{right_bits}")
        assert result.accepted is (left > right)
        if left <= right:
            assert result.reason == "reject"

    @pytest.mark.parametrize(
        ("input_string", "expected"),
        [
            ("aaaa", "aaaa#aaaa"),
            ("bbbb", "bbbb#bbbb"),
            ("baab", "baab#baab"),
            ("ababba", "ababba#ababba"),
        ],
    )
    def test_string_copy_additional_patterns(self, input_string, expected):
        result = run_machine("string_copy.yaml", input_string)
        assert result.accepted is True
        assert result.final_tape.strip("B") == expected

    def test_string_copy_unknown_symbol_stops_with_no_transition(self):
        result = run_machine("string_copy.yaml", "abc")
        assert result.accepted is False
        assert result.reason == "no_transition"

    @pytest.mark.parametrize("input_string", ["10100", "100000", "00100"])
    def test_student_choice_more_divisible_inputs(self, input_string):
        result = run_machine("student_choice.yaml", input_string)
        assert result.accepted is True

    @pytest.mark.parametrize("input_string", ["1", "111", "10101"])
    def test_student_choice_more_non_divisible_inputs(self, input_string):
        result = run_machine("student_choice.yaml", input_string)
        assert result.accepted is False
        assert result.reason == "reject"
