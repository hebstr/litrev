import pytest

from litrev_mcp.lib.patterns import (
    NUM_PATTERN,
    STAT_PATTERN,
    extract_claims,
    extract_context,
)


class TestNumPattern:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("42%", ["42%"]),
            ("3.14", ["3.14"]),
            ("0,5%", ["0,5%"]),
            ("100", ["100"]),
        ],
    )
    def test_basic_matches(self, text, expected):
        assert NUM_PATTERN.findall(text) == expected

    def test_rejects_single_digit_in_word(self):
        assert NUM_PATTERN.findall("abc3def") == []

    def test_fraction_matches_numerator(self):
        assert NUM_PATTERN.findall("3/4") == ["3"]

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("63 565 cas", ["63 565"]),
            ("1 234 567", ["1 234 567"]),
            ("10\u00a0000", ["10\u00a0000"]),
            ("63 565,4%", ["63 565,4%"]),
        ],
    )
    def test_french_thousands(self, text, expected):
        assert NUM_PATTERN.findall(text) == expected

    def test_thousands_not_greedy(self):
        matches = NUM_PATTERN.findall("entre 63 565 et 72 000 cas")
        assert "63 565" in matches
        assert "72 000" in matches


class TestStatPattern:
    @pytest.mark.parametrize(
        "text",
        [
            "OR 2.5 (95% CI 1.1–4.0)",
            "HR=0.75",
            "aOR 3.2 (1.5-6.8), p<0.01",
            "RR 1.8",
            "p = 0.03",
            "95% CI [1.2, 3.4]",
            "95% CI [0.8-1.3]",
            "SMD 0.45 (0.2-0.7)",
            "NNT 8",
        ],
    )
    def test_matches(self, text):
        assert STAT_PATTERN.search(text) is not None, f"Should match: {text}"

    def test_rejects_plain_text(self):
        assert STAT_PATTERN.search("The study was inconclusive.") is None


class TestExtractContext:
    def test_short_text(self):
        result = extract_context("hello world", 0, 5, window=80)
        assert "hello" in result
        assert not result.startswith("...")

    def test_ellipsis_both_sides(self):
        text = "A" * 200
        result = extract_context(text, 100, 105, window=10)
        assert result.startswith("...")
        assert result.endswith("...")

    def test_whitespace_collapsed(self):
        result = extract_context("a  \n\t  b", 0, 7, window=80)
        assert "  " not in result


class TestExtractClaims:
    def test_empty_text(self):
        assert extract_claims("") == []
        assert extract_claims("", source="foo") == []

    def test_stat_claim(self):
        text = "The adjusted OR 2.5 (95% CI 1.1–4.0) was significant."
        claims = extract_claims(text)
        stats = [c for c in claims if c["type"] == "statistic"]
        assert len(stats) >= 1
        assert any("OR" in c["value"] for c in stats)

    def test_percentage_claim(self):
        text = "The prevalence was 42% in the study group."
        claims = extract_claims(text)
        pcts = [c for c in claims if c["type"] == "percentage"]
        assert len(pcts) >= 1
        assert any("42%" in c["value"] for c in pcts)

    def test_number_claim(self):
        text = "We enrolled 150 patients over 24 months."
        claims = extract_claims(text)
        nums = [c for c in claims if c["type"] == "number"]
        assert any("150" in c["value"] for c in nums)

    def test_source_propagated(self):
        claims = extract_claims("OR 1.5", source="Smith_2024")
        assert all(c["source"] == "Smith_2024" for c in claims)

    def test_no_source_when_empty(self):
        claims = extract_claims("OR 1.5")
        assert all("source" not in c for c in claims)

    def test_dedup_within_text(self):
        text = "OR 2.5 was found. The OR 2.5 was confirmed."
        claims = extract_claims(text)
        values = [c["value"] for c in claims]
        assert len(values) == len(set(values))

    def test_numbers_inside_stat_not_duplicated(self):
        text = "aOR 3.2 (1.5-6.8), p<0.01"
        claims = extract_claims(text)
        non_stat = [c for c in claims if c["type"] != "statistic"]
        stat_values = " ".join(c["value"] for c in claims if c["type"] == "statistic")
        for c in non_stat:
            assert c["value"] not in stat_values or c["type"] != "number"
