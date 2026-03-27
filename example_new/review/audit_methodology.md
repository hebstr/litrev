# Methodology Audit — Synthesis Critique

## Summary

The review is well-structured with thematic organization covering all four PEO outcome domains. PRISMA-ScR flow is arithmetically consistent. The main methodological concerns are: only 2 databases contributed topical results (protocol specified 3), snowballing was not performed, and the Discussion section leans toward cumulative language without confronting contradictory findings.

## Findings

### [F-MET-01] Database shortfall: 2 of 3 planned databases searched — Major

**Detail**: The protocol (`protocol.md` line 29–31) specifies three databases: PubMed/MEDLINE, Scopus, and Web of Science. Only PubMed and Semantic Scholar (a substitute, not in the original protocol) were actually searched. Scopus and Web of Science were not queried due to institutional access constraints. OpenAlex was attempted but discarded (off-topic results).

The review documents this at lines 39 and 49 of the methodology section and at line 233 in limitations. However, the deviation from the protocol is not explicitly framed as a protocol deviation — it reads as a neutral description rather than a declared limitation.

**Recommendation**: In the methodology section, add an explicit statement: "This constitutes a deviation from the planned protocol, which specified Scopus and Web of Science." The ready-to-paste queries in `search_log.md` partially mitigate the issue.

---

### [F-MET-02] Snowballing not performed and not documented as omission — Minor

**Detail**: For scoping reviews, the SKILL routing table recommends snowballing (both directions). Snowballing was not performed and `screening_log.md` contains no snowballing section. The review's limitations section (line 233) does not mention the absence of citation chaining/snowballing.

**Recommendation**: Add a brief mention in limitations that citation chaining (forward/backward snowballing) was not performed, which may have missed relevant articles not indexed in the searched databases.

---

### [F-MET-03] PRISMA-ScR flow: minor discrepancy in identified count — Minor

**Detail**: The search_log.md summary states "Total: 3432" identified and "After deduplication: 3368 unique articles." The review at line 69 states "Records identified across databases (n = 3,432), deduplicated (n = 3,368)." The PRISMA flow at lines 72–75 confirms: 3,432 → 3,368 → 2,485 → 80.

Arithmetic check:
- 3,432 - 64 duplicates = 3,368 (consistent)
- 3,368 - 883 title excluded = 2,485 (consistent)
- 2,485 - 2,405 abstract excluded = 80 (consistent: 2,359 abstract-excluded + 46 no-abstract excluded = 2,405)

All counts are arithmetically consistent across documents.

**Recommendation**: No action needed — this item passes.

---

### [F-MET-04] Discussion uses predominantly cumulative language — Major

**Detail**: The Discussion section (lines 199–233) summarizes five key findings but does not confront contradictory evidence between studies. Language is consistently additive: "aligns with", "confirming", "support the need for", "has been specifically studied". No study disagreements or heterogeneity in findings are discussed, despite the abstract noting "wide heterogeneity in estimates."

For example:
- Prevalence ranges "7% to 26%" in general population vs "41% to 66%" in occupational groups, but no discussion of why this 10-fold range exists beyond "case definition, recall period, and population selection."
- No confrontation of studies that may show null associations for risk factors.

**Recommendation**: Add a paragraph in the Discussion acknowledging specific areas where studies disagree, and discuss possible explanations for heterogeneity (e.g., diagnostic criteria differences, population age distributions, study quality variation).

---

### [F-MET-05] Single-day review timeline not disclosed — Minor

**Detail**: The `screening_log.md` dates show all phases were conducted on 2026-03-27 (search, title screening, abstract screening, full-text screening). The review does not disclose that the entire review was conducted in a single session/day, which is atypical for scoping reviews and relevant for reproducibility assessment.

**Recommendation**: Add to limitations: "The search, screening, and extraction were conducted within a single session, which may limit the depth of individual article assessment."

---

### [F-MET-06] LLM-assisted screening acknowledged but extraction method understated — Minor

**Detail**: Line 71 discloses "Screening was performed by a single AI reviewer." Line 79 states "Quantitative claims were extracted automatically from abstracts using regex-based pattern matching, followed by semantic enrichment." However, the synthesis itself was also AI-generated, which is not explicitly stated. Full transparency requires disclosing that extraction, screening, and synthesis were all AI-assisted.

**Recommendation**: Add to the methodology or limitations that the synthesis was also AI-assisted, not just screening and extraction.

---

### [F-MET-07] Unsourced factual statements in Discussion — Minor

**Detail**: Several paragraphs in the Discussion section contain factual claims without citations:
- Line 217: "The wide prevalence variations and the strong influence of occupational factors support the need to link national-level (SNDS) data" — no citation.
- Line 219: "The known association between diabetes and corticosteroid-related glycemic excursions" — no citation for this clinical claim.
- Line 223–225: Implications paragraphs contain no citations.

**Recommendation**: Add supporting citations to factual claims in the Discussion, or qualify them as interpretive statements of the review authors.

---

### [F-MET-08] Geographic priority: French data coverage is thin — Minor

**Detail**: The protocol specifies "Données françaises privilégiées dans la synthèse." Among 80 included articles, French-specific data come primarily from the Cosali cohort (5 publications from the same cohort). No other French institutional or epidemiological data sources are represented. This is acknowledged in Knowledge Gaps (line 189) and limitations (line 233).

See also F-FID-05 for the grey literature gap.

**Recommendation**: Already documented. No additional action beyond what F-FID-05 recommends.

---

## Summary table

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 0 | — |
| Major | 2 | F-MET-01, F-MET-04 |
| Minor | 5 | F-MET-02, F-MET-05, F-MET-06, F-MET-07, F-MET-08 |

## Walkthrough Decisions (2026-03-27)

| Finding | Severity | Decision | Action |
|---------|----------|----------|--------|
| F-MET-01 | Major | ACCEPTED | Protocol deviation explicitly declared in methodology |
| F-MET-02 | Minor | ACCEPTED | Snowballing omission added to limitations (item 7) |
| F-MET-03 | Minor | NOTED | Arithmetic verified, all counts consistent |
| F-MET-04 | Major | ACCEPTED | "Sources of Heterogeneity" paragraph added to Discussion |
| F-MET-05 | Minor | ACCEPTED | Single-session timeline added to limitations (item 8) |
| F-MET-06 | Minor | ACCEPTED | Full AI-assisted disclosure added in Synthesis Approach |
| F-MET-07 | Minor | ACCEPTED | Citations added to unsourced claims in Discussion |
| F-MET-08 | Minor | NOTED | Cross-ref F-FID-05, already documented |
