import os
import tempfile

import pytest

from litrev_mcp.lib.bibtex import (
    build_bibtex_entry,
    deduplicate_keys,
    escape_bibtex,
    extract_doi_matches,
    make_bibtex_key,
    parse_bib_keys_to_doi,
    strip_code_blocks,
    unique_key,
)


class TestEscapeBibtex:
    def test_special_chars(self):
        assert escape_bibtex("A & B") == r"A \& B"
        assert escape_bibtex("100%") == r"100\%"
        assert escape_bibtex("item #1") == r"item \#1"

    def test_already_escaped_preserved(self):
        assert escape_bibtex(r"A \& B") == r"A \& B"

    def test_plain_text_unchanged(self):
        assert escape_bibtex("Hello World") == "Hello World"

    def test_tilde_and_caret(self):
        result = escape_bibtex("x~y^z")
        assert r"\textasciitilde{}" in result
        assert r"\textasciicircum{}" in result


class TestExtractDoiMatches:
    def test_basic_doi(self):
        assert extract_doi_matches("10.1000/xyz") == ["10.1000/xyz"]

    def test_dedup_preserves_order(self):
        text = "10.1000/a and 10.2000/b and 10.1000/a"
        assert extract_doi_matches(text) == ["10.1000/a", "10.2000/b"]

    def test_strips_trailing_punctuation(self):
        assert extract_doi_matches("10.1000/abc.") == ["10.1000/abc"]
        assert extract_doi_matches("10.1000/abc,") == ["10.1000/abc"]

    def test_strips_unbalanced_parens(self):
        assert extract_doi_matches("(10.1000/abc)") == ["10.1000/abc"]

    def test_balanced_parens_kept(self):
        result = extract_doi_matches("10.1000/abc(1)")
        assert result == ["10.1000/abc(1)"]

    def test_no_match(self):
        assert extract_doi_matches("no doi here") == []


class TestStripCodeBlocks:
    def test_removes_code_blocks(self):
        text = "before\n```python\ncode\n```\nafter"
        assert "code" not in strip_code_blocks(text)
        assert "before" in strip_code_blocks(text)

    def test_keep_bibtex(self):
        text = "text\n```bibtex\n@article{key,}\n```\nmore"
        result = strip_code_blocks(text, keep_bibtex=True)
        assert "@article" in result

    def test_keep_bibtex_removes_others(self):
        text = "```python\ncode\n```\n```bibtex\n@article{}\n```"
        result = strip_code_blocks(text, keep_bibtex=True)
        assert "code" not in result
        assert "@article" in result


class TestParseBibKeysToDoi:
    def test_parses_entries(self):
        bib = """@article{Smith2020,
  title={Something},
  doi={10.1000/abc},
}

@article{Jones2021,
  title={Other},
  doi={10.2000/def},
}
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".bib", delete=False) as f:
            f.write(bib)
            path = f.name
        try:
            result = parse_bib_keys_to_doi(path)
            assert result == {"Smith2020": "10.1000/abc", "Jones2021": "10.2000/def"}
        finally:
            os.unlink(path)

    def test_missing_file(self):
        assert parse_bib_keys_to_doi("/nonexistent/file.bib") == {}

    def test_entry_without_doi_skipped(self):
        bib = "@article{NoDoi,\n  title={No DOI here},\n}\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".bib", delete=False) as f:
            f.write(bib)
            path = f.name
        try:
            assert parse_bib_keys_to_doi(path) == {}
        finally:
            os.unlink(path)


class TestBuildBibtexEntry:
    def test_basic_entry(self):
        result = build_bibtex_entry("article", "Smith2020", {
            "title": "A Study",
            "year": "2020",
        })
        assert result.startswith("@article{Smith2020,")
        assert "title={A Study}" in result
        assert result.endswith("}")

    def test_escapes_values(self):
        result = build_bibtex_entry("article", "key", {"title": "A & B"})
        assert r"\&" in result

    def test_no_escape_doi(self):
        result = build_bibtex_entry("article", "key", {"doi": "10.1000/a_b"})
        assert r"\_" not in result
        assert "10.1000/a_b" in result

    def test_empty_fields_skipped(self):
        result = build_bibtex_entry("article", "key", {"title": "X", "abstract": ""})
        assert "abstract" not in result

    def test_sanitizes_key(self):
        result = build_bibtex_entry("article", "key with spaces!", {"title": "X"})
        assert "@article{keywithspaces," in result

    def test_no_trailing_comma(self):
        result = build_bibtex_entry("article", "key", {"title": "X"})
        lines = result.strip().split("\n")
        assert not lines[-2].endswith(",")


class TestUniqueKey:
    def test_new_key(self):
        seen = set()
        key, renamed = unique_key("Smith_2020", seen)
        assert key == "Smith_2020"
        assert renamed is None
        assert "Smith_2020" in seen

    def test_first_collision_renames_original(self):
        seen = {"Smith_2020"}
        key, renamed = unique_key("Smith_2020", seen)
        assert key == "Smith_2020b"
        assert renamed == ("Smith_2020", "Smith_2020a")

    def test_subsequent_collisions(self):
        seen = {"Smith_2020", "Smith_2020a"}
        key, renamed = unique_key("Smith_2020", seen)
        assert key == "Smith_2020b"
        assert renamed is None

    def test_overflow_raises(self):
        seen = {"k"} | {f"k{chr(ord('a') + i)}" for i in range(26)}
        with pytest.raises(RuntimeError):
            unique_key("k", seen)


class TestMakeBibtexKey:
    def test_with_first_author(self):
        assert make_bibtex_key({"first_author": "Smith", "year": 2020}) == "Smith_2020"

    def test_from_authors_list(self):
        key = make_bibtex_key({"authors": ["Smith J", "Jones A"], "year": 2021})
        assert key == "Smith_2021"

    def test_from_authors_string(self):
        key = make_bibtex_key({"authors": "Smith, J; Jones, A", "year": 2021})
        assert key == "Smith_2021"

    def test_missing_author(self):
        key = make_bibtex_key({"year": 2020})
        assert key == "Unknown_2020"

    def test_missing_year(self):
        key = make_bibtex_key({"first_author": "Smith"})
        assert key == "Smith_0000"


class TestDeduplicateKeys:
    def test_no_duplicates(self):
        assert deduplicate_keys(["a", "b", "c"]) == ["a", "b", "c"]

    def test_duplicates_get_suffixed(self):
        result = deduplicate_keys(["k", "k", "k"])
        assert result == ["ka", "kb", "kc"]

    def test_first_occurrence_renamed_on_collision(self):
        result = deduplicate_keys(["x", "y", "x"])
        assert result[0] == "xa"
        assert result[2] == "xb"
