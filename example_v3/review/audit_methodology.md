# Methodology Audit — Synthesis Critique

## Summary

The synthesis is well-structured, thematically comprehensive, and internally consistent on PRISMA arithmetic. The main weaknesses are: (1) predictive factors of CSI response — a core PICO outcome — receive only two paragraphs scattered across other themes rather than a dedicated section, despite 19 articles with relevant claims; (2) zero duplicates across three databases is never explained; (3) the single-day review timeline is not disclosed in limitations. Source balance is good, and confrontation of conflicting findings is present in Results though thin in the Discussion.

## Findings

### [F-MET-01] Predictive factors lack a dedicated section — major

**Detail**: PICO outcome #2 is "Predictive factors of response or failure" (protocol line 12, synthesis line 41). The synthesis covers this outcome only in two brief paragraphs: "Predictive factors for injection response" at the end of the Injection Technique theme (line 200) and "Risk factors for healing failure" at the end of the Surgical Outcomes theme (line 248). Meanwhile, `extracted_claims.json` contains 23 semantic claims about predictive/prognostic factors spread across 19 articles. This outcome is disproportionately thin relative to available literature and its prominence in the PICO framework.

**Recommendation**: Create a dedicated subsection "Predictive Factors of Response and Failure" within the thematic synthesis, consolidating evidence from both current paragraphs and drawing on the 19 articles with relevant claims.

---

### [F-MET-02] Zero duplicates across three databases unexplained — major

**Detail**: The PRISMA flow reports 552 identified records and 552 after deduplication (screening_log line 254, synthesis line 104). Querying PubMed, Semantic Scholar, and OpenAlex with overlapping search terms should produce substantial overlap (typically 20-40% for medical topics). The synthesis states "dedup performed during search phase" but provides no explanation for why zero duplicates were found. This is suspicious and undermines confidence in the deduplication step.

**Recommendation**: Document in the Methodology section (or an appendix) the deduplication method used and why the duplicate count is zero. If deduplication was performed upstream (e.g., DOI-based merge during search aggregation), state this explicitly with the tool/method used.

---

### [F-MET-03] Single-day review timeline not disclosed in limitations — minor

**Detail**: All screening dates in `screening_log.md` are 2026-04-02 (title, abstract, and full-text screening all on the same day). The search date in the synthesis is also 2026-04-02 (line 77). A 358-article review completed in a single day is only feasible with AI-assisted screening, which is disclosed, but the compressed timeline itself is not mentioned in the limitations section (lines 341-347). This is relevant because it precludes iterative reflection and quality checks between screening stages.

**Recommendation**: Add a sentence to the limitations acknowledging the single-session timeline (search through synthesis on the same day).

---

### [F-MET-04] Absence of snowballing not disclosed — minor

**Detail**: The protocol does not mention snowballing, and `screening_log.md` contains no snowballing section. The synthesis limitations (lines 341-347) do not mention that citation chaining / snowballing was not performed. For a 358-article scoping review, the absence of backward/forward citation tracking is a methodological limitation worth disclosing, particularly for identifying grey literature and seminal older works.

**Recommendation**: Add the absence of snowballing/citation chaining to the limitations section.

---

### [F-MET-05] All claims extracted from abstracts only — quality not assessed — minor

**Detail**: In `extracted_claims.json`, all 981 semantic claims have `"source": "abstract"` and all 358 articles have `"quality": null`. The synthesis limitations do mention "Claims were extracted from abstracts only" (line 345), which is good. However, the absence of any quality rating is not flagged despite it being noted in the Methodology as "Quality indicators (study design, sample size, bias risk) were noted during extraction" (line 126). The `quality` field is null for all 358 articles, contradicting this statement.

**Recommendation**: Either populate the quality field in `extracted_claims.json` as described in the Methodology, or revise the Methodology text to accurately state that no quality indicators were recorded. The current text ("were noted during extraction") is inaccurate.

---

### [F-MET-06] Discussion Main Findings partially restates Results — minor

**Detail**: The Discussion "Main Findings" subsection (lines 302-322) repeats several key claims already presented in the Results with the same citations (e.g., Hopewell_2021a, Beard_2018, Rossi_2024, Pang_2023, Traven_2019, Darbandi_2024). While some restatement is expected to frame interpretation, the five numbered points largely duplicate Results content without adding new interpretive depth. The "Interpretation and Implications" subsection (lines 324-334) does provide genuine interpretation.

**Recommendation**: Reduce restatement in Main Findings by focusing on synthesis across themes rather than repeating within-theme results. Reserve detailed evidence and citations for the Results.

---

### [F-MET-07] French geographic priority is thin and acknowledged late — minor

**Detail**: The protocol specifies "French data prioritized in synthesis" (protocol line 26). Only ~6 articles from French institutions are identifiable (Perdreau, Bonnevialle, Metayer, Dakkak, Darrieutort-Laffite, Lädermann). The synthesis mentions "French-language studies and French institutional data are sparse" (line 290) in Knowledge Gaps but not in the Limitations section proper. The geography sentence in Study Selection ("with French data prioritized", line 142) suggests prioritization occurred, but the actual French content in the synthesis is minimal.

**Recommendation**: Move the acknowledgment of sparse French data from Knowledge Gaps to the Limitations section, framing it as a gap between protocol intent and achievable coverage.

---

### [F-MET-08] Theme introductory paragraphs lack citations — minor

**Detail**: Each of the seven thematic subsections opens with an introductory paragraph (lines 160, 176, 190, 204, 220, 238, 254) that contains factual characterizations of the theme scope and article counts but no `[@...]` citations. While these are structural paragraphs rather than evidence claims, some contain factual statements (e.g., "intra-articular injection and hydrodilatation play a distinct role compared with subacromial injection for impingement" at line 220) that would benefit from sourcing.

**Recommendation**: Add at least one supporting citation to introductory paragraphs that contain factual claims about clinical practice.

---

## Walkthrough Decisions

All findings NOTED (validation run — no fixes applied). Findings recorded as skill diagnostics in pipeline_log.md.

| Finding | Severity | Decision | Rationale |
|---------|----------|----------|-----------|
| F-MET-01 | Major | NOTED | PICO outcome mapping gap — litrev-synthesize improvement target |
| F-MET-02 | Major | NOTED | Dedup documentation gap — litrev-search improvement target |
| F-MET-03 | Minor | NOTED | Timeline disclosure — orchestrator limitation |
| F-MET-04 | Minor | NOTED | Snowballing disclosure — orchestrator limitation |
| F-MET-05 | Minor | NOTED | Quality text contradicts null fields — litrev-extract/synthesize inconsistency |
| F-MET-06 | Minor | NOTED | Discussion restatement — litrev-synthesize writing quality |
| F-MET-07 | Minor | NOTED | French priority thin — overlaps F-FID-10, litrev-search limitation |
| F-MET-08 | Minor | NOTED | Unsourced theme intros — litrev-synthesize writing quality |

## Summary table

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 0 | — |
| Major | 2 | F-MET-01, F-MET-02 |
| Minor | 6 | F-MET-03, F-MET-04, F-MET-05, F-MET-06, F-MET-07, F-MET-08 |
