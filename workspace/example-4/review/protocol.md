# Protocol — Prediction Models for Postoperative Delirium in Older Surgical Patients

## Research Question

What prediction models and risk scores for postoperative delirium exist for older surgical patients (≥65 years, non-cardiac surgery), how do they perform (discrimination, calibration), which risk factors do they incorporate, and can routine hospital data (EHR) improve prediction compared to dedicated clinical assessment?

## Framework: PICO

| Component | Definition |
|-----------|------------|
| **Population** | Adults ≥65 years, scheduled non-cardiac surgery |
| **Intervention** | Prediction models/scores for postoperative delirium (clinical scores, ML models, EHR-derived models) |
| **Comparator** | Clinical judgment alone, no screening, or head-to-head model comparison |
| **Outcomes** | (1) Discrimination (AUC/c-statistic), calibration; (2) Identified risk factors (age, comorbidities, polypharmacy, frailty, biomarkers); (3) Impact on early detection and length of stay |

## Review Type

Scoping review (PRISMA-ScR)

## Scope

- **Time period**: 2015–2026
- **Languages**: English, French
- **Geographic scope**: International (no restriction)

## Inclusion Criteria

- Adults ≥65 years undergoing elective non-cardiac surgery
- Studies developing, validating, or comparing a prediction model or risk score for postoperative delirium
- Reports discrimination metrics (AUC, c-statistic) or identifies risk factors
- Published 2015–2026
- English or French language

## Exclusion Criteria

- Pediatric populations
- Cardiac surgery
- ICU delirium (non-postoperative context)
- Delirium tremens (alcohol withdrawal)
- Case reports, editorials, conference abstracts without full data
- Animal studies

## Databases

- PubMed/MEDLINE
- Semantic Scholar
- OpenAlex

## Search Strategy

### Key Concepts and Synonyms

| Concept | Terms |
|---------|-------|
| **Delirium** | delirium, postoperative delirium, POD, postoperative cognitive dysfunction, acute confusion |
| **Prediction** | prediction model, predictive model, risk score, risk prediction, prognostic model, machine learning, clinical decision support, screening tool, nomogram, risk stratification |
| **Elderly surgery** | elderly, older adults, aged, geriatric, surgical patients, elective surgery, non-cardiac surgery |
| **EHR/routine data** | electronic health record, EHR, routine data, administrative data, clinical data warehouse, health information system |

### Boolean Strategy

(delirium OR "postoperative delirium" OR POD OR "acute confusion") AND ("prediction model" OR "risk score" OR "machine learning" OR "prognostic model" OR nomogram OR "risk stratification" OR "predictive model") AND (elderly OR "older adults" OR aged OR geriatric OR "surgical patients" OR "elective surgery")

EHR-specific queries run separately to capture data-source-focused studies:
(delirium OR "postoperative delirium") AND ("electronic health record" OR EHR OR "routine data" OR "administrative data" OR "clinical data warehouse") AND (prediction OR predictive OR "risk score")
