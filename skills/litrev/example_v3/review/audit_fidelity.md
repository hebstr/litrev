# Fidelity Audit — Claims vs Sources

## Summary

- **4,195 quantitative claims** and **981 semantic claims** extracted from **358 articles** (348 with abstracts)
- Automated audit: 52 VERIFIED, 44 UNVERIFIED, 0 NO_ABSTRACT, 0 NO_EXTRACTION (96 claims checked in review text)
- BibTeX entries: 58 total, 1 orphan
- 10 articles included with zero extracted claims (all lacking abstracts)

---

## Findings

### [F-FID-01] Hopewell_2021 numbers attributed to wrong publication — minor

**Detail**: The review text attributes "adjusted mean difference -5.64, 99% CI -9.93 to -1.34" to `[@Hopewell_2021a; @Hopewell_2021b]`. These numbers do not appear in the Hopewell_2021a abstract (the Lancet paper, DOI 10.1016/S0140-6736(21)00846-1), which reports only `-0·66 [99% CI -4·52 to 3·20]` (exercise vs advice) and `-1·11 [-4·47 to 2·26]` (injection vs no injection over 12 months). The -5.64 figure is present in the Hopewell_2021b abstract (the HTA report, DOI 10.3310/hta25480), which is the full report of the same GRASP trial at 8 weeks.

The automated audit flagged these as UNVERIFIED because the audit tool only checked against the first Hopewell_2021 entry. The numbers are traceable to Hopewell_2021b but the dual citation `[@Hopewell_2021a; @Hopewell_2021b]` is imprecise: the 8-week result (-5.64) comes specifically from the HTA report (2021b), while the 12-month result (-1.11) comes from the Lancet paper (2021a).

**Recommendation**: Attribute the 8-week result (-5.64) specifically to `[@Hopewell_2021b]` and the 12-month result (-1.11) to `[@Hopewell_2021a]`.

---

### [F-FID-02] Darbandi_2024 attributed numbers from Kunze_2020 — major

**Detail**: The review text states: "A systematic review and meta-analysis of 10 studies (n=240,976) found that 20.0% received a perioperative CSI" with citation `[@Darbandi_2024; @Kunze_2020]`. The numbers 240,976 and 20.0% do not appear in the Darbandi_2024 abstract. They appear in the Kunze_2020 abstract: "A total of 10 studies including 240,976 patients were identified; 20.0% received a perioperative CSI."

Darbandi_2024 is a separate systematic review focused on preoperative risk factors for revision surgery. The sentence conflates two distinct meta-analyses as if they were the same study. The "47% increased risk (OR 1.44, 95% CI 1.36-1.52)" finding is correctly attributed to Darbandi_2024.

**Recommendation**: Split the sentence. Attribute the "10 studies, n=240,976, 20.0% perioperative CSI" finding to `[@Kunze_2020]` only. Keep the "47% increased risk" finding attributed to `[@Darbandi_2024]`.

---

### [F-FID-03] Azevedo_2020 "30%" is an introduction-level context figure, not the study's own result — minor

**Detail**: The review opens with: "Shoulder pain is one of the most prevalent musculoskeletal complaints, affecting up to 30% of primary care consultations for musculoskeletal disorders [@Azevedo_2020]." The Azevedo_2020 abstract states: "Shoulder pain is a common cause of consultation in Primary Health Care, and may correspond to up to 30% of the reasons for consultation." This 30% figure appears in the introduction of the Azevedo abstract as background context, not as the study's own finding. The study itself evaluated 119 patients for predictive factors of treatment response.

This is a context-vs-result confusion pattern: a background statistic from the introduction is cited as if Azevedo_2020 produced this figure. The original source of the 30% prevalence estimate is not identified.

**Recommendation**: Add a qualifier such as "according to estimates cited by" or trace the 30% figure to its primary source.

---

### [F-FID-04] Deng_2023 "n=59" does not appear in the abstract — minor

**Detail**: The review states "multisite injection produced lower early pain scores (VAS 3.1 versus 4.3 at 4 weeks) and better early function (n=59) [@Deng_2023]". The Deng_2023 abstract describes 64 patients randomised, with 30 and 29 analysed (n=59 analysed). The number 59 is not stated explicitly in the abstract; it is a derived value (30+29). The VAS scores 3.1 and 4.3 are correctly present in the abstract.

