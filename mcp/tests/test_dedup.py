from litrev_mcp.lib.dedup import deduplicate_simple, deduplicate_merge


class TestDeduplicateSimple:
    def test_empty(self):
        assert deduplicate_simple([]) == []

    def test_no_duplicates(self):
        results = [
            {"pmid": "1", "title": "Alpha"},
            {"pmid": "2", "title": "Beta"},
        ]
        assert deduplicate_simple(results) == results

    def test_dedup_by_pmid(self):
        results = [
            {"pmid": "1", "title": "First"},
            {"pmid": "1", "title": "Duplicate"},
        ]
        out = deduplicate_simple(results)
        assert len(out) == 1
        assert out[0]["title"] == "First"

    def test_dedup_by_doi(self):
        results = [
            {"doi": "10.1000/abc", "title": "A"},
            {"doi": "10.1000/ABC", "title": "B"},
        ]
        out = deduplicate_simple(results)
        assert len(out) == 1

    def test_dedup_by_normalized_title(self):
        results = [
            {"title": "Effect of Drug X on Outcome Y"},
            {"title": "Effect of Drug X on Outcome Y!"},
        ]
        out = deduplicate_simple(results)
        assert len(out) == 1

    def test_missing_fields_no_crash(self):
        results = [
            {},
            {"pmid": None, "doi": None, "title": None},
            {"pmid": "", "doi": "", "title": ""},
        ]
        assert len(deduplicate_simple(results)) == 3

    def test_pmid_as_int(self):
        results = [
            {"pmid": 12345, "title": "A"},
            {"pmid": "12345", "title": "B"},
        ]
        out = deduplicate_simple(results)
        assert len(out) == 1


class TestDeduplicateMerge:
    def test_empty(self):
        assert deduplicate_merge([]) == []

    def test_merges_fields(self):
        results = [
            {"pmid": "1", "title": "Study A", "doi": ""},
            {"pmid": "1", "title": "", "doi": "10.1000/x"},
        ]
        out = deduplicate_merge(results)
        assert len(out) == 1
        assert out[0]["title"] == "Study A"
        assert out[0]["doi"] == "10.1000/x"

    def test_first_value_wins(self):
        results = [
            {"pmid": "1", "abstract": "Full abstract here"},
            {"pmid": "1", "abstract": "Different abstract"},
        ]
        out = deduplicate_merge(results)
        assert out[0]["abstract"] == "Full abstract here"

    def test_dedup_cascade_pmid_doi_title(self):
        results = [
            {"pmid": "1", "doi": "10.1000/a", "title": "Study"},
            {"doi": "10.1000/a", "extra": "via doi"},
            {"title": "Study", "extra2": "via title"},
        ]
        out = deduplicate_merge(results)
        assert len(out) == 1
        assert out[0]["extra"] == "via doi"
        assert out[0]["extra2"] == "via title"

    def test_no_duplicates_preserved(self):
        results = [
            {"pmid": "1", "title": "A"},
            {"pmid": "2", "title": "B"},
        ]
        assert deduplicate_merge(results) == results

    def test_track_stats_returns_tuple(self):
        results = [
            {"pmid": "1", "title": "A"},
            {"pmid": "2", "title": "B"},
        ]
        out, stats = deduplicate_merge(results, track_stats=True)
        assert len(out) == 2
        assert stats == {"by_pmid": 0, "by_doi": 0, "by_title": 0}

    def test_track_stats_counts_methods(self):
        results = [
            {"pmid": "1", "doi": "10.1/a", "title": "Alpha"},
            {"pmid": "1", "title": "Dup by pmid"},
            {"doi": "10.1/b", "title": "Beta"},
            {"doi": "10.1/b", "title": "Dup by doi"},
            {"title": "Gamma"},
            {"title": "Gamma!"},
        ]
        out, stats = deduplicate_merge(results, track_stats=True)
        assert len(out) == 3
        assert stats["by_pmid"] == 1
        assert stats["by_doi"] == 1
        assert stats["by_title"] == 1

    def test_no_track_stats_returns_list(self):
        results = [{"pmid": "1"}, {"pmid": "1"}]
        out = deduplicate_merge(results)
        assert isinstance(out, list)
