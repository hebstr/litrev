---
title: "Literature Review title"
subtitle: "Topic"
date: today
format:
  html:
    toc: true
    toc-depth: 3
    number-sections: true
bibliography: references.bib
csl: vancouver.csl  # user may substitute any .csl style
---

**Review Type**: [Narrative / Systematic / Scoping / Meta-Analysis]
**PRISMA Compliance**: [Yes/No/Partial - specify which guidelines]

# Abstract {-}

**Background**: [Context and rationale]
**Objectives**: [Primary and secondary objectives]
**Methods**: [Databases, dates, selection criteria, quality assessment]
**Results**: [n studies included; key findings by theme]
**Conclusions**: [Main conclusions and implications]
**Keywords**: [5-8 keywords]

# Introduction

## Background and Context

[Provide background information on the topic. Establish why this literature review is important and timely. Discuss the broader context and current state of knowledge.]

## Scope and Objectives

[Clearly define the scope of the review and state the specific objectives. What questions will this review address?]

**Primary Research Questions:**
1. [Research question 1]
2. [Research question 2]
3. [Research question 3]

## Significance

[Explain the significance of this review. Why is it important to synthesize this literature now? What gaps does it fill?]

# Methodology

## Protocol

**Deviations**: [Document any protocol deviations]
**PRISMA**: [Checklist in Appendix B]

## Search Strategy

**Databases:** [PubMed, Scopus, EMBASE, Web of Science, Cochrane CENTRAL, medRxiv, etc.]
**Supplementary:** [Citation chaining, grey literature, trial registries]

**Search String Example:**
```
[Replace with actual PubMed search string from search_results.md]
```

**Dates:** [YYYY-MM-DD to YYYY-MM-DD]
**Validation:** [Key papers used to test search strategy]

## Tools and Software

**Screening:** [Rayyan, Covidence, ASReview]
**Analysis:** [VOSviewer, R, Python]
**Citation Management:** [Zotero, Mendeley, EndNote]
**AI Tools:** [Any AI-assisted tools used; document validation approach]

## Inclusion and Exclusion Criteria

**Inclusion Criteria:**
- [Criterion 1: e.g., Published between 2017-2026]
- [Criterion 2: e.g., Peer-reviewed articles and preprints]
- [Criterion 3: e.g., English language]
- [Criterion 4: e.g., Human or animal studies]
- [Criterion 5: e.g., Original research or systematic reviews]

**Exclusion Criteria:**
- [Criterion 1: e.g., Case reports with n<5]
- [Criterion 2: e.g., Conference abstracts without full text]
- [Criterion 3: e.g., Editorials and commentaries]
- [Criterion 4: e.g., Duplicate publications]
- [Criterion 5: e.g., Retracted articles]
- [Criterion 6: e.g., Studies with unavailable full text after author contact]

## Study Selection

