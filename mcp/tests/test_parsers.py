"""Unit tests for lib/parsers.py — all 6 format parsers + auto-detect."""

import pytest

from litrev_mcp.lib.parsers import (
    detect_format,
    parse,
    parse_bibtex,
    parse_doi_list,
    parse_pmid_list,
    parse_ris,
    parse_scopus_csv,
    parse_wos_tsv,
)


class TestDetectFormat:
    def test_bibtex(self):
        assert detect_format("@article{key, title={T}}") == "bibtex"

    def test_bibtex_leading_whitespace(self):
        assert detect_format("  \n@article{key, title={T}}") == "bibtex"

    def test_ris(self):
        assert detect_format("TY  - JOUR\nTI  - Test\nER  -") == "ris"

    def test_scopus_csv(self):
        header = "Authors,Title,Year,DOI,Source title,Abstract\n"
        assert detect_format(header + "a,b,2020,10.1/x,J,ab") == "scopus_csv"

    def test_wos_tsv(self):
        header = "AU\tTI\tPY\tDI\tSO\tAB\n"
        assert detect_format(header + "Auth\tTitle\t2020\t10.1/x\tJ\tAb") == "wos_tsv"

    def test_pmid_list(self):
        assert detect_format("12345678\n23456789\n") == "pmid_list"

    def test_doi_list(self):
        assert detect_format("10.1000/xyz\n10.2000/abc\n") == "doi_list"

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Cannot detect"):
            detect_format("random garbage that matches nothing")


class TestParseBibtex:
    SAMPLE = """
@article{Smith_2020,
  author = {Smith, John and Doe, Jane},
  title = {A Great Paper},
  journal = {Nature},
  year = {2020},
  doi = {10.1038/s41586-020-1234-5},
  pmid = {12345678},
  volume = {580},
  pages = {100--105},
  abstract = {This is the abstract.}
}
"""

    def test_basic_fields(self):
        records = parse_bibtex(self.SAMPLE)
        assert len(records) == 1
        r = records[0]
        assert r["title"] == "A Great Paper"
        assert r["authors"] == ["Smith, John", "Doe, Jane"]
        assert r["year"] == "2020"
        assert r["doi"] == "10.1038/s41586-020-1234-5"
        assert r["pmid"] == "12345678"
        assert r["journal"] == "Nature"
        assert r["abstract"] == "This is the abstract."
        assert r["source"] == "import-bibtex"
        assert r["first_author"] == "Smith"

    def test_optional_fields(self):
        records = parse_bibtex(self.SAMPLE)
        assert records[0]["volume"] == "580"
        assert records[0]["pages"] == "100--105"

    def test_multiple_entries(self):
        two = (
            self.SAMPLE
            + """
@inproceedings{Doe_2021,
  author = {Doe, Jane},
  title = {Another Paper},
  year = {2021}
}
"""
        )
        records = parse_bibtex(two)
        assert len(records) == 2
        assert records[1]["title"] == "Another Paper"

    def test_no_title_skipped(self):
        bib = "@article{k, author={A}, year={2020}}"
        assert parse_bibtex(bib) == []

    def test_escaped_chars(self):
        bib = "@article{k, title={A \\& B}, year={2020}}"
        records = parse_bibtex(bib)
        assert records[0]["title"] == "A & B"

    def test_numeric_year_field(self):
        bib = "@article{k, title={T}, year=2020}"
        records = parse_bibtex(bib)
        assert records[0]["year"] == "2020"

    def test_quoted_field_values(self):
        bib = '@article{k, title="Quoted Title", year="2020"}'
        records = parse_bibtex(bib)
        assert records[0]["title"] == "Quoted Title"


class TestParseRis:
    SAMPLE = """TY  - JOUR
TI  - A Great Paper
AU  - Smith, John
AU  - Doe, Jane
PY  - 2020
DO  - 10.1038/s41586-020-1234-5
JO  - Nature
AB  - This is the abstract.
VL  - 580
SP  - 100
EP  - 105
ER  -
"""

    def test_basic_fields(self):
        records = parse_ris(self.SAMPLE)
        assert len(records) == 1
        r = records[0]
        assert r["title"] == "A Great Paper"
        assert r["authors"] == ["Smith, John", "Doe, Jane"]
        assert r["year"] == "2020"
        assert r["doi"] == "10.1038/s41586-020-1234-5"
        assert r["journal"] == "Nature"
        assert r["abstract"] == "This is the abstract."
        assert r["source"] == "import-ris"
        assert r["first_author"] == "Smith"

    def test_pages(self):
        records = parse_ris(self.SAMPLE)
        assert records[0]["pages"] == "100-105"

    def test_multiple_entries(self):
        two = (
            self.SAMPLE
            + """TY  - CONF
TI  - Second Paper
AU  - Doe, Jane
PY  - 2021
ER  -
"""
        )
        records = parse_ris(two)
        assert len(records) == 2

    def test_no_title_skipped(self):
        ris = "TY  - JOUR\nAU  - Smith\nER  -\n"
        assert parse_ris(ris) == []

    def test_t1_fallback(self):
        ris = "TY  - JOUR\nT1  - Fallback Title\nER  -\n"
        records = parse_ris(ris)
        assert records[0]["title"] == "Fallback Title"

    def test_pmid_from_an(self):
        ris = "TY  - JOUR\nTI  - T\nAN  - 12345678\nER  -\n"
        records = parse_ris(ris)
        assert records[0]["pmid"] == "12345678"

    def test_an_non_numeric_ignored(self):
        ris = "TY  - JOUR\nTI  - T\nAN  - WOS:000123\nER  -\n"
        records = parse_ris(ris)
        assert records[0]["pmid"] == ""

    def test_flush_without_er(self):
        ris = "TY  - JOUR\nTI  - No End Tag\n"
        records = parse_ris(ris)
        assert len(records) == 1


