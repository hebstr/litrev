#!/usr/bin/env python3
"""Unit tests for claim_patterns.py, extract_data.py, verify_claims.py, and fetch_fulltext.py."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from claim_patterns import (
    extract_claims as cp_extract_claims,
    extract_context as cp_extract_context,
    NUM_PATTERN,
    STAT_PATTERN,
)
from claim_patterns import extract_claims
from extract_data import (
    make_bibtex_key,
    deduplicate_keys,
)
from claim_patterns import extract_context
from verify_claims import (
    normalize_number,
    number_matches,
    extract_review_claims,
    resolve_key,
    build_doi_index,
    verify,
)
from bibtex_keys import parse_bib_keys_to_doi
from fetch_fulltext import extract_claims_from_text


# === claim_patterns.py (direct tests) ===


class TestNumPattern(unittest.TestCase):
    def test_percentage(self):
        assert NUM_PATTERN.search("was 9.7% in") is not None

    def test_plain_number(self):
        assert NUM_PATTERN.search("of 1600 patients") is not None

    def test_single_digit_matches_regex(self):
        assert NUM_PATTERN.search("were 3 groups") is not None

    def test_no_match_in_word(self):
        assert NUM_PATTERN.search("COVID19") is None

    def test_comma_decimal(self):
        m = NUM_PATTERN.search("was 3,5%")
        assert m is not None
        assert m.group(0) == "3,5%"


class TestStatPattern(unittest.TestCase):
    def test_odds_ratio(self):
        assert STAT_PATTERN.search("OR 2.35 (95% CI 1.12-4.98)") is not None

    def test_hazard_ratio(self):
        assert STAT_PATTERN.search("HR = 1.45") is not None

    def test_p_value(self):
        assert STAT_PATTERN.search("p < 0.001") is not None

    def test_confidence_interval(self):
        assert STAT_PATTERN.search("95% CI [1.10-1.88]") is not None

    def test_adjusted_or(self):
        assert STAT_PATTERN.search("aOR 0.72 (0.55-0.94)") is not None

    def test_no_false_positive(self):
        assert STAT_PATTERN.search("the ORGANIZATION was founded") is None


class TestCpExtractClaims(unittest.TestCase):
    def test_source_field(self):
        claims = cp_extract_claims("rate was 25%", source="pmc")
        assert all(c["source"] == "pmc" for c in claims)

    def test_no_source_field(self):
        claims = cp_extract_claims("rate was 25%")
        assert all("source" not in c for c in claims)

    def test_stat_subsumes_number(self):
        claims = cp_extract_claims("OR 2.35 was significant.")
        stat_vals = [c["value"] for c in claims if c["type"] == "statistic"]
        num_vals = [c["value"] for c in claims if c["type"] == "number"]
        assert any("2.35" in v for v in stat_vals)
        assert not any("2.35" == v for v in num_vals)

    def test_deduplication(self):
        claims = cp_extract_claims("25% and another 25% observed.")
        values = [c["value"] for c in claims]
        assert values.count("25%") == 1

    def test_single_digit_excluded(self):
        claims = cp_extract_claims("There were 3 groups.")
        values = [c["value"] for c in claims]
        assert "3" not in values

    def test_empty_input(self):
        assert cp_extract_claims("") == []


class TestCpExtractContext(unittest.TestCase):
    def test_short_text(self):
        ctx = cp_extract_context("The rate was 25%.", 13, 16, window=80)
        assert "25%" in ctx
        assert not ctx.startswith("...")

    def test_long_text_truncated(self):
        text = "A" * 200 + "TARGET" + "B" * 200
        ctx = cp_extract_context(text, 200, 206, window=20)
        assert "TARGET" in ctx
        assert ctx.startswith("...")
        assert ctx.endswith("...")


# === extract_data.py ===


class TestExtractClaims(unittest.TestCase):
    def test_percentage(self):
        claims = extract_claims("The prevalence was 9.7% in older adults.")
        values = [c["value"] for c in claims]
        assert any("9.7%" in v for v in values)

    def test_plain_number(self):
        claims = extract_claims("A total of 1600 patients were included.")
        values = [c["value"] for c in claims]
        assert any("1600" in v for v in values)

    def test_odds_ratio(self):
        claims = extract_claims("The OR was 2.35 (95% CI 1.12-4.98).")
        types = [c["type"] for c in claims]
        assert "statistic" in types

    def test_p_value(self):
        claims = extract_claims("This was significant (p < 0.001).")
        values = [c["value"] for c in claims]
        assert any("p" in v and "0.001" in v for v in values)

    def test_hazard_ratio(self):
        claims = extract_claims("HR = 1.45, 95% CI 1.10–1.88")
        types = [c["type"] for c in claims]
        assert "statistic" in types

    def test_empty_abstract(self):
        assert extract_claims("") == []

    def test_no_numbers(self):
        claims = extract_claims("This is a qualitative review of the literature.")
        assert len(claims) == 0

    def test_single_digit_excluded(self):
        claims = extract_claims("There were 3 groups in this study.")
        values = [c["value"] for c in claims]
        assert "3" not in values

    def test_deduplication(self):
        claims = extract_claims("The rate was 25% and another 25% was observed.")
        values = [c["value"] for c in claims]
        assert values.count("25%") == 1

    def test_stat_subsumes_number(self):
        claims = extract_claims("OR 2.35 was significant.")
        values = [c["value"] for c in claims]
        stat_values = [c["value"] for c in claims if c["type"] == "statistic"]
        num_values = [c["value"] for c in claims if c["type"] == "number"]
        assert any("2.35" in v for v in stat_values)
        assert not any("2.35" == v for v in num_values)


class TestMakeBibtexKey(unittest.TestCase):
    def test_authors_string(self):
        article = {"authors": "Abate M; Schiavone C;", "year": 2014}
        assert make_bibtex_key(article) == "Abate_2014"

    def test_authors_list(self):
        article = {"authors": ["Smith J", "Doe A"], "year": 2020}
        assert make_bibtex_key(article) == "Smith_2020"

    def test_single_author(self):
        article = {"authors": "Yamamoto", "year": 2019}
        assert make_bibtex_key(article) == "Yamamoto_2019"

    def test_empty_authors_fallback(self):
        article = {"authors": "", "first_author": "Jones", "year": 2021}
        assert make_bibtex_key(article) == "Jones_2021"

    def test_no_authors_no_fallback(self):
        article = {"year": 2021}
        assert make_bibtex_key(article) == "Unknown_2021"

    def test_missing_year(self):
        article = {"authors": "Smith J"}
        assert make_bibtex_key(article) == "Smith_0000"

    def test_comma_separated_author(self):
        article = {"authors": "Dupont, Marie; Martin, Jean", "year": 2022}
        assert make_bibtex_key(article) == "Dupont_2022"

    def test_van_der_prefix(self):
        article = {"authors": "van der Berg, Jan; Smith, John", "year": 2021}
        assert make_bibtex_key(article) == "van_2021"

    def test_cjk_author(self):
        article = {"authors": "Wang J; Li X", "year": 2023}
        assert make_bibtex_key(article) == "Wang_2023"

    def test_hyphenated_name(self):
        article = {"authors": "Al-Rashid, Omar; Jones, Paul", "year": 2020}
        assert make_bibtex_key(article) == "Al-Rashid_2020"


class TestDeduplicateKeys(unittest.TestCase):
    def test_no_duplicates(self):
        keys = ["Smith_2020", "Jones_2021", "Doe_2019"]
        assert deduplicate_keys(keys) == keys

    def test_two_duplicates(self):
        keys = ["Smith_2020", "Smith_2020"]
        result = deduplicate_keys(keys)
        assert result == ["Smith_2020a", "Smith_2020b"], f"got {result}"

    def test_three_duplicates(self):
        keys = ["X_2020", "X_2020", "X_2020"]
        result = deduplicate_keys(keys)
        assert result == ["X_2020a", "X_2020b", "X_2020c"], f"got {result}"

    def test_mixed(self):
        keys = ["A_2020", "B_2020", "A_2020"]
        result = deduplicate_keys(keys)
        assert result[0] == "A_2020a", f"got {result[0]}"
        assert result[1] == "B_2020", f"got {result[1]}"
        assert result[2] == "A_2020b", f"got {result[2]}"


class TestExtractContext(unittest.TestCase):
    def test_short_text(self):
        text = "The rate was 25%."
        ctx = extract_context(text, 13, 16, window=80)
        assert "25%" in ctx
        assert not ctx.startswith("...")

    def test_long_text_truncated(self):
        text = "A" * 200 + "TARGET" + "B" * 200
        ctx = extract_context(text, 200, 206, window=20)
        assert "TARGET" in ctx
        assert ctx.startswith("...")
        assert ctx.endswith("...")


# === verify_claims.py ===


class TestNormalizeNumber(unittest.TestCase):
    def test_comma_to_dot(self):
        assert normalize_number("3,5") == "3.5"

    def test_spaces_removed(self):
        assert normalize_number("1 000") == "1000"

    def test_nbsp_removed(self):
        assert normalize_number("1\u00a0000") == "1000"

    def test_already_normal(self):
        assert normalize_number("42.5") == "42.5"


class TestNumberMatches(unittest.TestCase):
    def test_exact_match(self):
        assert number_matches("25%", "25%")

    def test_substring_match(self):
        assert number_matches("2.35", "OR 2.35 (95% CI 1.12-4.98)")

    def test_float_tolerance(self):
        assert number_matches("9.7", "9.7%")

    def test_comma_vs_dot(self):
        assert number_matches("3,5", "3.5%")

    def test_no_match(self):
        assert not number_matches("99.9", "OR 2.35")

    def test_close_float_no_match(self):
        assert not number_matches("2.3", "2.34")

    def test_not_close_enough(self):
        assert not number_matches("2.3", "2.9")

    def test_no_partial_digit_match(self):
        assert not number_matches("3", "OR 2.35 (95% CI 1.12-4.98)")

    def test_no_substring_in_larger_number(self):
        assert not number_matches("12", "123 patients")

    def test_no_integer_prefix_of_decimal(self):
        assert not number_matches("10", "was 10.5%")
        assert not number_matches("42", "was 42.5%")
        assert not number_matches("1", "HR 1.45")
        assert not number_matches("2", "OR 2.35")

    def test_exact_within_stat_string(self):
        assert number_matches("95", "95% CI 1.12-4.98")


class TestExtractReviewClaims(unittest.TestCase):
    def test_number_with_citation(self):
        text = "The prevalence was 25% [@Smith_2020]."
        claims = extract_review_claims(text)
        assert len(claims) >= 1
        assert any(c["citation_key"] == "Smith_2020" for c in claims)
        assert any("25" in c["value"] for c in claims)

    def test_statistic_with_citation(self):
        text = "The OR was 2.35 (95% CI 1.12-4.98) [@Jones_2021]."
        claims = extract_review_claims(text)
        assert any(c["type"] == "statistic" for c in claims)

    def test_multiple_citations(self):
        text = "Rates of 30% [@A_2020; @B_2021] were reported."
        claims = extract_review_claims(text)
        keys = [c["citation_key"] for c in claims]
        assert "A_2020" in keys
        assert "B_2021" in keys

    def test_no_citation_no_claim(self):
        text = "The prevalence was 25% in the general population."
        claims = extract_review_claims(text)
        assert len(claims) == 0

    def test_p_value_with_citation(self):
        text = "This was significant (p < 0.001) [@Doe_2022]."
        claims = extract_review_claims(text)
        assert any("p" in c["value"] and "0.001" in c["value"] for c in claims)

    def test_suffixed_key(self):
        text = "A rate of 15% [@Smith_2020a] was found."
        claims = extract_review_claims(text)
        assert any(c["citation_key"] == "Smith_2020a" for c in claims)

    def test_sentence_boundary_blocks_match(self):
        text = "A cohort of 500 patients was enrolled. Other studies confirm this trend [@Jones_2021]."
        claims = extract_review_claims(text)
        matched_keys = [c["citation_key"] for c in claims if "500" in c["value"]]
        assert "Jones_2021" not in matched_keys

    def test_same_sentence_still_matches(self):
        text = "The prevalence was 9.7% in the adult population across three European countries [@Smith_2020]."
        claims = extract_review_claims(text)
        assert any(c["citation_key"] == "Smith_2020" and "9.7" in c["value"] for c in claims)

    def test_decimal_dot_not_blocked(self):
        text = "OR 2.35 was reported [@Doe_2022]."
        claims = extract_review_claims(text)
        assert any("2.35" in c["value"] for c in claims)

    def test_abbreviation_dot_not_blocked(self):
        text = "In a study by Smith et al. the rate was 42% [@Smith_2020]."
        claims = extract_review_claims(text)
        assert any("42" in c["value"] and c["citation_key"] == "Smith_2020" for c in claims)


class TestResolveKey(unittest.TestCase):
    def setUp(self):
        self.articles = {
            "Smith_2020": {"doi": "10.1234/a"},
            "Jones_2021": {"doi": "10.5678/b"},
        }
        self.bib_dois = {
            "SmithJ_2020": "10.1234/a",
        }
        self.doi_index = {
            "10.1234/a": "Smith_2020",
            "10.5678/b": "Jones_2021",
        }

    def test_direct_match(self):
        assert resolve_key("Smith_2020", self.articles, {}, {}) == "Smith_2020"

    def test_doi_resolution(self):
        result = resolve_key("SmithJ_2020", self.articles, self.bib_dois, self.doi_index)
        assert result == "Smith_2020"

    def test_no_match(self):
        result = resolve_key("Unknown_2020", self.articles, self.bib_dois, self.doi_index)
        assert result is None


class TestBuildDoiIndex(unittest.TestCase):
    def test_basic_index(self):
        extraction = {
            "articles": {
                "Smith_2020": {"doi": "10.1234/A"},
                "Jones_2021": {"doi": "10.5678/b"},
            }
        }
        index = build_doi_index(extraction)
        assert index["10.1234/a"] == "Smith_2020"
        assert index["10.5678/b"] == "Jones_2021"

    def test_empty_doi_skipped(self):
        extraction = {"articles": {"X_2020": {"doi": ""}}}
        assert build_doi_index(extraction) == {}


class TestParseBibKeysToDoi(unittest.TestCase):
    def test_basic_parsing(self, tmp_path=None):
        import tempfile
        bib = "@article{Smith_2020,\n  doi = {10.1234/abc},\n  title = {Test}\n}\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".bib", delete=False) as f:
            f.write(bib)
            path = f.name
        try:
            result = parse_bib_keys_to_doi(path)
            assert "Smith_2020" in result
            assert result["Smith_2020"] == "10.1234/abc"
        finally:
            os.unlink(path)

    def test_missing_file(self):
        assert parse_bib_keys_to_doi("/nonexistent/path.bib") == {}


# === fetch_fulltext.py ===


class TestExtractClaimsFromText(unittest.TestCase):
    def test_basic_extraction(self):
        text = "The incidence was 12.5% in the study group (n=350)."
        claims = extract_claims_from_text(text, "test")
        values = [c["value"] for c in claims]
        assert any("12.5%" in v for v in values)
        assert any("350" in v for v in values)

    def test_source_field(self):
        text = "OR 2.5 was found."
        claims = extract_claims_from_text(text, "pmc")
        assert all(c["source"] == "pmc" for c in claims)

    def test_empty_text(self):
        assert extract_claims_from_text("", "test") == []

    def test_statistics(self):
        text = "HR = 1.45, 95% CI 1.10–1.88, p < 0.01"
        claims = extract_claims_from_text(text, "test")
        types = [c["type"] for c in claims]
        assert "statistic" in types

    def test_verbatim_context(self):
        text = "X" * 200 + "The rate was 42% overall." + "Y" * 200
        claims = extract_claims_from_text(text, "test")
        pct_claims = [c for c in claims if "42%" in c["value"]]
        assert len(pct_claims) >= 1
        assert "..." in pct_claims[0]["verbatim"]


class TestVerify(unittest.TestCase):
    def _make_extraction(self, articles):
        return {"articles": articles}

    def _claim(self, value="25%", key="Smith_2020"):
        return {"value": value, "type": "percentage", "citation_key": key, "context": "..."}

    def test_verified(self):
        result = verify(
            [self._claim("25%")],
            self._make_extraction({"Smith_2020": {"doi": "", "has_abstract": True, "claims": [{"value": "25%"}]}}),
        )
        assert result["claims"][0]["status"] == "VERIFIED"
        assert result["summary"]["verified"] == 1

    def test_unverified(self):
        result = verify(
            [self._claim("99%")],
            self._make_extraction({"Smith_2020": {"doi": "", "has_abstract": True, "claims": [{"value": "25%"}]}}),
        )
        assert result["claims"][0]["status"] == "UNVERIFIED"
        assert result["summary"]["unverified"] == 1

    def test_no_abstract(self):
        result = verify(
            [self._claim("10")],
            self._make_extraction({"Smith_2020": {"doi": "", "has_abstract": False, "claims": []}}),
        )
        assert result["claims"][0]["status"] == "NO_ABSTRACT"
        assert result["summary"]["no_abstract"] == 1

    def test_no_extraction(self):
        result = verify(
            [self._claim("10", key="Unknown_2020")],
            self._make_extraction({}),
        )
        assert result["claims"][0]["status"] == "NO_EXTRACTION"
        assert result["summary"]["no_extraction"] == 1


if __name__ == "__main__":
    unittest.main()