**Reviewers:** [n independent reviewers] | **Conflict resolution:** [Method]
**Inter-rater reliability:** [Cohen's kappa = X]

**PRISMA Flow:**
```
Records identified: n=[X] → Deduplicated: n=[Y] →
Title/abstract screened: n=[Y] → Full-text assessed: n=[Z] → Included: n=[N]
```

**Exclusion reasons:** [List with counts]

## Data Extraction

**Method:** [Standardized form (Appendix E); pilot-tested on n studies]
**Extractors:** [n independent] | **Verification:** [Double-checked]

**Items:** Study ID, design, population, interventions/exposures, outcomes, statistics, funding, COI, bias domains

**Missing data:** [Author contact protocol]

## Quality Assessment

**Tool:** [Cochrane RoB 2.0 / ROBINS-I / Newcastle-Ottawa / AMSTAR 2 / QUADAS-2]
**Method:** [2 independent reviewers; third for conflicts]
**Rating:** [Low/Moderate/High risk of bias]
**Publication bias:** [Funnel plots, Egger's test - if meta-analysis]

## Synthesis and Analysis

**Approach:** [Narrative / Meta-analysis / Both]
**Statistics** (if meta-analysis): Effect measures, heterogeneity (I², τ²), sensitivity analyses, subgroups
**Software:** [RevMan, R, Stata]
**Certainty:** [GRADE framework; factors: bias, inconsistency, indirectness, imprecision]

# Results

## Study Selection

**Summary:** [X records → Y deduplicated → Z full-text → N included (M in meta-analysis)]
**Study types:** [RCTs: n=X, Observational: n=Y, Reviews: n=Z]
**Years:** [Range; peak year]
**Geography:** [Countries represented]
**Source:** [Peer-reviewed: n=X, Preprints: n=Y]

<!-- Bibliometric Overview: OMIT this section unless the user specifically performed bibliometric analysis (e.g., VOSviewer, bibliometrix). Delete this entire block if not applicable. -->

## Bibliometric Overview

[Optional: Trends, journal distribution, author networks, citations, keywords - if analyzed with VOSviewer or similar]

## Study Characteristics

| Study | Year | Design | Sample Size | Main Findings | Quality |
|-------|------|--------|-------------|---------------|---------|
| First Author et al. | 2023 | [Type] | n=[X] | [Brief findings] | [Low/Mod/High RoB] |

**Quality:** Low RoB: n=X ([%]); Moderate: n=Y ([%]); High: n=Z ([%])

## Thematic Synthesis

[Organize by themes, NOT study-by-study. Synthesize across studies to identify consensus, controversies, and gaps.]

### Theme 1: [Title]

**Findings:** [Synthesis of key findings from multiple studies]
**Supporting studies:** [X, Y, Z]
**Contradictory evidence:** [If any]
<!-- Certainty: INCLUDE only for systematic reviews and meta-analyses. OMIT for scoping, narrative, and rapid reviews (no per-theme GRADE ratings). -->
**Certainty:** [GRADE rating]

## Methodological Approaches

**Common methods:** [Method 1 (n studies), Method 2 (n studies)]
**Emerging techniques:** [New approaches observed]
**Methodological quality:** [Overall assessment]

<!-- Meta-Analysis Results: INCLUDE only for meta-analysis reviews. OMIT entire section for all other review types. -->

## Meta-Analysis Results

[Include only if conducting meta-analysis]

**Effect estimates:** [Primary/secondary outcomes with 95% CI, p-values]
**Heterogeneity:** [I²=X%, τ²=Y, interpretation]
**Subgroups & sensitivity:** [Key findings from analyses]
**Publication bias:** [Funnel plot, Egger's p=X]
**Forest plots:** [Include for primary outcomes]

<!-- GRADE Summary of Findings: INCLUDE only for systematic reviews and meta-analyses. OMIT entire section for scoping, narrative, and rapid reviews. -->

## GRADE Summary of Findings

| Outcome | Studies (n) | Effect (95% CI) | Certainty | Downgrade reasons |
|---------|-------------|------------------|-----------|-------------------|
| [Primary] | n=X | RR/OR/MD [95% CI] | ⊕⊕⊕⊕ High / ⊕⊕⊕◯ Moderate / ⊕⊕◯◯ Low / ⊕◯◯◯ Very low | [Risk of bias, inconsistency, indirectness, imprecision, publication bias] |
| [Secondary] | n=X | RR/OR/MD [95% CI] | [Rating] | [Reasons] |

## Knowledge Gaps

**Knowledge:** [Unanswered research questions]
**Methodological:** [Study design/measurement issues]
**Translational:** [Research-to-practice gaps]
**Populations:** [Underrepresented groups/contexts]

# Discussion

## Main Findings

[Synthesize key findings by research question]

**Principal findings:** [Top 3-5 takeaways]
**Consensus:** [Where studies agree]
**Controversy:** [Conflicting results]

## Interpretation and Implications

**Context:** [How findings advance/challenge current understanding]
**Mechanisms:** [Potential explanations for observed patterns]

**Implications for:**
- **Practice:** [Actionable recommendations]
- **Policy:** [If relevant]
- **Research:** [Theoretical, methodological, priority directions]

## Strengths and Limitations

**Strengths:** [Comprehensive search, rigorous methods, large evidence base, transparency]

**Limitations:**
- Search/selection: [Language bias, database coverage, grey literature, publication bias]
- Methodological: [Heterogeneity, study quality]
- Temporal: [Rapid evolution, search cutoff date]

**Impact:** [How limitations affect conclusions]

## Comparison with Previous Reviews

[If relevant: How does this review update/differ from prior reviews?]

## Future Research

**Priority questions:**
1. [Question] - Rationale, suggested approach, expected impact
2. [Question] - Rationale, suggested approach, expected impact
3. [Question] - Rationale, suggested approach, expected impact

**Recommendations:** [Methodological improvements, understudied populations, emerging technologies]

# Conclusions

[Concise conclusions addressing research questions]

1. [Conclusion directly addressing primary research question]
2. [Key finding conclusion]
3. [Gap/future direction conclusion]

**Evidence certainty:** [High/Moderate/Low/Very Low]
**Translation readiness:** [Ready / Needs more research / Preliminary]

# Declarations

## Author Contributions
[CRediT taxonomy: Author 1 - Conceptualization, Methodology, Writing; Author 2 - Analysis, Review; etc.]

## Funding
[Grant details with numbers] OR [No funding received]

## Conflicts of Interest
[Author-specific declarations] OR [None]

## Data Availability
**Data/Code:** [Repository URL/DOI or "Available upon request"]
**Materials:** [Search strategies (Appendix A), PRISMA checklist (Appendix B), extraction form (Appendix E)]

## Acknowledgments
[Contributors not meeting authorship criteria, librarians, patient involvement]

# References

<!-- BibTeX block below is a working reference for cross-verification.
     The authoritative .bib file is generated by MCP generate_bibliography in Phase 6 -->

```bibtex
@article{AuthorLastName_Year,
  author  = {LastName, FirstName and LastName, FirstName},
  title   = {Article title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {1},
  number  = {1},
  pages   = {1--10},
  doi     = {10.xxxx/yyyy},
  pmid    = {12345678}
}
```

# Appendices

## Appendix A: Search Strings

**PubMed** (Date: YYYY-MM-DD; Results: n)
```
[Complete search string with operators and MeSH terms]
```

[Repeat for each database: Scopus, EMBASE, Web of Science, Cochrane CENTRAL, medRxiv, etc.]

## Appendix B: PRISMA Checklist

| Section | Item | Reported? | Page |
|---------|------|-----------|------|
| Title | Identify as systematic review | Yes/No | # |
| Abstract | Structured summary | Yes/No | # |
| Methods | Eligibility, sources, search, selection, data, quality | Yes/No | # |
| Results | Selection, characteristics, risk of bias, syntheses | Yes/No | # |
| Discussion | Interpretation, limitations, conclusions | Yes/No | # |
| Other | Support, conflicts, availability | Yes/No | # |

## Appendix C: Excluded Studies

| Study | Year | Reason | Category |
|-------|------|--------|----------|
| Author et al. | Year | [Reason] | [Wrong population/outcome/design/etc.] |

**Summary:** Wrong population (n=X), Wrong outcome (n=Y), etc.

## Appendix D: Quality Assessment

**Tool:** [Cochrane RoB 2.0 / ROBINS-I / Newcastle-Ottawa / etc.]

| Study | Domain 1 | Domain 2 | Domain 3 | Overall |
|-------|----------|----------|----------|---------|
| Study 1 | Low | Low | Some concerns | Low |
| Study 2 | [Score] | [Score] | [Score] | [Overall] |

## Appendix E: Data Extraction Form

```
STUDY: Author______ Year______ DOI______
DESIGN: □RCT □Cohort □Case-Control □Cross-sectional □Other______
POPULATION: n=_____ Age_____ Setting_____
INTERVENTION/EXPOSURE: _____
OUTCOMES: Primary_____ Secondary_____
RESULTS: Effect size_____ 95%CI_____ p=_____
QUALITY: □Low □Moderate □High RoB
FUNDING/COI: _____
```

## Appendix F: Meta-Analysis Details

[Only if meta-analysis performed]

**Software:** [R 4.x.x with meta/metafor packages / RevMan / Stata]
**Model:** [Random-effects; justification]
**Code:** [Link to repository]
**Sensitivity analyses:** [Details]

## Appendix G: Author Contacts

| Study | Contact Date | Response | Data Received |
|-------|--------------|----------|---------------|
| Author et al. | YYYY-MM-DD | Yes/No | Yes/No/Partial |

# Supplementary Materials

[If applicable]

**Tables:** S1 (Full study characteristics), S2 (Quality scores), S3 (Subgroups), S4 (Sensitivity)
**Figures:** S1 (PRISMA diagram), S2 (Risk of bias), S3 (Funnel plot), S4 (Forest plots), S5 (Networks)
**Data:** S1 (Extraction file), S2 (Search results), S3 (Analysis code), S4 (PRISMA checklist)
**Repository:** [OSF/GitHub/Zenodo URL with DOI]

# Review Metadata

**Search dates:** Initial: [Date]; Updated: [Date]
**Version:** [1.0] | **Last updated:** [Date]

**Quality checks:**
- [ ] Citations verified (Phase 6 MCP tools)
- [ ] PRISMA checklist completed
- [ ] Search reproducible
- [ ] Independent data verification
- [ ] Code peer-reviewed
- [ ] All authors approved
