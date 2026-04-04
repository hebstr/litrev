"""Integration tests for the import_corpus tool."""

import json
import os
import tempfile

import pytest

from litrev_mcp.tools.import_corpus import import_corpus


BIBTEX_SAMPLE = """
@article{Smith_2020,
  author = {Smith, John and Doe, Jane},
  title = {A Great Paper},
  journal = {Nature},
  year = {2020},
  doi = {10.1038/s41586-020-1234-5},
  abstract = {This is the abstract.}
}
@article{Lee_2021,
  author = {Lee, Alice},
  title = {Another Paper},
  journal = {Science},
  year = {2021},
  doi = {10.1126/science.abc1234}
}
"""

RIS_SAMPLE = """TY  - JOUR
TI  - RIS Paper One
AU  - Garcia, Maria
PY  - 2022
DO  - 10.1000/ris-test
JO  - JAMA
AB  - Abstract of the RIS paper.
ER  -
"""

SCOPUS_CSV_SAMPLE = (
    "Authors,Title,Year,DOI,Source title,Abstract,Cited by,PubMed ID\n"
    "Chen X.;Wang Y.,Scopus Paper,2023,10.1000/scopus,Lancet,Scopus abstract,15,99999999\n"
)

WOS_TSV_SAMPLE = (
    "AU\tTI\tPY\tDI\tSO\tAB\tTC\tPM\n"
    "Kim, S\tWoS Paper\t2021\t10.1000/wos\tBMJ\tWoS abstract\t8\t88888888\n"
)

PMID_SAMPLE = "12345678\n23456789\n"

DOI_SAMPLE = "10.1000/alpha\n10.2000/beta\n"


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


def _write(tmp_dir, name, content):
    path = os.path.join(tmp_dir, name)
    with open(path, "w") as f:
        f.write(content)
    return path


class TestImportCorpusBasic:
    def test_bibtex_parse_no_enrich(self, tmp_dir):
        path = _write(tmp_dir, "refs.bib", BIBTEX_SAMPLE)
        out = os.path.join(tmp_dir, "out.json")
        result = import_corpus(path, enrich=False, output_path=out)
        assert result["status"] == "ok"
        assert result["format"] == "bibtex"
        assert result["parsed"] == 2
        assert result["enrichment"] is None
        assert os.path.isfile(out)
        with open(out) as f:
            records = json.load(f)
        assert len(records) == 2
        assert records[0]["title"] == "A Great Paper"
        assert records[0]["source"] == "import-bibtex"

    def test_ris_parse_no_enrich(self, tmp_dir):
        path = _write(tmp_dir, "refs.ris", RIS_SAMPLE)
        result = import_corpus(path, enrich=False)
        assert result["status"] == "ok"
        assert result["format"] == "ris"
        assert result["parsed"] == 1

    def test_scopus_csv_parse_no_enrich(self, tmp_dir):
        path = _write(tmp_dir, "scopus.csv", SCOPUS_CSV_SAMPLE)
        result = import_corpus(path, enrich=False)
        assert result["status"] == "ok"
        assert result["format"] == "scopus_csv"
        assert result["parsed"] == 1

    def test_wos_tsv_parse_no_enrich(self, tmp_dir):
        path = _write(tmp_dir, "wos.txt", WOS_TSV_SAMPLE)
        result = import_corpus(path, enrich=False)
        assert result["status"] == "ok"
        assert result["format"] == "wos_tsv"
        assert result["parsed"] == 1

    def test_pmid_list_parse_no_enrich(self, tmp_dir):
        path = _write(tmp_dir, "pmids.txt", PMID_SAMPLE)
        result = import_corpus(path, enrich=False)
        assert result["status"] == "ok"
        assert result["format"] == "pmid_list"
        assert result["parsed"] == 2

    def test_doi_list_parse_no_enrich(self, tmp_dir):
        path = _write(tmp_dir, "dois.txt", DOI_SAMPLE)
        result = import_corpus(path, enrich=False)
        assert result["status"] == "ok"
        assert result["format"] == "doi_list"
        assert result["parsed"] == 2

    def test_explicit_format_override(self, tmp_dir):
        path = _write(tmp_dir, "data.txt", PMID_SAMPLE)
        result = import_corpus(path, format="pmid_list", enrich=False)
        assert result["format"] == "pmid_list"
        assert result["parsed"] == 2


class TestImportCorpusEdgeCases:
    def test_file_not_found(self, tmp_dir):
        result = import_corpus(os.path.join(tmp_dir, "nope.bib"), enrich=False)
        assert result["status"] == "error"
        assert "not found" in result["error"].lower()

    def test_undetectable_format(self, tmp_dir):
        path = _write(tmp_dir, "garbage.txt", "random garbage content here")
        result = import_corpus(path, enrich=False)
        assert result["status"] == "error"
        assert "detect" in result["error"].lower()

    def test_empty_file(self, tmp_dir):
        path = _write(tmp_dir, "empty.bib", "@article{k, author={A}}")
        result = import_corpus(path, enrich=False)
        assert result["status"] == "ok"
        assert result["parsed"] == 0

    def test_default_output_path(self, tmp_dir):
        path = _write(tmp_dir, "refs.bib", BIBTEX_SAMPLE)
        result = import_corpus(path, enrich=False)
        assert result["output_path"] == os.path.join(tmp_dir, "imported_results.json")
        assert os.path.isfile(result["output_path"])


class TestImportCorpusOutputSchema:
    def test_records_have_required_fields(self, tmp_dir):
        path = _write(tmp_dir, "refs.bib", BIBTEX_SAMPLE)
        out = os.path.join(tmp_dir, "out.json")
        import_corpus(path, enrich=False, output_path=out)
        with open(out) as f:
            records = json.load(f)
        required = {
            "title",
            "authors",
            "year",
            "doi",
            "pmid",
            "journal",
            "abstract",
            "citations",
            "url",
            "source",
        }
        for r in records:
            assert required <= set(r.keys()), (
                f"Missing fields: {required - set(r.keys())}"
            )

    def test_scopus_preserves_citations(self, tmp_dir):
        path = _write(tmp_dir, "scopus.csv", SCOPUS_CSV_SAMPLE)
        out = os.path.join(tmp_dir, "out.json")
        import_corpus(path, enrich=False, output_path=out)
        with open(out) as f:
            records = json.load(f)
        assert records[0]["citations"] == 15

    def test_pmid_list_sparse_records(self, tmp_dir):
        path = _write(tmp_dir, "pmids.txt", PMID_SAMPLE)
        out = os.path.join(tmp_dir, "out.json")
        import_corpus(path, enrich=False, output_path=out)
        with open(out) as f:
            records = json.load(f)
        assert records[0]["title"] == ""
        assert records[0]["pmid"] == "12345678"