class TestParseScopusCsv:
    HEADER = "Authors,Title,Year,DOI,Source title,Abstract,Cited by,PubMed ID,Volume,Page start,Page end,Document Type\n"

    def test_basic_row(self):
        row = "Smith J.;Doe J.,A Paper,2020,10.1/x,Nature,Abstract text,42,12345678,580,100,105,Article\n"
        records = parse_scopus_csv(self.HEADER + row)
        assert len(records) == 1
        r = records[0]
        assert r["title"] == "A Paper"
        assert r["authors"] == ["Smith J.", "Doe J."]
        assert r["year"] == "2020"
        assert r["doi"] == "10.1/x"
        assert r["citations"] == 42
        assert r["pmid"] == "12345678"
        assert r["source"] == "import-scopus"
        assert r["pages"] == "100-105"
        assert r["type"] == "Article"

    def test_missing_title_skipped(self):
        row = "Smith,,2020,10.1/x,J,Ab,0,,,,\n"
        assert parse_scopus_csv(self.HEADER + row) == []

    def test_non_numeric_citations(self):
        row = "A,Title,2020,,,Ab,N/A,,,,\n"
        records = parse_scopus_csv(self.HEADER + row)
        assert records[0]["citations"] == 0


class TestParseWosTsv:
    HEADER = "AU\tTI\tPY\tDI\tSO\tAB\tTC\tPM\tVL\tBP\tEP\tUT\tDT\n"

    def test_basic_row(self):
        row = "Smith, J\tA Paper\t2020\t10.1/x\tNature\tAbstract\t42\t12345678\t580\t100\t105\tWOS:000123\tArticle\n"
        records = parse_wos_tsv(self.HEADER + row)
        assert len(records) == 1
        r = records[0]
        assert r["title"] == "A Paper"
        assert r["year"] == "2020"
        assert r["citations"] == 42
        assert r["source"] == "import-wos"
        assert "WOS:000123" in r["url"]

    def test_missing_title_skipped(self):
        row = "A\t\t2020\t10.1/x\tJ\tAb\t0\t\t\t\t\t\t\n"
        assert parse_wos_tsv(self.HEADER + row) == []


class TestParsePmidList:
    def test_basic(self):
        records = parse_pmid_list("12345678\n23456789\n")
        assert len(records) == 2
        assert records[0]["pmid"] == "12345678"
        assert records[0]["title"] == ""
        assert records[0]["source"] == "import-pmid"
        assert "12345678" in records[0]["url"]

    def test_blank_lines_skipped(self):
        records = parse_pmid_list("12345678\n\n23456789\n\n")
        assert len(records) == 2

    def test_whitespace_stripped(self):
        records = parse_pmid_list("  12345678  \n")
        assert records[0]["pmid"] == "12345678"


class TestParseDoiList:
    def test_basic(self):
        records = parse_doi_list("10.1000/xyz\n10.2000/abc\n")
        assert len(records) == 2
        assert records[0]["doi"] == "10.1000/xyz"
        assert records[0]["title"] == ""
        assert records[0]["source"] == "import-doi"

    def test_blank_lines_skipped(self):
        records = parse_doi_list("10.1000/xyz\n\n")
        assert len(records) == 1


class TestParseDispatch:
    def test_auto_detect_bibtex(self):
        bib = "@article{k, title={T}, year={2020}}"
        records = parse(bib)
        assert records[0]["source"] == "import-bibtex"

    def test_explicit_format(self):
        records = parse("12345678\n23456789\n", fmt="pmid_list")
        assert len(records) == 2

    def test_ris_via_dispatch(self):
        ris = "TY  - JOUR\nTI  - Test\nER  -\n"
        records = parse(ris)
        assert records[0]["source"] == "import-ris"