**Recommendation**: Consider reporting "n=64 randomised, 59 analysed" for precision, or simply "n=64" to match the abstract.

---

### [F-FID-05] Beard_2018 numbers use period decimal, abstract uses middle dot — minor

**Detail**: The review reports "mean Oxford Shoulder Score difference 2.8-4.2 points" for Beard_2018. The abstract uses Unicode middle dots: "2·8 points" and "4·2". The numbers are correct but the automated audit flagged them as UNVERIFIED because the character encoding differs (`.` vs `·`). This is a tooling artefact rather than a fidelity error.

**Recommendation**: No content change needed. The audit tool's string matching should handle Unicode middle dot variants.

---

### [F-FID-06] Pang_2023 "13 RCTs" and Surace_2020 "32 trials" spelled out in abstracts — minor

**Detail**: The review cites "A meta-analysis of 13 RCTs (n=725)" for Pang_2023 and "32 trials (2,281 participants)" for Surace_2020. Both abstracts spell out these numbers: "Thirteen nonsurgical randomized controlled trials" (Pang) and "Thirty-two trials (2281 participants)" (Surace). The numbers are correct but were flagged as UNVERIFIED because the audit tool searched for digit forms only. The value 725 is present as a digit in the Pang abstract; 2,281/2281 is present in the Surace abstract.

**Recommendation**: No content change needed. This is an audit tool limitation (digit-only matching).

---

### [F-FID-07] Raeesi_2023 spurious audit entry — minor

**Detail**: The automated audit contains an UNVERIFIED entry for Raeesi_2023 with value "p               ." (a `p` followed by whitespace and a period). This is a regex extraction artefact, not a real claim. It appears to be a fragment of a p-value that was not properly parsed.

**Recommendation**: Ignore. The audit tool's regex pattern for statistical values should be tightened to avoid extracting whitespace-padded fragments.

---

### [F-FID-08] Orphan BibTeX entry: Sari_2020 — minor

**Detail**: The key `Sari_2020` is present in `references.bib` but is never cited in the review prose (it appears only inside the embedded BibTeX code block, not as a `@Sari_2020` citation). The article (Sari & Eroglu, 2020, comparison of US-guided PRP, prolotherapy, and corticosteroid injection) is thematically relevant to the CSI-vs-PRP comparison but was not referenced in the synthesis.

**Recommendation**: Either cite Sari_2020 in the appropriate section (CSI vs PRP) or remove it from the bibliography.

---

### [F-FID-09] Semantic duplicates: short-term CSI efficacy stated redundantly across sources — minor

**Detail**: At least 26 semantic claims across different articles state essentially the same finding: "CSI provides short-term pain relief but not long-term benefit." Examples:

- Hopewell_2021b: "Subacromial corticosteroid injection improved shoulder pain and function, but provided only modest short-term benefit."
- Xiao_2017: "Corticosteroid injections for AC demonstrate short-term efficacy, but may not provide a long-term benefit."
- Wang_2017: "Intra-articular corticosteroid injections were more effective in pain relief in the short term, but this pain relief did not sustain in the long term."
- Coombes_2010: "Despite the effectiveness of corticosteroid injections in the short term, non-corticosteroid injections might be of benefit for long-term treatment."

The review synthesis already handles this well by presenting it as convergent evidence. No corrective action needed, but this convergence could be explicitly quantified (e.g., "This finding is echoed across N independent studies").

**Recommendation**: Consider adding a statement quantifying the degree of convergence for the short-term efficacy finding.

---

### [F-FID-10] Grey literature gap: no French institutional guidelines or HAS recommendations — major

**Detail**: The protocol specifies "French data prioritized in synthesis" and the review is conducted for the PRISE protocol at CHU de Lille. However, the review corpus contains no references to French institutional guidelines from the Haute Autorite de Sante (HAS), SOFCOT (Societe Francaise de Chirurgie Orthopedique et Traumatologique), or other French professional bodies. For a topic as common as subacromial CSI for shoulder pain, HAS recommendations on care pathways and the place of infiltration would be expected as landmark references.

