"""Tests for number matching in audit_claims (A2: Unicode middle dots, A3: spelled-out numbers)."""

import pytest

from litrev_mcp.tools.verify import _number_matches, _words_to_digits


class TestUnicodeMiddleDot:
    def test_middle_dot_decimal(self):
        assert _number_matches("2.8", "2\u00b78 points")

    def test_middle_dot_in_stat(self):
        assert _number_matches("0.73", "HR 0\u00b773 (95% CI)")

    def test_middle_dot_percentage(self):
        assert _number_matches("45.2", "45\u00b72%")


class TestSpelledOutNumbers:
    def test_thirteen(self):
        assert _number_matches("13", "Thirteen RCTs were included")

    def test_thirty_two_hyphenated(self):
        assert _number_matches("32", "Thirty-two trials met criteria")

    def test_twenty_one_space(self):
        assert _number_matches("21", "Twenty one studies")

    def test_one_hundred(self):
        assert _number_matches("100", "One hundred patients")

    def test_two_thousand(self):
        assert _number_matches("2000", "Two thousand participants")

    def test_five_hundred(self):
        assert _number_matches("500", "Five hundred records screened")

    def test_case_insensitive(self):
        assert _number_matches("13", "THIRTEEN RCTs")


class TestWordsToDigits:
    def test_basic(self):
        assert _words_to_digits("Thirteen RCTs") == "13 RCTs"

    def test_compound(self):
        assert _words_to_digits("Thirty-two trials") == "32 trials"

    def test_hundred(self):
        assert _words_to_digits("Five hundred patients") == "500 patients"

    def test_thousand(self):
        assert _words_to_digits("Two thousand cases") == "2000 cases"

    def test_preserves_digits(self):
        assert _words_to_digits("42 studies") == "42 studies"

    def test_no_false_positive_on_partial(self):
        result = _words_to_digits("someone returned")
        assert "one" not in result.split() or "someone" in result
