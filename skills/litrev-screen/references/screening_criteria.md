# Screening Methodology Guide

## Principles

Screening is a sequential filter designed to efficiently narrow a large set of search results to the articles relevant to the research question. The key principle is **sensitivity over specificity**: at each stage, err on the side of inclusion. It is worse to miss a relevant article than to include an irrelevant one (which will be caught later).

## Title Screening

Title screening is the coarsest filter. It removes articles that are clearly irrelevant based on title alone.

### Include if:

- The title mentions any concept from the research question (population, exposure/intervention, outcome)
- The title is ambiguous but could plausibly be relevant
- The title describes a study type matching inclusion criteria (e.g., "systematic review", "meta-analysis", "cohort study")
- The title is in a different language but appears relevant based on available English translation

### Exclude if:

- The title clearly indicates a population outside inclusion criteria (e.g., "pediatric" when adults only, "canine model" when humans only)
- The title clearly indicates a different anatomical site, disease, or intervention with no overlap
- The title indicates an excluded study type (e.g., "case report" when only SR/MA/cohort are included)
- The title indicates an excluded topic (e.g., "in vitro biomechanical analysis" when only clinical studies are included)

### Common pitfalls:

- Do NOT exclude based on journal name alone
- Do NOT exclude because the title seems too broad — the abstract will clarify
- Do NOT exclude non-English titles if the inclusion criteria allow non-English articles or if the topic is the same
- Do NOT exclude studies with partially matching titles — e.g., a study on "shoulder disorders including rotator cuff" is relevant to a rotator cuff review

## Abstract Screening

Abstract screening is more rigorous. Apply all inclusion/exclusion criteria systematically.

### Structured approach:

For each abstract, check in order:
1. **Population**: Does the study population match? (age, condition, setting)
2. **Exposure/Intervention**: Does it address the relevant exposure or intervention?
3. **Outcome**: Does it report relevant outcomes?
4. **Study design**: Is the study design included in criteria? (SR, MA, RCT, cohort, etc.)
5. **Date range**: Is publication year within range? (usually already filtered by search)
6. **Language**: Is the article in an included language?
7. **Sample size**: Does it meet minimum sample size requirements (if any)?

Exclude at the FIRST criterion that fails — do not continue checking.

### Recording decisions:

For each exclusion, record:
- The article index
- The first author and year (for human readability)
- The specific criterion that caused exclusion (not just "irrelevant")

For retained articles, no justification is needed (inclusion is the default).

### Articles without abstracts:

If an article has no abstract available (even after PubMed fetch), retain it by default and flag it for full-text screening. Do not exclude solely for lack of abstract.

## Full-Text Screening

Full-text screening is the most rigorous stage. It applies when:
- The review type requires it (systematic, meta-analysis)
- Articles had no abstract
- The user explicitly requests it

At this stage, all criteria must be met for inclusion. Borderline cases that survived abstract screening may be excluded here with more specific justifications.

### Additional exclusion reasons at full-text:

- Duplicate publication (same cohort reported in multiple papers — keep the most complete)
- Insufficient methodological detail
- Outcomes not reported in a usable format (for meta-analysis)
- Study overlaps with a more comprehensive included study

## PRISMA Documentation

At each stage, maintain exact counts:
- Pool size entering the stage
- Number retained
- Number excluded (with reasons grouped by category)

The counts must be arithmetically consistent. At title and full-text stages: retained + excluded = pool. At abstract stage: retained + excluded + no abstract = pool (no-abstract articles are listed in a separate `### No Abstract` section and proceed to full-text screening). If they don't add up, there is an error in the screening process that must be resolved before proceeding.

## Disagreements and Difficult Cases

In a solo screening context (single reviewer, which is typical for this skill), difficult cases should be:
1. Flagged in the screening log with a note explaining the uncertainty
2. Included by default (sensitivity principle)
3. Discussed with the user if the number of borderline cases is large (>10% of the pool)