Similarly, no occupational health body reports (e.g., INRS for occupational shoulder pathology) are present despite shoulder pain being a leading occupational musculoskeletal disorder.

**Recommendation**: Search for HAS recommendations on shoulder pain management and infiltration therapy. Search for SOFCOT or SFR (Societe Francaise de Rhumatologie) position statements. Include INRS documentation if the occupational dimension is relevant to the PRISE protocol.

---

### [F-FID-11] Causal language "leads to" in Roddy_2021 semantic claim from an RCT — minor

**Detail**: A semantic claim from Roddy_2021 states: "In patients with SAPS, physiotherapist-led exercise leads to greater improvements in pain and function than an exercise leaflet." Roddy_2021 is a factorial RCT, so the causal framing is acceptable for the exercise comparison. However, the claim uses stronger causal language ("leads to") than the abstract's own phrasing. This is a minor overinterpretation of the extraction.

**Recommendation**: No action required for the review text (this claim is not used verbatim in the synthesis). Note for extraction quality: prefer mirroring the source's own hedging.

---

### [F-FID-12] Causal language "leads to" in Zufferey_2012 from a controlled trial — minor

**Detail**: A semantic claim from Zufferey_2012 states: "Local steroid injection for shoulder pain leads to significant improvements in pain and function for up to 12 weeks." Zufferey_2012 is a controlled (non-randomised) trial of 70 patients comparing US-guided vs standard injection. The claim generalises about "local steroid injection" without a comparator, and uses causal language. The controlled design partially supports causal inference, but the claim is broader than the study's actual comparison.

**Recommendation**: No action required for the review text (not used verbatim). Flag as extraction-level imprecision.

---

### [F-FID-13] 10 articles with zero claims due to missing abstracts — minor

**Detail**: 10 articles were included in the review but have no extracted claims (quantitative or semantic) because their abstracts were not available. These include articles with incomplete author keys (`M._2024`, `A._2011`, `A._2019`, `S._2016`, `P._2017`, `P._2013`) suggesting metadata quality issues, plus `Unknown_2010` and `Jason_2016`. These articles contribute nothing to the evidence synthesis but inflate the "358 included" count.

**Recommendation**: Either attempt full-text retrieval for these 10 articles, or note them explicitly as included-but-not-extracted in the PRISMA flow. The current flow diagram shows "Included: n=358" which overstates the extractable evidence base (348 with claims).

---

## Walkthrough Decisions

All findings NOTED (validation run — no fixes applied). Findings recorded as skill diagnostics in pipeline_log.md.

| Finding | Severity | Decision | Rationale |
|---------|----------|----------|-----------|
| F-FID-02 | Major | NOTED | Synthesis conflation — litrev-synthesize improvement target |
| F-FID-10 | Major | NOTED | Grey literature gap — litrev-search structural limitation |
| F-FID-01 | Minor | NOTED | Attribution imprecision — extraction/synthesis boundary |
| F-FID-03 | Minor | NOTED | Context-vs-result confusion — known extraction pattern |
| F-FID-04 | Minor | NOTED | Derived number — minor imprecision |
| F-FID-05 | Minor | NOTED | Unicode tooling artefact |
| F-FID-06 | Minor | NOTED | Spelled-out numbers — tooling artefact |
| F-FID-07 | Minor | NOTED | Regex artefact |
| F-FID-08 | Minor | NOTED | Orphan bib entry — minor cleanup |
| F-FID-09 | Minor | NOTED | Semantic duplicates — not actionable |
| F-FID-11 | Minor | NOTED | Causal language — extraction-level |
| F-FID-12 | Minor | NOTED | Causal language — extraction-level |
| F-FID-13 | Minor | NOTED | No-abstract articles — search/screen boundary |

## Summary table

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 0 | |
| Major | 2 | F-FID-02, F-FID-10 |
| Minor | 11 | F-FID-01, F-FID-03, F-FID-04, F-FID-05, F-FID-06, F-FID-07, F-FID-08, F-FID-09, F-FID-11, F-FID-12, F-FID-13 |
