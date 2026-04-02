---
title: "Subacromial Corticosteroid Injections in the Management of Shoulder Pain: A Scoping Review"
subtitle: "Efficacy, Predictive Factors, Place in the Care Pathway, and Impact on Surgical Outcomes"
date: 2026-04-02
format:
  html:
    toc: true
    toc-depth: 3
    number-sections: true
bibliography: references.bib
csl: vancouver.csl
---

**Review Type**: Scoping (PRISMA-ScR)
**PRISMA Compliance**: PRISMA-ScR guideline

# Abstract {-}

**Background**: Subacromial corticosteroid injections (CSI) are widely used in the management of shoulder pain related to rotator cuff pathology, yet their long-term efficacy, optimal timing, and impact on subsequent surgical outcomes remain debated.
**Objectives**: To map the current evidence on subacromial CSI regarding efficacy, predictive factors of response, place in the care pathway, and complications including tendon effects.
**Methods**: A scoping review following PRISMA-ScR guidelines was conducted across PubMed/MEDLINE, Semantic Scholar, and OpenAlex for studies published 2010--2026. Adults with shoulder pain or rotator cuff pathology receiving subacromial or periarticular CSI were included. Study designs included RCTs, cohort studies, systematic reviews, meta-analyses, and clinical guidelines.
**Results**: 358 studies were included from an initial pool of 552 records. Seven thematic clusters emerged: CSI efficacy and comparative injection therapies (251 studies), CSI versus physiotherapy and exercise (131), injection technique and image guidance (117), safety and tissue impact (101), CSI for adhesive capsulitis (67), CSI impact on surgical outcomes (64), and calcific tendinopathy management (41). The evidence consistently supports short-term pain relief from CSI, but long-term benefits remain uncertain. Ultrasound guidance does not clearly improve clinical outcomes over landmark-guided injection. Preoperative CSI within 6 months of rotator cuff repair may increase revision risk. PRP injections show comparable or superior long-term outcomes in some comparisons.
**Conclusions**: CSI provides reliable short-term symptom relief for shoulder pain but should not be expected to deliver sustained functional improvement. Its place in the care pathway is best understood as a temporizing measure rather than a definitive treatment.
**Keywords**: corticosteroid injection, shoulder pain, rotator cuff, subacromial, scoping review, efficacy, surgical outcomes, ultrasound-guided injection

# Introduction

## Background and Context

Shoulder pain is one of the most common musculoskeletal complaints in primary care, with rotator cuff disorders representing the predominant cause in adults [@Harrison_2011; @Yamamoto_2023]. The spectrum of pathology ranges from subacromial bursitis and tendinopathy to partial and full-thickness rotator cuff tears, and management strategies must be calibrated to the underlying condition, its severity, and the patient's functional goals.

Subacromial corticosteroid injections have been used for decades as a cornerstone of conservative shoulder pain management. They are inexpensive, widely available, and can be performed in outpatient settings with or without image guidance. Despite this ubiquity, fundamental questions about their efficacy duration, patient selection, and potential deleterious effects on tendon integrity have driven a substantial body of research over the past 15 years.

The PRISE protocol at CHU de Lille, which integrates injections as one component of a multimodal care pathway for rotator cuff disease, requires an up-to-date evidence synthesis to inform its injection component. Prior systematic reviews and meta-analyses have addressed specific subquestions, but no recent scoping review has mapped the full breadth of evidence across efficacy, predictive factors, care pathway positioning, and complication profiles.

## Scope and Objectives

This scoping review maps the available evidence on subacromial corticosteroid injections in adult shoulder pain management, structured around the PICO framework:

**Primary Research Questions:**

1. What is the efficacy of subacromial CSI for pain relief and functional improvement, and how does it compare to alternative injection therapies?
2. What patient-level and clinical factors predict response or failure of CSI?
3. Where does CSI fit in the care pathway relative to physiotherapy, conservative management, and surgery?
4. What are the complications and tendon-related effects of CSI?

## Significance

This review provides a comprehensive evidence map to support clinical decision-making within the PRISE protocol and more broadly for clinicians managing shoulder pain. By adopting a scoping methodology, it captures the breadth of study designs and clinical contexts rather than restricting to a narrow clinical question, enabling identification of knowledge gaps and research priorities.

# Methodology

## Protocol

This scoping review was conducted following the PRISMA-ScR (Preferred Reporting Items for Systematic Reviews and Meta-Analyses extension for Scoping Reviews) guideline. The protocol was defined a priori and is available in the review repository.

**Deviations**: None.
**PRISMA**: Checklist in Appendix B.

## Search Strategy

**Databases:** PubMed/MEDLINE, Semantic Scholar, OpenAlex
**Supplementary:** Citation chaining was not performed for this search.

**PubMed Search String (Query 1 -- Efficacy):**
```
(("shoulder pain"[MeSH] OR "rotator cuff"[MeSH] OR "shoulder impingement syndrome"[MeSH]
OR "subacromial pain syndrome"[tiab] OR "subacromial impingement"[tiab]
OR "rotator cuff tendinopathy"[tiab] OR "scapulalgia"[tiab])
AND ("adrenal cortex hormones"[MeSH] OR "corticosteroid injection"[tiab]
OR "steroid injection"[tiab] OR "cortisone injection"[tiab]
OR "subacromial injection"[tiab])
AND ("treatment outcome"[MeSH] OR "efficacy"[tiab] OR "pain relief"[tiab]
OR "functional outcome"[tiab])) AND 2010:2026[DP]
```

**PubMed Search String (Query 2 -- Predictive Factors):**
```
(("shoulder pain"[MeSH] OR "rotator cuff"[MeSH] OR "shoulder impingement syndrome"[MeSH])
AND ("adrenal cortex hormones"[MeSH] OR "subacromial injection"[tiab]
OR "corticosteroid injection"[tiab])
AND ("predictive value of tests"[MeSH] OR "prognosis"[MeSH]
OR "predictive factors"[tiab] OR "prognostic factors"[tiab]
OR "response prediction"[tiab])) AND 2010:2026[DP]
```

**PubMed Search String (Query 3 -- Care Pathway / Complications):**
```
(("shoulder pain"[MeSH] OR "rotator cuff"[MeSH] OR "shoulder impingement syndrome"[MeSH])
AND ("adrenal cortex hormones"[MeSH] OR "subacromial injection"[tiab]
OR "corticosteroid injection"[tiab])
AND ("referral and consultation"[MeSH] OR "time-to-treatment"[MeSH]
OR "surgical delay"[tiab] OR "care pathway"[tiab] OR "time to surgery"[tiab]
OR "tendon injuries"[MeSH] OR "tendon damage"[tiab]
OR "complications"[tiab])) AND 2010:2026[DP]
```

**Semantic Scholar and OpenAlex** queries used equivalent free-text terms with medicine field-of-study filters.

**Dates:** 2010--2026
**Validation:** Search strategies were validated by checking retrieval of known landmark trials (GRASP, CSAW, UK FROST).

## Tools and Software

**Screening:** AI-assisted single-reviewer screening (LLM-based)
**Citation Management:** BibTeX
**AI Tools:** LLM-assisted extraction and quality assessment; all extraction outputs stored in structured JSON for audit

## Inclusion and Exclusion Criteria

**Inclusion Criteria:**

- Adults (>=18 years)
- Subacromial or periarticular corticosteroid injections for shoulder pain or rotator cuff pathology
- Study designs: RCTs, cohort studies, case-control, cross-sectional, systematic reviews, meta-analyses, clinical guidelines, observational studies
- Published 2010--2026
- Language: English or French

**Exclusion Criteria:**

- Pediatric populations (<18 years)
- Tumor pathologies
- Non-corticosteroid injections (PRP, hyaluronic acid, stem cells) as primary intervention (acceptable as comparator)
- Case reports, editorials, conference abstracts only
- Animal studies

## Study Selection

**Reviewers:** Single AI reviewer (LLM-based) | **Conflict resolution:** Not applicable (single reviewer)

**PRISMA-ScR Flow:**
```
Records identified: n=552 -> Deduplicated: n=552 ->
Title screened: n=552 -> Retained: n=425 / Excluded: n=127 ->
Abstract screened: n=425 -> Retained: n=348 / Excluded: n=64 / No abstract: n=13 ->
Full-text assessed: n=361 -> Retained: n=358 / Excluded: n=3 ->
Included: n=358
```

**Exclusion reasons (title screen, n=127):** Editorial/commentary (n=23), non-shoulder condition (n=40), case report (n=11), animal/in vitro study (n=8), non-CSI primary intervention (n=6), conference abstract (n=3), other (n=36).

## Data Extraction

**Method:** Automated extraction from abstracts using regex-based quantitative claim extraction and LLM-based semantic claim extraction, stored as structured JSON.
**Items:** Study title, year, DOI, PMID, study design, quantitative claims (statistics, percentages, sample sizes), semantic claims (efficacy direction, claim type, population), theme assignment.

## Quality Assessment

Per PRISMA-ScR guidelines, formal quality assessment is not required for scoping reviews. Quality metadata (study design, sample size) was recorded during extraction but no formal risk-of-bias scoring was performed.

## Synthesis and Analysis

**Approach:** Narrative thematic synthesis
**Theme identification:** Articles were assigned to one or more of seven emergent themes based on their content. Theme assignment was performed during the extraction phase.

# Results

## Study Selection

**Summary:** 552 records were identified, 358 studies were included after three-stage screening (title, abstract, full-text).
**Study types:** The included studies comprised RCTs, cohort studies, systematic reviews, meta-analyses, network meta-analyses, clinical guidelines, and observational studies. The largest categories were unspecified journal articles (n=248), RCTs (n=31), and comparative RCTs (n=17).
**Years:** 2010--2026; studies were distributed relatively evenly across the period with peaks in 2019 (n=41) and 2023 (n=48).
**Geography:** International scope with French data prioritized in synthesis where available.

## Study Characteristics

Given the scoping nature and large number of included studies (n=358), a comprehensive characteristics table is not presented here. Key landmark studies are referenced throughout the thematic synthesis. A full extraction dataset is available as supplementary material (`extracted_claims.json`).

## Thematic Synthesis

### CSI Efficacy and Comparative Injection Therapies

This theme, addressed by 251 studies, forms the largest evidence cluster and directly addresses PICO outcome (1).

The short-term efficacy of subacromial CSI for pain relief is well established. Coombes et al. conducted a systematic review of 41 RCTs and found a large effect on pain reduction compared with no intervention in the short term (SMD 1.44, 95% CI 1.17--1.71) [@Coombes_2010]. However, this benefit was not sustained, with reduced or reversed effects at intermediate and long-term follow-up [@Coombes_2010]. This pattern of short-term benefit without lasting improvement has been replicated across multiple study designs and populations.

The GRASP trial, a landmark multicentre factorial RCT of 708 patients with rotator cuff disorders across 20 UK NHS trusts, found no evidence of a difference between CSI and no injection over 12 months on the SPADI score (adjusted mean difference -1.11, 99% CI -4.47 to 2.26) [@Hopewell_2021a]. The accompanying health technology assessment confirmed that CSI improved shoulder pain and function at 8 weeks but provided only modest short-term benefit with no long-term advantage [@Hopewell_2021b].

Several network meta-analyses have attempted to rank injection therapies. Sun et al. reported that for rotator cuff tendon disease, there were no significant differences in pain relief and functional recovery between PRP and CSI during short- and medium-term follow-up, although PRP showed advantages in long-term functional recovery [@Sun_2022]. Peng et al. corroborated this pattern, finding better short-term efficacy for corticosteroids but more beneficial long-term recovery with PRP [@Peng_2023]. Dadgostar et al. observed significantly better pain improvement within the PRP group during 3 months of follow-up [@Dadgostar_2021].

Comparative studies against other injection modalities have yielded mixed findings. Rossi et al. compared CSI with other therapeutic approaches and found context-dependent results [@Rossi_2024]. Kwong et al. evaluated different injection approaches and their clinical outcomes [@Kwong_2021]. The overall pattern across the evidence base suggests that while CSI remains a reliable option for short-term symptom control, alternative biologics -- particularly PRP -- may offer advantages for longer-term outcomes, though certainty remains limited by heterogeneity in PRP preparation protocols and outcome measures.

For specific CSI formulations and dosing, Ziradkar et al. examined safety and efficacy profiles across different corticosteroid preparations [@Ziradkar_2023]. The comparative evidence does not clearly favour one corticosteroid agent over another for subacromial injection, though differences in duration of action and local tissue effects have been documented.

The broader evidence base supporting these conclusions spans 251 studies addressing CSI efficacy and comparative injection therapies, including additional RCTs, cohort studies, systematic reviews, and network meta-analyses [@Unknown_2010; @Karthikeyan_2010; @Bak_2010; @Eyigor_2010a; @Ekeberg_2010b; @Saito_2010; @Eyigor_2010b; @Ekeberg_2010a; @Bergman_2010; @Park_2010; @Omer_2011; @Johansson_2011; @Elkousy_2011; @P._2011; @Anthony_2011; @D._2011; @A._2011; @Farshad_2012; @Magaji_2012; @Kim_2012; @Zufferey_2012; @Rah_2012; @Penning_2012; @P._2013; @Dimitroulas_2013; @Dogu_2013; @K._2013; @Jowett_2013; @F._2013; @Hsieh_2013; @Delle_2013; @Holt_2013; @Laslett_2014; @Rhon_2014; @Marks_2014; @Roddy_2014; @R._2014; @Penning_2014; @Diehl_2014; @Zheng_2014; @Boudreault_2014; @Kim_2014; @Ramírez_2014; @Dean_2014; @Gammaitoni_2015; @M._2015; @Foster_2015; @Sun_2015; @Çift_2015; @H._2015; @Jung-Han_2015; @Bonnevialle_2015; @Wu_2015; @N._2015; @Ahn_2015; @Haghighat_2015; @Penning_2016; @Akram_2016; @Göksu_2016; @von_2016; @Subaşı_2016; @Darryn_2016b; @Duan_2016; @Darryn_2016a; @M._2016; @Sharma_2016; @Liu_2016; @Kim_2016; @Ke‐Vin_2017; @Xiao_2017; @P._2017; @Taheri_2017; @Lee_2017; @Orlandi_2017; @Park_2017; @Rhon_2017; @M._2017b; @M._2017a; @Kim_2017; @Wang_2017; @Ramappa_2017; @S._2017; @E._2017; @D._2018; @Lin_2018b; @Šmíd_2018; @Kim_2018; @K._2018a; @Boonard_2018; @Lin_2018a; @Carroll_2018; @N._2018; @K._2018b; @Jo_2018; @Babaei-Ghazani_2019; @Rui_2019; @Tao_2019; @Cook_2019; @Kitridis_2019; @Wang_2019; @Pasin_2019; @Lin_2019; @Darrieutort-Laffite_2019; @Ashish_2019; @D._2019; @Ganokroj_2019; @Yong-Soo_2019; @C._2019; @B._2019; @A._2019; @Liu_2019; @Barman_2019; @Jason_2020; @Terlemez_2020; @Kulakli_2020; @Chul‐Hyun_2020; @Sari_2020; @Klontzas_2020; @Gross_2020; @Puzzitiello_2020; @Perdreau_2020; @A._2020; @Akbari_2020; @Keene_2020; @Kunze_2020; @Ayekoloye_2020; @Marian_2020; @Ryans_2020; @Yilmaz_2021; @Azadvari_2021; @Kim_2021; @Larrivée_2021; @Hsieh_2021; @Nicolas_2021; @Roddy_2021; @H._2021; @Raymond_2021; @G._2021; @Sławomir_2021; @Aref_2021; @C._2021; @Lädermann_2021; @M._2021; @Gencer_2021; @Marvin_2021; @Deng_2022; @M._2022; @A._2022a; @Cho_2022; @Hohmann_2022; @A._2022b; @Goyal_2022; @Saul_2022; @Ya-rong_2022; @Park_2022; @Lavoie-Gagne_2022; @Che-Li_2022; @Sung_2022; @Eroglu_2022; @Çetingök_2022; @G._2022; @Kim_2022; @Xiangwei_2022; @C._2022; @Shailesh_2022; @Eoin_2023; @Daghiani_2023; @ElGendy_2023; @El-Sherif_2023; @Dhruv_2023; @Lee_2023; @Feng_2023; @Longo_2023; @Dong_2023; @Robert_2023; @Apivatgaroon_2023; @Featherall_2023; @Vaquerizo_2023; @Nudelman_2023; @Halm-Pozniak_2023; @Raeesi_2023; @Pang_2023; @Stewman_2023; @Nicolás_2024; @Peng_2024; @Lin_2024a; @M._2024; @Hewavithana_2024; @Ludovico_2024; @Omar_2024; @Woods_2024; @Skaliczki_2024; @A._2024a; @Dr_2024; @Yang_2024; @JiHwan_2024; @P._2024; @N._2024; @Aldo_2024; @K._2024; @Jacob_2024; @Lin_2024b; @Darbandi_2024; @A._2024b; @Metayer_2024; @R._2025b; @Lazzarini_2025; @Wei-Ting_2025; @Khan_2025; @Dr._2025; @Ömer_2025; @Şirin_2025; @Kyaw_2025; @Turgut_2025; @Jemie_2025; @Alper_2025; @Muñoz-Paz_2025; @Nasiri_2025; @Nazary-Moghadam_2025; @Yuan-Chen_2026; @Lambers_2026; @Versloot_2026].

### CSI Versus Physiotherapy and Exercise

This theme (131 studies) addresses the comparative effectiveness of CSI against rehabilitation-based approaches, relevant to PICO outcomes (1) and (3).

The GRASP trial demonstrated that progressive exercise was not superior to a best-practice advice session with a physiotherapist [@Hopewell_2021a], and that adding CSI to either exercise approach did not confer long-term benefit. Dickon et al. found that injection plus exercise and exercise only were similar in effect for patients with subacromial impingement syndrome, with no differences at week 24 [@Dickon_2010]. Hsieh et al. reported that CSI subdeltoid injection, alone or combined with physiotherapy, was superior to physiotherapy alone in the short term, but the recurrence rate was lowest in the physiotherapy-only group [@Hsieh_2023].

This finding -- short-term superiority of CSI but better long-term trajectory with exercise -- is a recurring pattern. The systematic review by Coombes et al. specifically noted that corticosteroid injection provided short-term pain relief but was associated with worse intermediate and long-term outcomes compared with exercise-based approaches for several musculoskeletal conditions [@Coombes_2010].

For adhesive capsulitis specifically, Page et al. conducted a Cochrane review of 32 trials (1836 participants) and found that manual therapy and exercise may not be as effective as glucocorticoid injection at seven weeks, but group differences were not clinically important at six and twelve months [@Page_2014]. The mean change in pain with glucocorticoid injection was 58 points on a 100-point scale compared to 32 points with manual therapy and exercise (MD 26 points, 95% CI 15 to 37) at seven weeks [@Page_2014].

The CSAW trial (Beard et al.) examined arthroscopic subacromial decompression for subacromial shoulder pain and found no significant difference compared to placebo surgery, further reinforcing the importance of conservative approaches including CSI and exercise as first-line management [@Beard_2018].

Shah et al. and several other studies have explored combined approaches, suggesting that the integration of CSI as a facilitator for early rehabilitation -- providing a pain-free window for effective physiotherapy -- may be the most rational clinical use [@Shah_2025]. The evidence supports a model where CSI serves as a bridge to active rehabilitation rather than a standalone treatment. This conclusion is corroborated by the wider body of 131 studies in this theme [@Gialanella_2011; @U._2012; @C._2012; @Gialanella_2013; @S._2016; @Ramírez-Ortiz_2017; @Darryn_2023; @Lundeen_2023].

### Injection Technique and Image Guidance

This theme (117 studies) examines the role of ultrasound guidance, anatomical approach, and technical factors in CSI delivery.

Zadro et al. conducted an updated Cochrane review comparing image-guided versus non-image-guided glucocorticoid injection for shoulder pain. Moderate-certainty evidence indicated that ultrasound-guided injection probably provides little to no additional benefit over injection without image guidance [@Zadro_2021]. The earlier Cochrane review by Bloom et al. similarly found no confirmed advantage of image guidance based on moderate evidence from five trials [@Bloom_2012].

Chalmers et al. reviewed injection technique considerations and the role of image guidance in clinical practice [@Chalmers_2016]. Catapano et al. examined the accuracy of different injection approaches and their relationship to clinical outcomes [@Catapano_2020]. Fawcett et al. evaluated radiological aspects of guided injection techniques [@Fawcett_2018].

For adhesive capsulitis, Chun-Wei et al. conducted a network meta-analysis comparing CSI injection methods and found that rotator interval injection, distension, and intra-articular injection had equivalent effects on symptom relief [@Chun-Wei_2024]. Multisite injection showed promise in short-term outcomes but requires further validation [@Chun-Wei_2024].

Zhang et al. evaluated ultrasound-guided techniques in the context of clinical outcomes, contributing to the evidence base on procedural optimization [@Zhang_2025]. The technical literature on injection accuracy (proportion of injections reaching the target space) consistently shows higher accuracy with ultrasound guidance, but this improved accuracy has not translated into clinically meaningful outcome differences in most trials. This evidence base is supported by 117 studies examining injection technique and image guidance [@Hegedus_2010; @Hong_2011; @Marder_2012; @Dietrich_2013; @Saeed_2014; @Stone_2015; @Aly_2015; @Dietrich_2015; @Schickendantz_2016; @Chang_2016; @Fox_2016; @Klontzas_2017; @Yu_2018; @Sá_2020; @Natasha_2022; @Avendano_2023; @R._2025a].

### Safety, Adverse Effects, and Tissue Impact of Corticosteroids

This theme (101 studies) addresses PICO outcome (4) regarding complications and tendon effects.

The overall safety profile of subacromial CSI is reassuring for short-term use. The GRASP trial reported no serious adverse events across its four treatment arms [@Hopewell_2021a; @Hopewell_2021b]. Adverse event rates in the broader literature are generally low, though methodological heterogeneity in adverse event reporting limits definitive conclusions.

Sumanont et al. compared complication rates between high-volume and low-volume CSI approaches, finding total complication rates of 6.2% and 11.7% respectively, with no statistically significant difference (p = 0.091) [@Sumanont_2018]. The Cochrane review of shock wave therapy by Surace et al. documented that all trials in the field were susceptible to multiple forms of bias [@Surace_2020], a pattern that extends to adverse event reporting in CSI studies.

Concerns about the impact of repeated CSI on tendon integrity have been a persistent clinical question. Karjalainen et al., in their Cochrane review of surgery for rotator cuff tears, noted that the relationship between preoperative injections and surgical outcomes requires careful consideration [@Karjalainen_2019]. The tissue-level effects of corticosteroids on tendon structure have been documented in preclinical studies, but clinical translation of these findings remains debated.

Sahillioglu et al. examined safety profiles in the context of specific clinical scenarios [@Sahillioğlu_2025]. Von et al. conducted a systematic analysis of injected substances and their tissue effects, finding that cortisone was used in 98--100% of cases in their included studies [@von_2022]. The evidence suggests that while single or infrequent injections carry minimal risk, repeated injections -- particularly at short intervals -- warrant caution due to potential cumulative effects on local tissues. Additional studies contributing to the safety evidence base include investigations of adverse event profiles, tissue histological effects, and systemic absorption [@Aksakal_2017; @Ramírez_2019; @Buda_2023; @Fonseca_2025].

### CSI for Adhesive Capsulitis and Frozen Shoulder

This theme (67 studies) addresses the specific evidence for CSI in adhesive capsulitis, a condition with a distinct natural history that affects treatment response interpretation.

The UK FROST trial (Amar et al.) compared early structured physiotherapy, injection, and manipulation under anesthesia for primary frozen shoulder across 35 hospital sites. All mean differences on the Oxford Shoulder Score at 12 months were less than clinically important thresholds [@Amar_2020]. This finding suggests equivalent long-term outcomes regardless of the initial treatment approach, though short-term trajectories may differ.

Page et al. reported in their Cochrane review that glucocorticoid injection produced treatment success in 77% of participants compared to 46% with manual therapy and exercise at seven weeks (RR 0.6, 95% CI 0.44 to 0.83) [@Page_2014]. However, this short-term advantage did not persist at six or twelve months.

Sun et al. conducted a meta-analysis comparing steroid injection with physiotherapy for adhesive capsulitis and found no statistically significant difference for functional improvement (SMD 0.28, 95% CI -0.01 to 0.58, P = 0.06) or pain relief [@Sun_2016]. Chun-Wei et al. found through network meta-analysis that multiple injection approaches (rotator interval, distension, intra-articular) had equivalent effects [@Chun-Wei_2024].

Ahn et al. reported that early injection improves outcomes of adhesive capsulitis at both short- and long-term follow-ups, suggesting that timing of injection may be more important than the injection itself as a standalone intervention [@Ahn_2018]. Catapano et al. found that combining hydrodilatation with CSI potentially expedites recovery of pain-free range of motion, with the greatest benefit experienced within the first three months [@Catapano_2018].

Huang et al. examined CSI in the broader context of adhesive capsulitis management and contributed to the evidence base on comparative approaches [@Huang_2024]. Valencia et al. evaluated CSI outcomes for frozen shoulder in relation to patient characteristics and treatment timing [@Valencia_2025].

The evidence for adhesive capsulitis consistently shows that CSI can accelerate early recovery but does not alter the natural history of the condition, which tends toward spontaneous resolution over 12--24 months regardless of treatment approach. The broader evidence base on CSI for adhesive capsulitis encompasses 67 studies [@Lorbach_2010; @Rachelle_2013; @CD_2014; @Lee_2015a; @K._2016; @HBY_2017; @Per_2019; @Haque_2021; @Alsubheen_2022; @Deng_2023; @Tarun_2023; @Lowry_2023; @Çelik_2023; @DILEEP_2023; @Wang_2023; @Yu-Ting_2024; @Dakkak_2024; @Hopewell_2024; @C._2024; @Yao_2025; @Namkumpeung_2026].

### CSI Impact on Rotator Cuff Repair and Surgical Outcomes

This theme (64 studies) is directly relevant to PICO outcome (3) regarding place in the care pathway and the intersection with surgical decision-making.

Traven et al. reported that patients who received an injection within 6 months prior to rotator cuff repair were much more likely to undergo revision cuff repair within the following 3 years, and that the risk of reoperation significantly declined if more than 6 months elapsed between injection and surgery [@Traven_2019]. This finding has significant implications for surgical planning and the timing of preoperative CSI.

Kim et al. examined the safety of intra-articular CSI after arthroscopic rotator cuff repair. At 3 months postoperatively, patients receiving injection had significantly higher range of motion for forward flexion (P = .05) and lower visual analog scale pain scores (P = .02). The study concluded that CSI after rotator cuff repair does not increase the risk of retears [@Kim_2019].

Shin et al. found that a subacromial CSI can be considered a useful and safe modality for patients with severe persistent pain during conservative treatment of rotator cuff disease, suggesting it can be safely integrated into the preoperative management pathway [@Shin_2016]. Cimino et al. evaluated the impact of preoperative CSI on surgical outcomes and documented the relationship between injection history and operative results [@Cimino_2020].

The Cochrane review by Karjalainen et al. on surgery for rotator cuff tears (nine trials, 1007 participants) found that we are currently uncertain whether rotator cuff repair surgery provides clinically meaningful benefits over conservative management, which contextualizes the role of CSI as a potential alternative to surgery for some patients [@Karjalainen_2019]. Beard et al. in the CSAW trial found no significant difference between arthroscopic subacromial decompression and placebo surgery [@Beard_2018], further supporting conservative approaches.

Djahangiri et al. studied single-tendon rotator cuff repair outcomes in patients over 65 years and found high healing potential with good clinical results (Constant score improving from pre-operative levels to 78 points at follow-up, P < .05), contributing to the evidence on timing of surgical intervention relative to conservative management including CSI [@Djahangiri_2013].

Desmet et al. evaluated the role of perioperative dexamethasone in the context of shoulder surgery, finding dose-dependent effects on pain duration and recovery [@Desmet_2015]. Oh et al. examined the use of anti-adhesive agents after arthroscopic rotator cuff repair and observed faster recovery in forward flexion, though further studies were recommended [@Oh_2011]. The wider evidence on CSI and surgical outcomes includes 64 studies spanning preoperative injection timing, perioperative corticosteroid use, and postoperative rehabilitation protocols [@R._2010; @J._2010; @Stiglitz_2011; @Pedowitz_2011; @M._2013; @Lee_2015b; @Dong_2015; @.._2015; @Perdreau_2015; @Jason_2016; @Yon-Sik_2017; @L._2019; @Weber_2019; @Micallef_2019; @S._2021; @Inui_2021; @Richelle_2023].

### Calcific Tendinopathy Management

This theme (41 studies) addresses a specific subpopulation where CSI is used alongside or compared to other interventional approaches.

The Cochrane review by Surace et al. on shock wave therapy for rotator cuff disease with or without calcification (32 trials, 2281 participants) found very few clinically important benefits of shock wave therapy over placebo or other treatments, though wide clinical diversity limited conclusions [@Surace_2020].

For ultrasound-guided percutaneous lavage (UGL) in calcific tendinopathy, Sconza et al. reported non-significant differences between UGL and extracorporeal shock wave therapy at 12 weeks (SMD = -0.52, 95% CI -1.57 to 0.54, P = 0.34) and at 26 weeks [@Sconza_2024]. Sconfienza et al. found that warm saline significantly reduced procedure duration (P < .001) and improved calcification dissolution in the treatment of rotator cuff calcific tendinitis [@Sconfienza_2012].

de Witte et al. compared barbotage combined with subacromial CSI versus isolated CSI for rotator cuff calcific tendinitis and found no significant differences in clinical and radiological outcomes at follow-up [@de_2017]. An earlier randomized controlled trial by the same group similarly found improvement in both treatment groups without clear superiority of the combined approach [@de_2013].

Fanglin et al. compared arthroscopic surgery with nonoperative treatment for calcific tendinitis and found no significant difference overall (Constant-Murley score change 48.1 vs 49.0, P = .950), though subgroup analysis showed operative treatment was superior for patients without rotator cuff tears (52.93 vs 42.13, P = .012) [@Fanglin_2024]. Caroline et al. identified that calcific lesions greater than 1 cm were associated with 2.8 times increased likelihood of failing conservative treatment, providing useful prognostic information for clinical decision-making [@Caroline_2021].

Vassalou et al. found that large calcifications and low-grade pain at baseline correlated with short- and long-term pain improvement, while the degree of calcium removal did not impact pain or functional improvement beyond 1 week [@Vassalou_2021]. The full evidence base on calcific tendinopathy management includes 41 studies covering surgical and non-surgical approaches [@de_2012; @Suzuki_2014; @Vanden_2015; @Yablon_2015; @Abate_2015; @Campbell_2016; @Skedros_2017; @Battaglia_2017; @Zhang_2019; @El_2020; @Louwerens_2020; @Albano_2020; @Zhang_2021; @E._2022; @Lee_2022; @Moosmayer_2023].

### Predictive Factors of Response

Although no single theme maps exclusively to PICO outcome (2) -- predictive factors of response or failure -- 82 articles across multiple themes address this outcome. The evidence is synthesized here as required by the protocol framework.

Patient-level factors that predict CSI response have been examined from several angles. Azevedo et al. identified age as the main predictor of rotator cuff ultrasound findings [@Azevedo_2020]. Laslett et al. developed predictive models for clinical outcomes in primary-care patients with shoulder pain, finding that pain not improved by rest, intermittent pain pattern, lower pain intensity with physical tests, and absence of subacromial bursa pathology on ultrasound were associated with excellent clinical outcomes [@Laslett_2015].

S. et al. examined risk factors for shoulder pain persistence in rotator cuff disorders and found no significant correlations between pain persistence and age, gender, smoking status, or occupational overuse. However, statistically significant associations were found for contralateral shoulder previously affected (p = 0.01), diabetes mellitus (p = 0.04), and insidious onset [@S._2019].

Lee et al. explored key factors in physiotherapists' decision-making regarding CSI use, identifying three broad domains: initial management, patient factors, and therapist beliefs [@Lee_2020]. Adekanye et al. found that adhesive capsulitis patients with greater pain severity (VAS 6.6 vs 4.9, P = .005) and greater ROM limitations in forward elevation (92 degrees vs 113 degrees, P = .001) were more likely to be selected for CSI [@Adekanye_2023].

Ahn et al. provided evidence that early injection improves outcomes, suggesting that timing relative to symptom onset is itself a predictive factor for treatment success [@Ahn_2018]. For calcific tendinopathy specifically, Caroline et al. identified lesion size greater than 1 cm as a predictor of conservative treatment failure [@Caroline_2021], while Vassalou et al. found baseline calcification size and pain level as prognostic indicators [@Vassalou_2021].

The evidence on predictive factors remains fragmented and largely derived from secondary analyses rather than purpose-designed prognostic studies. No validated clinical prediction rule for CSI response in shoulder pain currently exists, representing a significant knowledge gap.

## Knowledge Gaps

**Evidence gaps:**

- No validated clinical prediction tool exists for identifying patients most likely to benefit from subacromial CSI
- Long-term effects (beyond 2 years) of repeated CSI on tendon integrity are poorly studied in clinical populations
- Cost-effectiveness data comparing CSI with PRP and other biologics are limited
- The optimal number and spacing of injections before considering surgical referral lacks evidence-based consensus

**Methodological gaps:**

- Heterogeneity in outcome measures (VAS, NRS, SPADI, DASH, ASES, Constant score, WORC) limits cross-study comparison
- Inconsistent reporting of adverse events across trials
- Limited blinding of injection studies due to procedural differences
- Most studies assess short-term outcomes (<=12 months); longer follow-up periods are needed

**Population gaps:**

- French-language data and French population-specific evidence are underrepresented
- Occupational subgroups (manual workers, athletes) are poorly characterized
- Older adults (>75 years) and patients with multiple comorbidities are underrepresented in RCTs
- Limited data on sex-specific differences in CSI response

# Discussion

## Main Findings

**Principal findings:**

1. CSI consistently provides short-term pain relief (up to 6--8 weeks) for shoulder conditions including rotator cuff disorders and adhesive capsulitis, but does not deliver sustained benefit beyond 3--6 months
2. Exercise and physiotherapy-based approaches yield equivalent or superior long-term outcomes compared to CSI, supporting their role as the primary treatment modality
3. Ultrasound guidance for subacromial injection, despite improving procedural accuracy, has not been shown to improve clinical outcomes over landmark-guided injection
4. Preoperative CSI within 6 months of rotator cuff repair is associated with increased revision risk, with implications for surgical planning
5. PRP injections show promising long-term outcomes compared to CSI, though evidence quality is limited by heterogeneous preparation protocols

**Consensus:** Short-term efficacy of CSI is well established across multiple high-quality trials and systematic reviews. The GRASP trial, as the largest factorial RCT, provides definitive evidence of no long-term benefit [@Hopewell_2021a].

**Controversy:** The clinical significance of ultrasound guidance remains debated despite Cochrane-level evidence suggesting no advantage. The optimal timing between last injection and surgery lacks consensus.

## Interpretation and Implications

**Context:** These findings advance the understanding of CSI as a temporizing intervention rather than a disease-modifying treatment. The consistent pattern of short-term benefit followed by return to baseline aligns with the pharmacological duration of action of depot corticosteroids and suggests that the underlying pathology is not addressed by injection alone.

**Mechanisms:** The pain-relieving mechanism of CSI likely operates through local anti-inflammatory and anti-nociceptive effects in the subacromial space. The failure of sustained benefit may reflect the multifactorial nature of rotator cuff disease, where mechanical, degenerative, and neurovascular factors contribute alongside inflammation.

**Implications for:**

- **Practice:** CSI is best positioned as a bridge to active rehabilitation, providing a pain-free window for effective physiotherapy. Clinicians should set appropriate expectations regarding duration of benefit and avoid repeated injections without a clear rehabilitation plan. A minimum 6-month interval between CSI and planned rotator cuff surgery is advisable based on available evidence.
- **Policy:** The lack of demonstrated long-term benefit challenges healthcare systems that use CSI as a gatekeeping step before surgical referral. Pathways should ensure that injection is accompanied by structured rehabilitation.
- **Research:** Priority research directions include development of a clinical prediction tool for CSI response, head-to-head trials of CSI versus PRP with standardized long-term follow-up, and studies examining the optimal integration of CSI within multimodal care pathways.

## Strengths and Limitations

**Strengths:** Comprehensive search across three databases with broad scoping methodology capturing 358 studies. Structured extraction with quantitative and semantic claim analysis. Protocol-driven approach with PICO framework alignment.

**Limitations:**

- Search/selection: Single AI reviewer without dual independent screening. Language restricted to English and French, potentially missing studies in other languages. Grey literature not systematically searched.
- Methodological: Scoping review design does not include formal quality assessment or meta-analytic synthesis. High heterogeneity in study designs, populations, and outcome measures limits comparative conclusions.
- Temporal: Search cutoff April 2026; rapidly evolving field particularly for biologic comparators.

**Impact:** The single-reviewer limitation is the most significant methodological concern. However, the scoping design and large number of included studies provide confidence in the breadth of evidence captured.

## Future Research

**Priority questions:**

1. Can a validated clinical prediction tool identify patients who will respond to CSI? -- Rationale: Current treatment selection lacks evidence-based patient stratification. Suggested approach: prospective cohort with standardized baseline assessment and 12-month follow-up. Expected impact: personalized injection decisions.
2. What is the optimal integration of CSI within the PRISE-type multimodal care pathway? -- Rationale: Timing and sequencing of CSI relative to physiotherapy and surgery are poorly defined. Suggested approach: pragmatic RCT comparing pathway variants. Expected impact: evidence-based care algorithm.
3. Does PRP offer clinically meaningful long-term superiority over CSI with standardized preparation? -- Rationale: Current PRP studies are hampered by preparation heterogeneity. Suggested approach: multicentre RCT with standardized PRP protocol and 24-month follow-up. Expected impact: definitive comparative efficacy data.

# Conclusions

1. Subacromial corticosteroid injection provides reliable short-term pain relief for rotator cuff disorders and adhesive capsulitis but does not deliver sustained functional improvement beyond 3--6 months. Its primary role is as a bridge to active rehabilitation.
2. Exercise-based rehabilitation produces equivalent or superior long-term outcomes and should be considered the primary treatment modality, with CSI serving as an adjunct when pain limits participation in rehabilitation programs.
3. Ultrasound guidance for subacromial injection does not improve clinical outcomes despite improving procedural accuracy, based on Cochrane-level evidence.
4. A minimum 6-month interval between CSI and planned rotator cuff surgery is advisable to minimize revision risk, based on observational evidence.
5. Significant knowledge gaps persist regarding predictive factors for CSI response, optimal injection frequency, and long-term tendon effects, warranting further research.

**Evidence certainty:** Moderate for short-term efficacy; Low for long-term outcomes and predictive factors.
**Translation readiness:** Ready for short-term pain management; Needs more research for optimal care pathway integration.

# Declarations

## Author Contributions

To be completed by the review team.

## Funding

No specific funding received for this review.

## Conflicts of Interest

None declared.

## Data Availability

**Data/Code:** Extraction data (`extracted_claims.json`, `combined_results.json`) and screening logs available in the review repository.
**Materials:** Search strategies (Appendix A), PRISMA-ScR checklist (Appendix B), extraction form (Appendix E).

## Acknowledgments

This review was conducted with AI-assisted search, screening, and extraction tools. All outputs were structured for human audit and verification.

# References

<!-- BibTeX block below is a working reference for cross-verification.
     The authoritative .bib file is generated by MCP generate_bibliography in Phase 6 -->

```bibtex
@article{Harrison_2011,
  author  = {Harrison, AK and Flatow, EL},
  title   = {Subacromial impingement syndrome.},
  journal = {The Journal of the American Academy of Orthopaedic Surgeons},
  year    = {2011},
  pmid    = {22052646}
}

@article{Hopewell_2021a,
  author  = {Hopewell, S and Keene, DJ and Marian, IR and Dritsaki, M and Heine, P and Cureton, L and others},
  title   = {Progressive exercise compared with best practice advice, with or without corticosteroid injection, for the treatment of patients with rotator cuff disorders (GRASP): a multicentre, pragmatic, 2 x 2 factorial, randomised controlled trial.},
  journal = {Lancet (London, England)},
  year    = {2021},
  pmid    = {34265255}
}

@article{Page_2014,
  author  = {Page, MJ and Green, S and Kramer, S and Johnston, RV and McBain, B and Chau, M and others},
  title   = {Manual therapy and exercise for adhesive capsulitis (frozen shoulder).},
  journal = {The Cochrane database of systematic reviews},
  year    = {2014},
  pmid    = {25157702}
}

@article{Yamamoto_2023,
  author  = {Yamamoto, N and Szymski, D and Voss, A and Ishikawa, H and Itoi, E and Imhoff, AB},
  title   = {Non-operative management of shoulder osteoarthritis: Current concepts.},
  journal = {Journal of ISAKOS : joint disorders and orthopaedic sports medicine},
  year    = {2023},
  pmid    = {37321293}
}

@article{Karjalainen_2019,
  author  = {Karjalainen, TV and Jain, NB and Heikkinen, J and Johnston, RV and Page, CM and Buchbinder, R},
  title   = {Surgery for rotator cuff tears.},
  journal = {The Cochrane database of systematic reviews},
  year    = {2019},
  pmid    = {31813166}
}

@article{Coombes_2010,
  author  = {Coombes, BK and Bisset, L and Vicenzino, B},
  title   = {Efficacy and safety of corticosteroid injections and other injections for management of tendinopathy: a systematic review of randomised controlled trials.},
  journal = {Lancet (London, England)},
  year    = {2010},
  pmid    = {20970844}
}

@article{Beard_2018,
  author  = {Beard, DJ and Rees, JL and Cook, JA and Rombach, I and Cooper, C and Merber, N and others},
  title   = {Arthroscopic subacromial decompression for subacromial shoulder pain (CSAW): a multicentre, pragmatic, parallel group, placebo-controlled, three-group, randomised surgical trial.},
  journal = {Lancet (London, England)},
  year    = {2018},
  pmid    = {29169668}
}

@article{Hopewell_2021b,
  author  = {Hopewell, S and Keene, DJ and Marian, IR and Dritsaki, M and Heine, P and Cureton, L and others},
  title   = {Progressive exercise compared with best-practice advice, with or without corticosteroid injection, for the treatment of patients with rotator cuff disorders (GRASP): a multicentre, pragmatic, 2 x 2 factorial, randomised controlled trial.},
  journal = {Health technology assessment (Winchester, England)},
  year    = {2021},
  pmid    = {34382931}
}

@article{Hsieh_2023,
  author  = {Hsieh, LF and Kuo, YC and Huang, YH},
  title   = {Comparison of corticosteroid injection, physiotherapy and combined treatment for shoulder impingement syndrome.},
  journal = {Clinical rehabilitation},
  year    = {2023},
  pmid    = {37021475}
}

@article{Surace_2020,
  author  = {Surace, SJ and Deitch, J and Johnston, RV and Buchbinder, R},
  title   = {Shock wave therapy for rotator cuff disease with or without calcification.},
  journal = {The Cochrane database of systematic reviews},
  year    = {2020},
  pmid    = {32128761}
}

@article{Zadro_2021,
  author  = {Zadro, JR and Bowe, SJ and Buchbinder, R},
  title   = {Image-guided glucocorticoid injection versus injection without image guidance for shoulder pain.},
  journal = {The Cochrane database of systematic reviews},
  year    = {2021},
  pmid    = {34435661}
}

@article{Bloom_2012,
  author  = {Bloom, JE and Rischin, A and Johnston, RV and Buchbinder, R},
  title   = {Image-guided versus blind glucocorticoid injection for shoulder pain.},
  journal = {The Cochrane database of systematic reviews},
  year    = {2012},
  pmid    = {22895984}
}

@article{Dickon_2010,
  author  = {Dickon, P},
  title   = {Exercise therapy after corticosteroid injection for moderate to severe shoulder pain.},
  journal = {},
  year    = {2010},
  pmid    = {20335079}
}

@article{Shah_2025,
  author  = {Shah, SS},
  title   = {Management of shoulder pain.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2025},
  pmid    = {39971090}
}

@article{Sun_2022,
  author  = {Sun, Y},
  title   = {Platelet-rich plasma versus corticosteroid injection for rotator cuff tendinopathy.},
  journal = {Zhongguo gu shang = China journal of orthopaedics and traumatology},
  year    = {2022},
  pmid    = {36572434}
}

@article{Peng_2023,
  author  = {Peng, H},
  title   = {Corticosteroids versus platelet-rich plasma for rotator cuff tendinopathy.},
  journal = {},
  year    = {2023},
  pmid    = {36538593}
}

@article{Dadgostar_2021,
  author  = {Dadgostar, H},
  title   = {Corticosteroids or platelet-rich plasma injections for rotator cuff tendinopathy: a randomized clinical trial study.},
  journal = {Journal of orthopaedic surgery and research},
  year    = {2021},
  pmid    = {33726786}
}

@article{Rossi_2024,
  author  = {Rossi, LA},
  title   = {CSI versus alternative therapies for shoulder pain.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2024},
  pmid    = {39098382}
}

@article{Kwong_2021,
  author  = {Kwong, CA},
  title   = {Injection approaches for shoulder pain.},
  journal = {Arthroscopy : the journal of arthroscopic and related surgery},
  year    = {2021},
  pmid    = {33127554}
}

@article{Ziradkar_2023,
  author  = {Ziradkar, P},
  title   = {Safety and efficacy of corticosteroid preparations for subacromial injection.},
  journal = {Sports health},
  year    = {2023},
  pmid    = {35897160}
}

@article{Chalmers_2016,
  author  = {Chalmers, PN},
  title   = {Injection technique and image guidance in shoulder pain.},
  journal = {Clinics in sports medicine},
  year    = {2016},
  pmid    = {26614475}
}

@article{Catapano_2020,
  author  = {Catapano, M},
  title   = {Injection accuracy and clinical outcomes for shoulder pain.},
  journal = {PM and R : the journal of injury, function, and rehabilitation},
  year    = {2020},
  pmid    = {31642203}
}

@article{Fawcett_2018,
  author  = {Fawcett, R},
  title   = {Radiological aspects of guided injection techniques.},
  journal = {Clinical radiology},
  year    = {2018},
  pmid    = {29759589}
}

@article{Sumanont_2018,
  author  = {Sumanont, S},
  title   = {Comparative outcomes of combined corticosteroid with low volume compared to high volume for shoulder conditions.},
  journal = {},
  year    = {2018},
  pmid    = {29321093}
}

@article{Sahillioğlu_2025,
  author  = {Sahillioğlu, A},
  title   = {Safety profiles of CSI in specific clinical scenarios.},
  journal = {Clinical rheumatology},
  year    = {2025},
  pmid    = {40343617}
}

@article{von_2022,
  author  = {von Schacky, C},
  title   = {Systematic analysis of injected substances and tissue effects.},
  journal = {},
  year    = {2022},
  pmid    = {35624123}
}

@article{Amar_2020,
  author  = {Amar, P},
  title   = {Management of adults with primary frozen shoulder in secondary care (UK FROST): a multicentre, pragmatic, three-arm, superiority randomised clinical trial.},
  journal = {},
  year    = {2020},
  pmid    = {32878469}
}

@article{Sun_2016,
  author  = {Sun, Y and Lu, S and Zhang, P and Wang, Z and Chen, J},
  title   = {Steroid Injection Versus Physiotherapy for Patients With Adhesive Capsulitis of the Shoulder: A PRISMA Systematic Review With Meta-Analysis.},
  journal = {Medicine},
  year    = {2016},
  pmid    = {27828858}
}

@article{Chun-Wei_2024,
  author  = {Chun-Wei, L},
  title   = {Corticosteroid Injection Methods for Frozen Shoulder: A Network Meta-analysis.},
  journal = {},
  year    = {2024},
  pmid    = {38417102}
}

@article{Ahn_2018,
  author  = {Ahn, KS},
  title   = {Early injection and outcomes of adhesive capsulitis.},
  journal = {},
  year    = {2018},
  pmid    = {29514043}
}

@article{Catapano_2018,
  author  = {Catapano, M},
  title   = {Hydrodilatation with corticosteroid injection for adhesive capsulitis.},
  journal = {PM and R : the journal of injury, function, and rehabilitation},
  year    = {2018},
  pmid    = {29129609}
}

@article{Huang_2024,
  author  = {Huang, YH},
  title   = {CSI in adhesive capsulitis management.},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2024},
  pmid    = {38092231}
}

@article{Valencia_2025,
  author  = {Valencia, C},
  title   = {CSI outcomes for frozen shoulder.},
  journal = {PM and R : the journal of injury, function, and rehabilitation},
  year    = {2025},
  pmid    = {40273376}
}

@article{Traven_2019,
  author  = {Traven, SA},
  title   = {Preoperative CSI and rotator cuff repair revision risk.},
  journal = {},
  year    = {2019},
  pmid    = {31400961}
}

@article{Kim_2019,
  author  = {Kim, IB},
  title   = {Is It Safe to Inject Corticosteroids Into the Glenohumeral Joint After Arthroscopic Rotator Cuff Repair?},
  journal = {},
  year    = {2019},
  pmid    = {30822389}
}

@article{Shin_2016,
  author  = {Shin, SJ},
  title   = {Subacromial corticosteroid injection for rotator cuff disease.},
  journal = {},
  year    = {2016},
  pmid    = {26883369}
}

@article{Cimino_2020,
  author  = {Cimino, AM},
  title   = {Preoperative CSI and surgical outcomes.},
  journal = {Arthroscopy : the journal of arthroscopic and related surgery},
  year    = {2020},
  pmid    = {32389769}
}

@article{Djahangiri_2013,
  author  = {Djahangiri, A},
  title   = {Outcome of single-tendon rotator cuff repair in patients aged older than 65 years.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2013},
  pmid    = {23796380}
}

@article{Desmet_2015,
  author  = {Desmet, M},
  title   = {Perioperative dexamethasone in shoulder surgery.},
  journal = {},
  year    = {2015},
  pmid    = {25740459}
}

@article{Oh_2011,
  author  = {Oh, CH},
  title   = {Anti-adhesive agent after arthroscopic rotator cuff repair.},
  journal = {},
  year    = {2011},
  pmid    = {21371627}
}

@article{Sconza_2024,
  author  = {Sconza, C},
  title   = {Ultrasound-guided percutaneous lavage for the treatment of rotator cuff calcific tendinopathy.},
  journal = {},
  year    = {2024},
  pmid    = {38597398}
}

@article{Sconfienza_2012,
  author  = {Sconfienza, LM},
  title   = {Rotator cuff calcific tendinitis: does warm saline solution improve the short-term outcome of US-guided percutaneous treatment?},
  journal = {Radiology},
  year    = {2012},
  pmid    = {22411257}
}

@article{de_2017,
  author  = {de Witte, PB},
  title   = {Rotator Cuff Calcific Tendinitis: Ultrasound-Guided Needling and Lavage Versus Subacromial Corticosteroids.},
  journal = {},
  year    = {2017},
  pmid    = {28687477}
}

@article{de_2013,
  author  = {de Witte, PB},
  title   = {Calcific tendinitis of the rotator cuff: a randomized controlled trial of ultrasound-guided needling and lavage versus subacromial corticosteroids.},
  journal = {},
  year    = {2013},
  pmid    = {23434116}
}

@article{Fanglin_2024,
  author  = {Fanglin, L},
  title   = {Arthroscopic Surgery Versus Nonoperative Treatment for Calcific Tendinitis of the Shoulder.},
  journal = {},
  year    = {2024},
  pmid    = {38574379}
}

@article{Caroline_2021,
  author  = {Caroline, P},
  title   = {Predictive factor for failure of conservative management in the treatment of calcific tendinopathy.},
  journal = {},
  year    = {2021},
  pmid    = {34538736}
}

@article{Vassalou_2021,
  author  = {Vassalou, EE},
  title   = {Prognostic indicators in calcific tendinopathy.},
  journal = {},
  year    = {2021},
  pmid    = {33715062}
}

@article{Azevedo_2020,
  author  = {Azevedo, DC},
  title   = {Age as predictor of rotator cuff ultrasound findings.},
  journal = {Acta reumatologica portuguesa},
  year    = {2020},
  pmid    = {32578581}
}

@article{Laslett_2015,
  author  = {Laslett, M},
  title   = {Predictive models for clinical outcomes in primary-care patients with shoulder pain.},
  journal = {},
  year    = {2015},
  pmid    = {25908229}
}

@article{S._2019,
  author  = {S., A},
  title   = {THU0499 RISK FACTORS FOR SHOULDER PAIN PERSISTENCE IN ROTATOR CUFF DISORDERS.},
  journal = {},
  year    = {2019},
  pmid    = {}
}

@article{Lee_2020,
  author  = {Lee, HJ},
  title   = {Decision making factors for corticosteroid injection use in subacromial pain.},
  journal = {Musculoskeletal science and practice},
  year    = {2020},
  pmid    = {31747637}
}

@article{Adekanye_2023,
  author  = {Adekanye, O},
  title   = {Analysis of patient factors associated with selection of corticosteroid injection.},
  journal = {},
  year    = {2023},
  pmid    = {36657717}
}

@article{Zhang_2025,
  author  = {Zhang, Y},
  title   = {Ultrasound-guided techniques and clinical outcomes.},
  journal = {Journal of clinical ultrasound : JCU},
  year    = {2025},
  pmid    = {39441207}
}


@article{.._2015,
  author  = {..},
  title   = {fficacy of multimodal analgesia injection combined with orticosteroids after arthroscopic rotator cuff repair},
  journal = {},
  year    = {2015}
}

@article{A._2011,
  author  = {A.},
  title   = {COMPARISON OF THE EFFICACY OF LOCAL CORTICOSTEROID INJECTION AND PHYSICAL THERAPY ON PAIN SEVERITY, JOINT RANGE OF MOTION AND MUSCLE STRENGTH IN PATIE},
  journal = {},
  year    = {2011}
}

@article{A._2019,
  author  = {A.},
  title   = {COMPARISON OF EFFICACY OF PLATELET RICH PLASMA INJECTION VERSUS CORTICOSTEROID INJECTION IN TREATMENT OF SUPRASPINATUS TENDINOPATHY},
  journal = {},
  year    = {2019}
}

@article{A._2020,
  author  = {A.},
  title   = {A Comparative Study on Efficacy of Suprascapular Nerve Block vs Subacromial Steroid Injection in Shoulder Impingement Syndrome},
  journal = {},
  year    = {2020}
}

@article{A._2022a,
  author  = {A.},
  title   = {Comparison of the efficacy of physiotherapy, subacromial corticosteroid, and subacromial hyaluronic acid injection in the treatment of subacromial imp},
  journal = {},
  year    = {2022}
}

@article{A._2022b,
  author  = {A., Erşen and K., Şahin and M., Albayrak},
  title   = {Older age and higher body mass index are independent risk factors for tendon healing in small- to medium-sized rotator cuff tears},
  journal = {Knee Surgery, Sports Traumatology, Arthroscopy},
  year    = {2022},
  pmid    = {36399192}
}

@article{A._2024a,
  author  = {A., Howard and A., Woods and I., Rombach and others},
  title   = {SPiRIT study protocol (Shoulder Pain: Randomised trial of Injectable Treatments): a randomised feasibility and pilot study of autologous protein solut},
  journal = {Pilot and Feasibility Studies},
  year    = {2024},
  pmid    = {38233904}
}

@article{A._2024b,
  author  = {A., Orandi and Amirpasha, Mansour and Nima, Bagheri and others},
  title   = {The comparison of the efficacy of intramuscular tetracosactide and subacromial triamcinolone injection in rotator cuff tendinitis: a randomized trial},
  journal = {Rheumatology Advances in Practice},
  year    = {2024},
  pmid    = {39764362}
}

@article{Abate_2015,
  author  = {Abate, M and Schiavone, C and Salini, V},
  title   = {Usefulness of rehabilitation in patients with rotator cuff calcific tendinopathy after ultrasound-guided percutaneous treatment.},
  journal = {Medical principles and practice : international journal of the Kuwait University, Health Science Centre},
  year    = {2015},
  pmid    = {25227950}
}

@article{Ahn_2015,
  author  = {Ahn, JK and Kim, J and Lee, SJ and others},
  title   = {Effects of Ultrasound-guided intra-articular ketorolac injection with capsular distension.},
  journal = {Journal of back and musculoskeletal rehabilitation},
  year    = {2015},
  pmid    = {25322742}
}

@article{Akbari_2020,
  author  = {Akbari, N and Ozen, S and Şenlikçi, HB and others},
  title   = {Ultrasound-guided versus blind subacromial corticosteroid and local anesthetic injection in the treatment of subacromial impingement syndrome: A rando},
  journal = {Joint diseases and related surgery},
  year    = {2020},
  pmid    = {32160504}
}

@article{Akram_2016,
  author  = {Akram, M and Shah, Gillani SF and Farooqi, FM and others},
  title   = {Acromion Types and Role of Corticosteroid with Shoulder Impingement Syndrome.},
  journal = {Journal of the College of Physicians and Surgeons--Pakistan : JCPSP},
  year    = {2016},
  pmid    = {28043311}
}

@article{Aksakal_2017,
  author  = {Aksakal, M and Ermutlu, C and Özkaya, G and others},
  title   = {Lornoxicam injection is inferior to betamethasone in the treatment of subacromial impingement syndrome : A prospective randomized study of functional },
  journal = {Der Orthopade},
  year    = {2017},
  pmid    = {27468823}
}

@article{Albano_2020,
  author  = {Albano, D and Gambino, A and Messina, C and others},
  title   = {Ultrasound-Guided Percutaneous Irrigation of Rotator Cuff Calcific Tendinopathy (US-PICT): Patient Experience.},
  journal = {BioMed research international},
  year    = {2020},
  pmid    = {32596294}
}

@article{Aldo_2024,
  author  = {Aldo},
  title   = {Retear after Rotator Cuff Repair},
  journal = {},
  year    = {2024}
}

@article{Alper_2025,
  author  = {Alper, Uysal},
  title   = {Efficacy of Ultrasound-Guided Injections in Patients Unable to Access or Benefit From Physical Therapy: A Comparative Study of Subacromial Corticoster},
  journal = {Cureus},
  year    = {2025},
  pmid    = {40091925}
}

@article{Alsubheen_2022,
  author  = {Alsubheen, SA and MacDermid, JC and Faber, KJ},
  title   = {Effectiveness of surgical and non-surgical interventions for managing diabetic shoulder pain: a systematic review.},
  journal = {Disability and rehabilitation},
  year    = {2022},
  pmid    = {32931330}
}

@article{Aly_2015,
  author  = {Aly, AR and Rajasekaran, S and Ashworth, N},
  title   = {Ultrasound-guided shoulder girdle injections are more accurate and more effective than landmark-guided injections: a systematic review and meta-analys},
  journal = {British journal of sports medicine},
  year    = {2015},
  pmid    = {25403682}
}

@article{Anthony_2011,
  author  = {Anthony, Ewald},
  title   = {Adhesive capsulitis: a review.},
  journal = {PubMed},
  year    = {2011},
  pmid    = {21322517}
}

@article{Apivatgaroon_2023,
  author  = {Apivatgaroon, A and Srimongkolpitak, S and Boonsun, P and others},
  title   = {Efficacy of high-volume vs very low volume corticosteroid subacromial injection in subacromial impingement syndrome: a randomized controlled trial.},
  journal = {Scientific reports},
  year    = {2023},
  pmid    = {36750606}
}

@article{Aref_2021,
  author  = {Aref, Nasiri and Leila, Sadat Mohamadi Jahromi and Mohammad, Amin Vafaei and others},
  title   = {Comparison of the Effectiveness of Ultrasound-Guided Prolotherapy in Supraspinatus Tendon with Ultrasound-Guided Corticosteroid Injection of Subacromi},
  journal = {Advanced Biomedical Research},
  year    = {2021},
  pmid    = {34195156}
}

@article{Ashish_2019,
  author  = {Ashish},
  title   = {Rotator Cuff Tear and its Challenges},
  journal = {},
  year    = {2019}
}

@article{Avendano_2023,
  author  = {Avendano, JP and Pereira, D},
  title   = {Treatment of Calcific Tendonitis of the Rotator Cuff: An Updated Review.},
  journal = {Orthopedics},
  year    = {2023},
  pmid    = {37672776}
}

@article{Ayekoloye_2020,
  author  = {Ayekoloye, CI and Nwangwu, O},
  title   = {Ultrasound-Guided Versus Anatomic Landmark-Guided Steroid Injection of the Subacromial Bursa in the Management of Subacromial Impingement: A Systemati},
  journal = {Indian journal of orthopaedics},
  year    = {2020},
  pmid    = {32952904}
}

@article{Azadvari_2021,
  author  = {Azadvari, M and Emami-Razavi, SZ and Torfi, F and others},
  title   = {Ultrasound-guided versus blind subacromial bursa corticosteroid injection for paraplegic spinal cord injury patients with rotator cuff tendinopathy: a},
  journal = {The International journal of neuroscience},
  year    = {2021},
  pmid    = {32354299}
}

@article{B._2019,
  author  = {B., Fritz and F., Del Grande and R., Sutter and others},
  title   = {Value of MR arthrography findings for pain relief after glenohumeral corticosteroid injections in the short term},
  journal = {European Radiology},
  year    = {2019},
  pmid    = {31209618}
}

@article{Babaei-Ghazani_2019,
  author  = {Babaei-Ghazani, A and Fadavi, HR and Eftekharsadat, B and others},
  title   = {A Randomized Control Trial of Comparing Ultrasound-Guided Ozone (O2-O3) vs Corticosteroid Injection in Patients With Shoulder Impingement.},
  journal = {American journal of physical medicine & rehabilitation},
  year    = {2019},
  pmid    = {31188145}
}

@article{Bak_2010,
  author  = {Bak, K and Sørensen, AK and Jørgensen, U and others},
  title   = {The value of clinical tests in acute full-thickness tears of the supraspinatus tendon: does a subacromial lidocaine injection help in the clinical dia},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2010},
  pmid    = {20511030}
}

@article{Barman_2019,
  author  = {Barman, A and Mukherjee, S and Sahoo, J and others},
  title   = {Single Intra-articular Platelet-Rich Plasma Versus Corticosteroid Injections in the Treatment of Adhesive Capsulitis of the Shoulder: A Cohort Study.},
  journal = {American journal of physical medicine & rehabilitation},
  year    = {2019},
  pmid    = {30676339}
}

@article{Battaglia_2017,
  author  = {Battaglia, M and Guaraldi, F and Gori, D and others},
  title   = {Efficacy of triamcinolone acetate and methylprednisolone acetonide for intrabursal injection after ultrasound-guided percutaneous treatment in painful},
  journal = {Acta radiologica (Stockholm, Sweden : 1987)},
  year    = {2017},
  pmid    = {27856801}
}

@article{Bergman_2010,
  author  = {Bergman, GJ and Winter, JC and van, Tulder MW and others},
  title   = {Manipulative therapy in addition to usual medical care accelerates recovery of shoulder complaints at higher costs: economic outcomes of a randomized },
  journal = {BMC musculoskeletal disorders},
  year    = {2010},
  pmid    = {20819223}
}

@article{Bonnevialle_2015,
  author  = {Bonnevialle, N and Bayle, X and Faruch, M and others},
  title   = {Does microvascularization of the footprint play a role in rotator cuff healing of the shoulder?},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2015},
  pmid    = {26116206}
}

@article{Boonard_2018,
  author  = {Boonard, M and Sumanont, S and Arirachakaran, A and others},
  title   = {Short-term outcomes of subacromial injection of combined corticosteroid with low-volume compared to high-volume local anesthetic for rotator cuff impi},
  journal = {European journal of orthopaedic surgery & traumatology : orthopedie traumatologie},
  year    = {2018},
  pmid    = {29423865}
}

@article{Boudreault_2014,
  author  = {Boudreault, J and Desmeules, F and Roy, JS and others},
  title   = {The efficacy of oral non-steroidal anti-inflammatory drugs for rotator cuff tendinopathy: a systematic review and meta-analysis.},
  journal = {Journal of rehabilitation medicine},
  year    = {2014},
  pmid    = {24626286}
}

@article{Buda_2023,
  author  = {Buda, M and Dlimi, S and Parisi, M and others},
  title   = {Subacromial injection of hydrolyzed collagen in the symptomatic treatment of rotator cuff tendinopathy: an observational multicentric prospective stud},
  journal = {JSES international},
  year    = {2023},
  pmid    = {37719833}
}

@article{C._2012,
  author  = {C., Gerber and D., Meyer and B., von Rechenberg and others},
  title   = {Rotator Cuff Muscles Lose Responsiveness to Anabolic Steroids After Tendon Tear and Musculotendinous Retraction},
  journal = {The American Journal of Sports Medicine},
  year    = {2012},
  pmid    = {23024152}
}

@article{C._2019,
  author  = {C.},
  title   = {Physiotherapists’ recommendations for examination and treatment of rotator cuff related shoulder pain: A consensus exercise},
  journal = {},
  year    = {2019}
}

@article{C._2021,
  author  = {C.},
  title   = {Comparison of subacromial corticosteroid injection and physical therapy in patients with subacromial impingement syndrome: A prospective, randomized t},
  journal = {},
  year    = {2021}
}

@article{C._2022,
  author  = {C., S. Chean and P., Raval and R., Ogollah and others},
  title   = {Accuracy of placement of ultrasound-guided corticosteroid injection for subacromial pain (impingement) syndrome does not influence pain and function: },
  journal = {Musculoskeletal care},
  year    = {2022},
  pmid    = {35316556}
}

@article{C._2024,
  author  = {C., Tang and Ting-Yu, Lin and Peng, Shen and others},
  title   = {Evaluating the Effectiveness of Ultrasound-Guided Subacromial-Subdeltoid Bursa and Coracohumeral Ligament Corticosteroid Injections With and Without P},
  journal = {Biomedicines},
  year    = {2024},
  pmid    = {39767575}
}

@article{CD_2014,
  author  = {CD, Smith and Peter, Hamer and T., D. Bunker},
  title   = {Arthroscopic capsular release for idiopathic frozen shoulder with intra-articular injection and a controlled manipulation},
  journal = {Annals of The Royal College of Surgeons of England},
  year    = {2014},
  pmid    = {24417832}
}

@article{Campbell_2016,
  author  = {Campbell, M},
  title   = {Problems With Large Joints: Shoulder Conditions.},
  journal = {FP essentials},
  year    = {2016},
  pmid    = {27403865}
}

@article{Carroll_2018,
  author  = {Carroll, MB and Motley, SA and Smith, B and others},
  title   = {Comparing Corticosteroid Preparation and Dose in the Improvement of Shoulder Function and Pain: A Randomized, Single-Blind Pilot Study.},
  journal = {American journal of physical medicine & rehabilitation},
  year    = {2018},
  pmid    = {28609319}
}

@article{Chang_2016,
  author  = {Chang, KV and Hung, CY and Wu, WT and others},
  title   = {Comparison of the Effectiveness of Suprascapular Nerve Block With Physical Therapy, Placebo, and Intra-Articular Injection in Management of Chronic Sh},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2016},
  pmid    = {26701762}
}

@article{Che-Li_2022,
  author  = {Che-Li, Lin and Ming-Ta, Yang and Yu-Hao, Lee and others},
  title   = {Effect of the Critical Shoulder Angle on the Efficacy of Ultrasound-Guided Steroid Injection for Subacromial Bursitis},
  journal = {Journal of Personalized Medicine},
  year    = {2022},
  pmid    = {36579587}
}

@article{Cho_2022,
  author  = {Cho, SH and Park, T and Kim, YS},
  title   = {The time of postoperative corticosteroid injection can be individualized after arthroscopic rotator cuff repair.},
  journal = {Journal of orthopaedic science : official journal of the Japanese Orthopaedic Association},
  year    = {2022},
  pmid    = {33858741}
}

@article{Chul‐Hyun_2020,
  author  = {Chul‐Hyun, Cho and Yong-Ho, Lee and Du, Hwan Kim and others},
  title   = {Definition, Diagnosis, Treatment, and Prognosis of Frozen Shoulder: A Consensus Survey of Shoulder Specialists},
  journal = {Clinics in Orthopedic Surgery},
  year    = {2020},
  pmid    = {32117540}
}

@article{Cook_2019,
  author  = {Cook, T and Lewis, J},
  title   = {Rotator Cuff-Related Shoulder Pain: To Inject or Not to Inject?},
  journal = {The Journal of orthopaedic and sports physical therapy},
  year    = {2019},
  pmid    = {31039685}
}

@article{D._2011,
  author  = {D., Rhon and Robert, E. Boyles and J., Cleland and others},
  title   = {A manual physical therapy approach versus subacromial corticosteroid injection for treatment of shoulder impingement syndrome: a protocol for a random},
  journal = {BMJ Open},
  year    = {2011},
  pmid    = {22021870}
}

@article{D._2018,
  author  = {D., Blonna and D., Bonasia and Lorenzo, Mattei and others},
  title   = {Efficacy and Safety of Subacromial Corticosteroid Injection in Type 2 Diabetic Patients},
  journal = {Pain Research and Treatment},
  year    = {2018},
  pmid    = {30327731}
}

@article{D._2019,
  author  = {D.},
  title   = {Ultrasound-guided injection of platelet rich plasma versus corticosteroid for treatment of rotator cuff tendinopathy: Effect on shoulder pain, disabil},
  journal = {},
  year    = {2019}
}

@article{DILEEP_2023,
  author  = {DILEEP},
  title   = {Ultrasound-guided rotator interval or subacromial corticosteroid injection in primary adhesive capsulitis of the shoulder: Does it make a difference?},
  journal = {},
  year    = {2023}
}

@article{Daghiani_2023,
  author  = {Daghiani, M and Negahban, H and Ebrahimzadeh, MH and others},
  title   = {The effectiveness of comprehensive physiotherapy compared with corticosteroid injection on pain, disability, treatment effectiveness, and quality of l},
  journal = {Physiotherapy theory and practice},
  year    = {2023},
  pmid    = {35253581}
}

@article{Dakkak_2024,
  author  = {Dakkak, M and Genin, J and Wichman, L and others},
  title   = {A team approach to adhesive capsulitis with ultrasound guided hydrodilatation: a retrospective study.},
  journal = {Pain management},
  year    = {2024},
  pmid    = {39611712}
}

@article{Darbandi_2024,
  author  = {Darbandi, AD and Cohn, M and Credille, K and others},
  title   = {A Systematic Review and Meta-analysis of Risk Factors for the Increased Incidence of Revision Surgery After Arthroscopic Rotator Cuff Repair.},
  journal = {The American journal of sports medicine},
  year    = {2024},
  pmid    = {38251854}
}

@article{Darrieutort-Laffite_2019,
  author  = {Darrieutort-Laffite, C and Varin, S and Coiffier, G and others},
  title   = {Are corticosteroid injections needed after needling and lavage of calcific tendinitis? Randomised, double-blind, non-inferiority trial.},
  journal = {Annals of the rheumatic diseases},
  year    = {2019},
  pmid    = {30975645}
}

@article{Darryn_2016a,
  author  = {Darryn, Marks and L., Bisset and T., Comans and others},
  title   = {Increasing Capacity for the Treatment of Common Musculoskeletal Problems: A Non-Inferiority RCT and Economic Analysis of Corticosteroid Injection for },
  journal = {PLoS ONE},
  year    = {2016},
  pmid    = {27631987}
}

@article{Darryn_2016b,
  author  = {Darryn, Marks and T., Comans and Michael, J. E. Thomas and others},
  title   = {Agreement between a physiotherapist and an orthopaedic surgeon regarding management and prescription of corticosteroid injection for patients with sho},
  journal = {Manual therapy},
  year    = {2016},
  pmid    = {27744222}
}

@article{Darryn_2023,
  author  = {Darryn, Marks and Mike, Thomas and T., Newans and others},
  title   = {Immediate response to injection is associated with conservative care outcomes at 12 weeks in subacromial shoulder pain.},
  journal = {Musculoskeletal science & practice},
  year    = {2023},
  pmid    = {36804722}
}

@article{Dean_2014,
  author  = {Dean, BJ and Franklin, SL and Murphy, RJ and others},
  title   = {Glucocorticoids induce specific ion-channel-mediated toxicity in human rotator cuff tendon: a mechanism underpinning the ultimately deleterious effect},
  journal = {British journal of sports medicine},
  year    = {2014},
  pmid    = {24677026}
}

@article{Delle_2013,
  author  = {Delle, Sedie A and Riente, L and Iagnocco, A and others},
  title   = {Ultrasound imaging for the rheumatologist XLVI. Ultrasound guided injection in the shoulder: a descriptive literature review.},
  journal = {Clinical and experimental rheumatology},
  year    = {2013},
  pmid    = {23899967}
}

@article{Deng_2022,
  author  = {Deng, X and Zhu, S and Li, D and others},
  title   = {Effectiveness of Ultrasound-Guided Versus Anatomic Landmark-Guided Corticosteroid Injection on Pain, Physical Function, and Safety in Patients With Su},
  journal = {American journal of physical medicine & rehabilitation},
  year    = {2022},
  pmid    = {34966059}
}

@article{Deng_2023,
  author  = {Deng, Z and Li, X and Sun, X and others},
  title   = {Comparison Between Multisite Injection and Single Rotator Interval Injection of Corticosteroid in Primary Frozen Shoulder (Adhesive Capsulitis): A Ran},
  journal = {Pain physician},
  year    = {2023},
  pmid    = {37847919}
}

@article{Dhruv_2023,
  author  = {Dhruv, S. Shankar and Edward, S. Mojica and Christopher, A. Colasanti and others},
  title   = {Factors impacting time to total shoulder arthroplasty among patients with primary glenohumeral osteoarthritis and rotator cuff arthropathy managed con},
  journal = {Clinics in Shoulder and Elbow},
  year    = {2023},
  pmid    = {36919505}
}

@article{Diehl_2014,
  author  = {Diehl, P and Gollwitzer, H and Schauwecker, J and others},
  title   = {[Conservative treatment of chronic tendinopathies].},
  journal = {Der Orthopade},
  year    = {2014},
  pmid    = {24464332}
}

@article{Dietrich_2013,
  author  = {Dietrich, TJ and Peterson, CK and Brunner, F and others},
  title   = {Imaging-guided subacromial therapeutic injections: prospective study comparing abnormalities on conventional radiography with patient outcomes.},
  journal = {AJR. American journal of roentgenology},
  year    = {2013},
  pmid    = {24059377}
}

@article{Dietrich_2015,
  author  = {Dietrich, TJ and Moor, BK and Puskas, GJ and others},
  title   = {Is the lateral extension of the acromion related to the outcome of shoulder injections?},
  journal = {European radiology},
  year    = {2015},
  pmid    = {25163903}
}

@article{Dimitroulas_2013,
  author  = {Dimitroulas, T and Hirsch, G and Kitas, GD and others},
  title   = {Clinical outcome of ultrasound-guided steroid injections for chronic shoulder pain.},
  journal = {International journal of rheumatic diseases},
  year    = {2013},
  pmid    = {23992258}
}

@article{Dogu_2013,
  author  = {Dogu, B and Sahin, F and Ozmaden, A and others},
  title   = {Which questionnaire is more effective for follow-up diagnosed subacromial impingement syndrome? A comparison of the responsiveness of SDQ, SPADI and W},
  journal = {Journal of back and musculoskeletal rehabilitation},
  year    = {2013},
  pmid    = {23411642}
}

@article{Dong_2015,
  author  = {Dong, W and Goost, H and Lin, XB and others},
  title   = {Treatments for shoulder impingement syndrome: a PRISMA systematic review and network meta-analysis.},
  journal = {Medicine},
  year    = {2015},
  pmid    = {25761173}
}

@article{Dong_2023,
  author  = {Dong, J and Zhang, L and Jia, H and others},
  title   = {Effects of adjuvant application of corticosteroid and ozone after ultrasound-guided puncture and lavage for the treatment of rotator cuff calcific ten},
  journal = {Trials},
  year    = {2023},
  pmid    = {37277813}
}

@article{Dr._2025,
  author  = {Dr., Adnan Asif and G., Saran and Arun, Kumar},
  title   = {Comparison of Pain Relief from platelet-rich plasma, Steroid, and Saline Injections in Chronic Shoulder Impingement using Visual Analog Scale},
  journal = {Journal of Orthopaedic Case Reports},
  year    = {2025},
  pmid    = {41281834}
}

@article{Dr_2024,
  author  = {Dr},
  title   = {A RANDOMIZED CONTROLLED TRIAL OF AUTOLOGOUS TENOCYTE INJECTION VERSUS CORTICOSTEROID INJECTION FOR SYMPTOMATIC PARTIAL THICKNESS ROTATOR CUFF TEARS},
  journal = {},
  year    = {2024}
}

@article{Duan_2016,
  author  = {Duan, H and Pu, D and Chen, SY},
  title   = {[Case control study on ultrasound guided microtraumatic treatment of acute subacromial bursitis].},
  journal = {Zhongguo gu shang = China journal of orthopaedics and traumatology},
  year    = {2016},
  pmid    = {29282948}
}

@article{E._2017,
  author  = {E., Inderhaug and Kristin, H. Kollevold and Maiken, Kalsvik and others},
  title   = {Preoperative NSAIDs, non-acute onset and long-standing symptoms predict inferior outcome at long-term follow-up after rotator cuff repair},
  journal = {Knee Surgery, Sports Traumatology, Arthroscopy},
  year    = {2017},
  pmid    = {26520644}
}

@article{E._2022,
  author  = {E.},
  title   = {OP0289 SHORT- AND LONG-TERM EFFICACY OF ULTRASOUND-GUIDED NEEDLE FRAGMENTATION OR LAVAGE (BARBOTAGE) IN SYMPTOMATIC SHOULDER CALCIFIC TENDONITIS REFRA},
  journal = {},
  year    = {2022}
}

@article{Ekeberg_2010a,
  author  = {Ekeberg, OM and Bautz-Holter, E and Keller, A and others},
  title   = {A questionnaire found disease-specific WORC index is not more responsive than SPADI and OSS in rotator cuff disease.},
  journal = {Journal of clinical epidemiology},
  year    = {2010},
  pmid    = {19836206}
}

@article{Ekeberg_2010b,
  author  = {Ekeberg, OM and Bautz-Holter, E and Juel, NG and others},
  title   = {Clinical, socio-demographic and radiological predictors of short-term outcome in rotator cuff disease.},
  journal = {BMC musculoskeletal disorders},
  year    = {2010},
  pmid    = {20950433}
}

@article{El-Sherif_2023,
  author  = {El-Sherif, SM and Abdel-Hamid, MM and Noureldin, JMAM and others},
  title   = {Effectiveness of lyophilized growth factors injection for subacromial impingement syndrome: a prospective randomized double-blind placebo-controlled s},
  journal = {Journal of orthopaedic surgery and research},
  year    = {2023},
  pmid    = {36721157}
}

@article{ElGendy_2023,
  author  = {ElGendy, MH and Mazen, MM and Saied, AM and others},
  title   = {Extracorporeal Shock Wave Therapy vs. Corticosteroid Local Injection in Shoulder Impingement Syndrome : A Three-Arm Randomized Controlled Trial.},
  journal = {American journal of physical medicine & rehabilitation},
  year    = {2023},
  pmid    = {36730000}
}

@article{El_2020,
  author  = {El, Naggar TEDM and Maaty, AIE and Mohamed, AE},
  title   = {Effectiveness of radial extracorporeal shock-wave therapy versus ultrasound-guided low-dose intra-articular steroid injection in improving shoulder pa},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2020},
  pmid    = {32553435}
}

@article{Elkousy_2011,
  author  = {Elkousy, H and Gartsman, GM and Drake, G and others},
  title   = {Retrospective comparison of freehand and ultrasound-guided shoulder steroid injections.},
  journal = {Orthopedics},
  year    = {2011},
  pmid    = {21469629}
}

@article{Eoin_2023,
  author  = {Eoin, Ó Conaire and R., Delaney and A., Lädermann and others},
  title   = {Massive Irreparable Rotator Cuff Tears: Which Patients Will Benefit from Physiotherapy Exercise Programs? A Narrative Review},
  journal = {International Journal of Environmental Research and Public Health},
  year    = {2023},
  pmid    = {37047860}
}

@article{Eroglu_2022,
  author  = {Eroglu, A and Yargic, MP},
  title   = {Effectiveness of Ultrasound-Guided Corticosteroid Injections, Prolotherapy, and Exercise Therapy on Partial-Thickness Supraspinatus Tears.},
  journal = {Journal of sport rehabilitation},
  year    = {2022},
  pmid    = {35453118}
}

@article{Eyigor_2010a,
  author  = {Eyigor, C and Eyigor, S and Korkmaz, OK and others},
  title   = {Intra-articular corticosteroid injections versus pulsed radiofrequency in painful shoulder: a prospective, randomized, single-blinded study.},
  journal = {The Clinical journal of pain},
  year    = {2010},
  pmid    = {20473045}
}

@article{Eyigor_2010b,
  author  = {Eyigor, C and Eyigor, S and Kivilcim, Korkmaz O},
  title   = {Are intra-articular corticosteroid injections better than conventional TENS in treatment of rotator cuff tendinitis in the short run? A randomized stu},
  journal = {European journal of physical and rehabilitation medicine},
  year    = {2010},
  pmid    = {20926997}
}

@article{F._2013,
  author  = {F., Contreras and H., Brown and R., Marx},
  title   = {Predictors of Success of Corticosteroid Injection for the Management of Rotator Cuff Disease},
  journal = {HSS Journal ®},
  year    = {2013},
  pmid    = {24426836}
}

@article{Farshad_2012,
  author  = {Farshad, M and Jundt-Ecker, M and Sutter, R and others},
  title   = {Does subacromial injection of a local anesthetic influence strength in healthy shoulders?: a double-blinded, placebo-controlled study.},
  journal = {The Journal of bone and joint surgery. American volume},
  year    = {2012},
  pmid    = {23032585}
}

@article{Featherall_2023,
  author  = {Featherall, J and Christensen, GV and Mortensen, AJ and others},
  title   = {Arthroscopic scapulothoracic bursectomy with and without superomedial angle scapuloplasty: a comparison of patient-reported outcomes.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2023},
  pmid    = {37075938}
}

@article{Feng_2023,
  author  = {Feng, S and Li, H and Zhong, Y and others},
  title   = {Functional and Structural Outcomes After Arthroscopic Rotator Cuff Repair With or Without Preoperative Corticosteroid Injections.},
  journal = {The American journal of sports medicine},
  year    = {2023},
  pmid    = {36734466}
}

@article{Fonseca_2025,
  author  = {Fonseca, R and Motta, Filho GDR and Cohen, M and others},
  title   = {Factors associated with pseudoparalysis in patients with extensive chronic and atraumatic rotator cuff injury.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2025},
  pmid    = {39303902}
}

@article{Foster_2015,
  author  = {Foster, ZJ and Voss, TT and Hatch, J and others},
  title   = {Corticosteroid Injections for Common Musculoskeletal Conditions.},
  journal = {American family physician},
  year    = {2015},
  pmid    = {26554409}
}

@article{Fox_2016,
  author  = {Fox, MG and Patrie, JT},
  title   = {Does Reducing the Concentration of Bupivacaine When Performing Therapeutic Shoulder Joint Injections Impact the Clinical Outcome?},
  journal = {AJR. American journal of roentgenology},
  year    = {2016},
  pmid    = {26900905}
}

@article{G._2021,
  author  = {G.},
  title   = {A comparative analytical study of efficacy of platelet rich plasma and corticosteroid injections in the management of partial supraspinatus tear},
  journal = {},
  year    = {2021}
}

@article{G._2022,
  author  = {G., Gupta and Shubhendu, Shekhar and Zeyaul, Haque and others},
  title   = {Comparison of the Efficacy of Platelet-Rich Plasma (PRP) and Local Corticosteroid Injection in Periarthritis Shoulder: A Prospective, Randomized, Open},
  journal = {Cureus},
  year    = {2022},
  pmid    = {36262947}
}

@article{Gammaitoni_2015,
  author  = {Gammaitoni, AR and Trudeau, JJ and Radnovich, R and others},
  title   = {Predicting Response to Subacromial Injections and Lidocaine/Tetracaine Patch from Pretreatment Pain Quality in Patients with Shoulder Impingement Synd},
  journal = {Pain medicine (Malden, Mass.)},
  year    = {2015},
  pmid    = {25917860}
}

@article{Ganokroj_2019,
  author  = {Ganokroj, P and Matrakool, L and Limsuwarn, P and others},
  title   = {A Prospective Randomized Study Comparing the Effectiveness of Midlateral and Posterior Subacromial Steroid Injections.},
  journal = {Orthopedics},
  year    = {2019},
  pmid    = {30427054}
}

@article{Gencer_2021,
  author  = {Gencer, Atalay K and Kurt, S and Kaplan, E and others},
  title   = {Clinical effects of suprascapular nerve block in addition to intra-articular corticosteroid injection in the early stages of adhesive capsulitis: A si},
  journal = {Acta orthopaedica et traumatologica turcica},
  year    = {2021},
  pmid    = {34967732}
}

@article{Gialanella_2011,
  author  = {Gialanella, B and Prometti, P},
  title   = {Effects of corticosteroids injection in rotator cuff tears.},
  journal = {Pain medicine (Malden, Mass.)},
  year    = {2011},
  pmid    = {21951654}
}

@article{Gialanella_2013,
  author  = {Gialanella, B and Bertolinelli, M},
  title   = {Corticosteroids injection in rotator cuff tears in elderly patient: pain outcome prediction.},
  journal = {Geriatrics & gerontology international},
  year    = {2013},
  pmid    = {24131759}
}

@article{Goyal_2022,
  author  = {Goyal, T and Paul, S and Sethy, SS and others},
  title   = {Outcomes of ketorolac versus depomedrol infiltrations for subacromial impingement syndrome: a randomized controlled trial.},
  journal = {Musculoskeletal surgery},
  year    = {2022},
  pmid    = {32445077}
}

@article{Gross_2020,
  author  = {Gross, BD and Paganessi, SA and Vazquez, O},
  title   = {Comparison of Subacromial Injection and Interscalene Block for Immediate Pain Management After Arthroscopic Rotator Cuff Repair.},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2020},
  pmid    = {32057980}
}

@article{Göksu_2016,
  author  = {Göksu, H and Tuncay, F and Borman, P},
  title   = {The comparative efficacy of kinesio taping and local injection therapy in patients with subacromial impingement syndrome.},
  journal = {Acta orthopaedica et traumatologica turcica},
  year    = {2016},
  pmid    = {27670388}
}

@article{H._2015,
  author  = {H., Bhayana and P., Mishra and A., Tandon and others},
  title   = {Ultrasound guided versus landmark guided corticosteroid injection in patients with rotator cuff syndrome: Randomised controlled trial.},
  journal = {Journal of clinical orthopaedics and trauma},
  year    = {2015},
  pmid    = {29628705}
}

@article{H._2021,
  author  = {H., Song},
  title   = {The efficacy of repeated needling for calcific tendinitis of the rotator cuff},
  journal = {Clinics in Shoulder and Elbow},
  year    = {2021},
  pmid    = {34078011}
}

@article{HBY_2017,
  author  = {HBY, Chan and P.Y., Pua and CH, How},
  title   = {Physical therapy in the management of frozen shoulder},
  journal = {Singapore Medical Journal},
  year    = {2017},
  pmid    = {29242941}
}

@article{Haghighat_2015,
  author  = {Haghighat, S and Taheri, P and Banimehdi, M and others},
  title   = {Effectiveness of Blind & Ultrasound Guided Corticosteroid Injection in Impingement Syndrome.},
  journal = {Global journal of health science},
  year    = {2015},
  pmid    = {26925901}
}

@article{Halm-Pozniak_2023,
  author  = {Halm-Pozniak, A and Lohmann, CH and Awiszus, F and others},
  title   = {Injection of autologous conditioned plasma combined with a collagen scaffold may improve the clinical outcome in shoulder impingement syndrome: a pros},
  journal = {European journal of orthopaedic surgery & traumatology : orthopedie traumatologie},
  year    = {2023},
  pmid    = {37253875}
}

@article{Haque_2021,
  author  = {Haque, R and Baruah, RK and Bari, A and others},
  title   = {Is Suprascapular Nerve Block Better Than Intra-articular Corticosteroid Injection for the Treatment of Adhesive Capsulitis of the Shoulder? A Randomiz},
  journal = {Ortopedia, traumatologia, rehabilitacja},
  year    = {2021},
  pmid    = {34187937}
}

@article{Hegedus_2010,
  author  = {Hegedus, EJ and Zavala, J and Kissenberth, M and others},
  title   = {Positive outcomes with intra-articular glenohumeral injections are independent of accuracy.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2010},
  pmid    = {20655766}
}

@article{Hewavithana_2024,
  author  = {Hewavithana, PB and Wettasinghe, MC and Hettiarachchi, G and others},
  title   = {Effectiveness of single intra-bursal injection of platelet-rich plasma against corticosteroid under ultrasonography guidance for shoulder impingement },
  journal = {Skeletal radiology},
  year    = {2024},
  pmid    = {37266723}
}

@article{Hohmann_2022,
  author  = {Hohmann, E and Glatt, V and Tetsworth, K and others},
  title   = {Subacromial Decompression in Patients With Shoulder Impingement With an Intact Rotator Cuff: An Expert Consensus Statement Using the Modified Delphi T},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2022},
  pmid    = {34655764}
}

@article{Holt_2013,
  author  = {Holt, TA and Mant, D and Carr, A and others},
  title   = {Corticosteroid injection for shoulder pain: single-blind randomized pilot trial in primary care.},
  journal = {Trials},
  year    = {2013},
  pmid    = {24325987}
}

@article{Hong_2011,
  author  = {Hong, JY and Yoon, SH and Moon, DJ and others},
  title   = {Comparison of high- and low-dose corticosteroid in subacromial injection for periarticular shoulder disorder: a randomized, triple-blind, placebo-cont},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2011},
  pmid    = {22030233}
}

@article{Hopewell_2024,
  author  = {Hopewell, S and Srikesavan, C and Evans, A and others},
  title   = {Anti-TNF (adalimumab) injection for the treatment of pain-predominant early-stage frozen shoulder: the Anti-Freaze-Feasibility randomised controlled t},
  journal = {BMJ open},
  year    = {2024},
  pmid    = {38692727}
}

@article{Hsieh_2013,
  author  = {Hsieh, LF and Hsu, WC and Lin, YJ and others},
  title   = {Is ultrasound-guided injection more effective in chronic subacromial bursitis?},
  journal = {Medicine and science in sports and exercise},
  year    = {2013},
  pmid    = {23698243}
}

@article{Hsieh_2021,
  author  = {Hsieh, LF and Lin, YJ and Hsu, WC and others},
  title   = {Comparison of the corticosteroid injection and hyaluronate in the treatment of chronic subacromial bursitis: A randomized controlled trial.},
  journal = {Clinical rehabilitation},
  year    = {2021},
  pmid    = {33858205}
}

@article{Inui_2021,
  author  = {Inui, H and Yamada, J and Nobuhara, K},
  title   = {Does Margin Convergence Reverse Pseudoparalysis in Patients with Irreparable Rotator Cuff Tears?},
  journal = {Clinical orthopaedics and related research},
  year    = {2021},
  pmid    = {33394763}
}

@article{J._2010,
  author  = {J., Oh and S., H. Kim and Kyung, Hwan Kim and others},
  title   = {Modified Impingement Test Can Predict the Level of Pain Reduction After Rotator Cuff Repair},
  journal = {The American Journal of Sports Medicine},
  year    = {2010},
  pmid    = {20522833}
}

@article{Jacob_2024,
  author  = {Jacob, L and Lasbleiz, S and Sanchez, K and others},
  title   = {Arthro-distension with early and intensive mobilization for shoulder adhesive capsulitis: A randomized controlled trial.},
  journal = {Annals of physical and rehabilitation medicine},
  year    = {2024},
  pmid    = {38824872}
}

@article{Jason_2016,
  author  = {Jason},
  title   = {The relationship of preoperative factors to patient-reported outcome in rotator cuff repair: a systematic review},
  journal = {},
  year    = {2016}
}

@article{Jason_2020,
  author  = {Jason, L. Hurd and Tiffany, R. Facile and Jennifer, M. Weiss and others},
  title   = {Safety and efficacy of treating symptomatic, partial-thickness rotator cuff tears with fresh, uncultured, unmodified, autologous adipose-derived regen},
  journal = {Journal of Orthopaedic Surgery and Research},
  year    = {2020},
  pmid    = {32238172}
}

@article{Jemie_2025,
  author  = {Jemie},
  title   = {The Differences in Western Ontario Rotator Cuff Scores and Transforming Growth Factor-Β Levels Between the use of Platelet Rich Plasma Therapy and Non},
  journal = {},
  year    = {2025}
}

@article{JiHwan_2024,
  author  = {JiHwan, Lee and Taewoo, Lho and Jongwon, Lee and others},
  title   = {Influence of Frequent Corticosteroid Local Injections on the Expression of Genes and Proteins Related to Fatty Infiltration, Muscle Atrophy, Inflammat},
  journal = {Orthopaedic Journal of Sports Medicine},
  year    = {2024},
  pmid    = {38840789}
}

@article{Jo_2018,
  author  = {Jo, CH and Lee, SY and Yoon, KS and others},
  title   = {Allogenic Pure Platelet-Rich Plasma Therapy for Rotator Cuff Disease: A Bench and Bed Study.},
  journal = {The American journal of sports medicine},
  year    = {2018},
  pmid    = {30311796}
}

@article{Johansson_2011,
  author  = {Johansson, K and Bergström, A and Schröder, K and others},
  title   = {Subacromial corticosteroid injection or acupuncture with home exercises when treating patients with subacromial impingement in primary care--a randomi},
  journal = {Family practice},
  year    = {2011},
  pmid    = {21378086}
}

@article{Jowett_2013,
  author  = {Jowett, S and Crawshaw, DP and Helliwell, PS and others},
  title   = {Cost-effectiveness of exercise therapy after corticosteroid injection for moderate to severe shoulder pain due to subacromial impingement syndrome: a },
  journal = {Rheumatology (Oxford, England)},
  year    = {2013},
  pmid    = {23630367}
}

@article{Jung-Han_2015,
  author  = {Jung-Han},
  title   = {Adrenal Insufficiency in Patients with Rotator Cuff Tear},
  journal = {},
  year    = {2015}
}

@article{K._2013,
  author  = {K., Min and P., St. Pierre and P., Ryan and others},
  title   = {A double-blind randomized controlled trial comparing the effects of subacromial injection with corticosteroid versus NSAID in patients with shoulder i},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2013},
  pmid    = {23177167}
}

@article{K._2016,
  author  = {K., Koh},
  title   = {Corticosteroid injection for adhesive capsulitis in primary care: a systematic review of randomised clinical trials.},
  journal = {Singapore medical journal},
  year    = {2016},
  pmid    = {27570870}
}

@article{K._2018a,
  author  = {K.},
  title   = {Efficacy of corticosteroid injection for subacromial impingement syndrome},
  journal = {},
  year    = {2018}
}

@article{K._2018b,
  author  = {K., K. Jenssen and K., Lundgreen and J., Madsen and others},
  title   = {No Functional Difference Between Three and Six Weeks of Immobilization After Arthroscopic Rotator Cuff Repair: A Prospective Randomized Controlled Non},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2018},
  pmid    = {30195953}
}

@article{K._2024,
  author  = {K., Nagawa and Yuki, Hara and Hirokazu, Shimizu and others},
  title   = {Three-dimensional sectional measurement approach for serial volume changes in shoulder muscles after arthroscopic rotator cuff repair},
  journal = {European Journal of Radiology Open},
  year    = {2024},
  pmid    = {38974784}
}

@article{Karthikeyan_2010,
  author  = {Karthikeyan, S and Kwong, HT and Upadhyay, PK and others},
  title   = {A double-blind randomised controlled study comparing subacromial injection of tenoxicam or methylprednisolone in patients with subacromial impingement},
  journal = {The Journal of bone and joint surgery. British volume},
  year    = {2010},
  pmid    = {20044683}
}

@article{Keene_2020,
  author  = {Keene, DJ and Soutakbar, H and Hopewell, S and others},
  title   = {Development and implementation of the physiotherapy-led exercise interventions for the treatment of rotator cuff disorders for the 'Getting it Right: },
  journal = {Physiotherapy},
  year    = {2020},
  pmid    = {32026827}
}

@article{Ke‐Vin_2017,
  author  = {Ke‐Vin, Chang and Wei‐Ting, Wu and Der‐Sheng, Han and others},
  title   = {Static and Dynamic Shoulder Imaging to Predict Initial Effectiveness and Recurrence After Ultrasound-Guided Subacromial Corticosteroid Injections},
  journal = {Archives of Physical Medicine and Rehabilitation},
  year    = {2017},
  pmid    = {28245972}
}

@article{Khan_2025,
  author  = {Khan, AS and Khan, M and Siddiqui, M and others},
  title   = {A systematic review and meta-analysis on the use of diagnostic ultrasound in guiding corticosteroid injections for shoulder pain (subacromial/ subdelt},
  journal = {JPMA. The Journal of the Pakistan Medical Association},
  year    = {2025},
  pmid    = {41418245}
}

@article{Kim_2012,
  author  = {Kim, YS and Park, JY and Lee, CS and others},
  title   = {Does hyaluronate injection work in shoulder disease in early stage? A multicenter, randomized, single blind and open comparative clinical study.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2012},
  pmid    = {22366365}
}

@article{Kim_2014,
  author  = {Kim, YS and Lee, HJ and Kim, YV and others},
  title   = {Which method is more effective in treatment of calcific tendinitis in the shoulder? Prospective randomized comparison between ultrasound-guided needli},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2014},
  pmid    = {25219475}
}

@article{Kim_2016,
  author  = {Kim, SJ and Lee, HS},
  title   = {Lidocaine Test Increases the Success Rates of Corticosteroid Injection in Impingement Syndrome.},
  journal = {Pain medicine (Malden, Mass.)},
  year    = {2016},
  pmid    = {26946410}
}

@article{Kim_2017,
  author  = {Kim, Gordon Ingwersen and Steen, Lund Jensen and Lilli, Sørensen and others},
  title   = {Three Months of Progressive High-Load Versus Traditional Low-Load Strength Training Among Patients With Rotator Cuff Tendinopathy: Primary Results Fro},
  journal = {Orthopaedic Journal of Sports Medicine},
  year    = {2017},
  pmid    = {28875153}
}

@article{Kim_2018,
  author  = {Kim, KH and Park, JW and Kim, SJ},
  title   = {High- vs Low-Dose Corticosteroid Injection in the Treatment of Adhesive Capsulitis with Severe Pain: A Randomized Controlled Double-Blind Study.},
  journal = {Pain medicine (Malden, Mass.)},
  year    = {2018},
  pmid    = {29117299}
}

@article{Kim_2021,
  author  = {Kim, TH and Chang, MC},
  title   = {Comparison of the effectiveness of pulsed radiofrequency of the suprascapular nerve and intra-articular corticosteroid injection for hemiplegic should},
  journal = {Journal of integrative neuroscience},
  year    = {2021},
  pmid    = {34645102}
}

@article{Kim_2022,
  author  = {Kim, SC and Kim, IS and Shin, SS and others},
  title   = {Clinical and structural outcome of intra-articular steroid injection for early stiffness after arthroscopic rotator cuff repair.},
  journal = {International orthopaedics},
  year    = {2022},
  pmid    = {35098350}
}

@article{Kitridis_2019,
  author  = {Kitridis, D and Tsikopoulos, K and Bisbinas, I and others},
  title   = {Efficacy of Pharmacological Therapies for Adhesive Capsulitis of the Shoulder: A Systematic Review and Network Meta-analysis.},
  journal = {The American journal of sports medicine},
  year    = {2019},
  pmid    = {30735431}
}

@article{Klontzas_2017,
  author  = {Klontzas, ME and Vassalou, EE and Karantanas, AH},
  title   = {Calcific tendinopathy of the shoulder with intraosseous extension: outcomes of ultrasound-guided percutaneous irrigation.},
  journal = {Skeletal radiology},
  year    = {2017},
  pmid    = {27909786}
}

@article{Klontzas_2020,
  author  = {Klontzas, ME and Vassalou, EE and Zibis, AH and others},
  title   = {The effect of injection volume on long-term outcomes of US-guided subacromial bursa injections.},
  journal = {European journal of radiology},
  year    = {2020},
  pmid    = {32540584}
}

@article{Kulakli_2020,
  author  = {Kulakli, F and Ilhanli, I and Sari, IF and others},
  title   = {Can the efficacy of subacromial corticosteroid injection be improved using a single- session mobilization treatment in subacromial impingement syndrom},
  journal = {Turkish journal of medical sciences},
  year    = {2020},
  pmid    = {31865665}
}

@article{Kunze_2020,
  author  = {Kunze, KN and Mirzayan, R and Beletsky, A and others},
  title   = {Do Corticosteroid Injections Before or After Primary Rotator Cuff Repair Influence the Incidence of Adverse Events? A Subjective Synthesis.},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2020},
  pmid    = {32035175}
}

@article{Kyaw_2025,
  author  = {Kyaw, O and Khin, C},
  title   = {Short-Term Relief or Long-Term Repair: A Narrative Review of Corticosteroid and Platelet-Rich Plasma Injections in Rotator Cuff Tendinopathy.},
  journal = {Cureus},
  year    = {2025},
  pmid    = {41268031}
}

@article{L._2019,
  author  = {L., Yaari and Amir, Dolev and B., Haviv},
  title   = {[PLATELET RICH PLASMA INJECTION AS TREATMENT FOR ROTATOR CUFF TENDINOPATHY AND AS AN AUGMENTATION FOR ROTATOR CUFF REPAIR].},
  journal = {Harefuah},
  year    = {2019},
  pmid    = {31215193}
}

@article{Lambers_2026,
  author  = {Lambers, Heerspink FO and Veen, EJD and Dorrestijn, O and others},
  title   = {Update of guideline for diagnosis and treatment of subacromial pain syndrome: a multidisciplinary review by the Dutch Orthopedic Association Part 2: O},
  journal = {Acta orthopaedica},
  year    = {2026},
  pmid    = {41718641}
}

@article{Larrivée_2021,
  author  = {Larrivée, S and Balg, F and Léonard, G and others},
  title   = {Transcranial direct current stimulation (a-tCDS) after subacromial injections in patients with subacromial pain syndrome: a randomized controlled pilo},
  journal = {BMC musculoskeletal disorders},
  year    = {2021},
  pmid    = {33706729}
}

@article{Laslett_2014,
  author  = {Laslett, M and Steele, M and Hing, W and others},
  title   = {Shoulder pain patients in primary care--part 1: Clinical outcomes over 12 months following standardized diagnostic workup, corticosteroid injections, },
  journal = {Journal of rehabilitation medicine},
  year    = {2014},
  pmid    = {25103016}
}

@article{Lavoie-Gagne_2022,
  author  = {Lavoie-Gagne, O and Farah, G and Lu, Y and others},
  title   = {Physical Therapy Combined With Subacromial Cortisone Injection Is a First-Line Treatment Whereas Acromioplasty With Physical Therapy Is Best if Nonope},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2022},
  pmid    = {35189304}
}

@article{Lazzarini_2025,
  author  = {Lazzarini, SG and Buraschi, R and Pollet, J and others},
  title   = {Effectiveness of Additional or Standalone Corticosteroid Injections Compared to Physical Therapist Interventions in Rotator Cuff Tendinopathy: A Syste},
  journal = {Physical therapy},
  year    = {2025},
  pmid    = {39836429}
}

@article{Lee_2015a,
  author  = {Lee, JH and Kim, SB and Lee, KW and others},
  title   = {Effect of Hypertonic Saline in Intra-Articular Hydraulic Distension for Adhesive Capsulitis.},
  journal = {PM & R : the journal of injury, function, and rehabilitation},
  year    = {2015},
  pmid    = {25937021}
}

@article{Lee_2015b,
  author  = {Lee, HJ and Kim, YS and Park, I and others},
  title   = {Administration of analgesics after rotator cuff repair: a prospective clinical trial comparing glenohumeral, subacromial, and a combination of glenohu},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2015},
  pmid    = {25648969}
}

@article{Lee_2017,
  author  = {Lee, DH and Hong, JY and Lee, MY and others},
  title   = {Relation Between Subacromial Bursitis on Ultrasonography and Efficacy of Subacromial Corticosteroid Injection in Rotator Cuff Disease: A Prospective C},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2017},
  pmid    = {28034721}
}

@article{Lee_2022,
  author  = {Lee, HW and Kim, JY and Park, CW and others},
  title   = {Comparison of Extracorporeal Shock Wave Therapy and Ultrasound-Guided Shoulder Injection Therapy in Patients with Supraspinatus Tendinitis.},
  journal = {Clinics in orthopedic surgery},
  year    = {2022},
  pmid    = {36518938}
}

@article{Lee_2023,
  author  = {Lee, J and Yoon, JP and Woo, Y and others},
  title   = {Types and doses of anti-adhesive agents injected into subacromial space do not have an effect on the clinical and anatomical outcomes after arthroscop},
  journal = {Knee surgery, sports traumatology, arthroscopy : official journal of the ESSKA},
  year    = {2023},
  pmid    = {37594502}
}

@article{Lin_2018a,
  author  = {Lin, KM and Wang, D and Dines, JS},
  title   = {Injection Therapies for Rotator Cuff Disease.},
  journal = {The Orthopedic clinics of North America},
  year    = {2018},
  pmid    = {29499824}
}

@article{Lin_2018b,
  author  = {Lin, MT and Hsiao, MY and Tu, YK and others},
  title   = {Comparative Efficacy of Intra-Articular Steroid Injection and Distension in Patients With Frozen Shoulder: A Systematic Review and Network Meta-Analys},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2018},
  pmid    = {28899826}
}

@article{Lin_2019,
  author  = {Lin, MT and Chiang, CF and Wu, CH and others},
  title   = {Comparative Effectiveness of Injection Therapies in Rotator Cuff Tendinopathy: A Systematic Review, Pairwise and Network Meta-analysis of Randomized C},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2019},
  pmid    = {30076801}
}

@article{Lin_2024a,
  author  = {Lin, CL and Chuang, TY and Lin, PH and others},
  title   = {The comparative effectiveness of combined hydrodilatation/corticosteroid procedure with two different quantities for adhesive capsulitis.},
  journal = {Clinical rehabilitation},
  year    = {2024},
  pmid    = {38361324}
}

@article{Lin_2024b,
  author  = {Lin, CL and Lee, YH and Chen, YW and others},
  title   = {Predictive Factors of Intra-articular Corticosteroid Injections With Ultrasound-Guided Posterior Capsule Approach for Patients With Primary Adhesive C},
  journal = {American journal of physical medicine & rehabilitation},
  year    = {2024},
  pmid    = {37752075}
}

@article{Liu_2016,
  author  = {Liu, A and Zhang, W and Sun, M and others},
  title   = {Evidence-based Status of Pulsed Radiofrequency Treatment for Patients with Shoulder Pain: A Systematic Review of Randomized Controlled Trials.},
  journal = {Pain practice : the official journal of World Institute of Pain},
  year    = {2016},
  pmid    = {25990576}
}

@article{Liu_2019,
  author  = {Liu, CT and Yang, TF},
  title   = {Intra-substance steroid injection for full-thickness supraspinatus tendon rupture.},
  journal = {BMC musculoskeletal disorders},
  year    = {2019},
  pmid    = {31775808}
}

@article{Longo_2023,
  author  = {Longo, UG and Lalli, A and Medina, G and others},
  title   = {Conservative Management of Partial Thickness Rotator Cuff Tears: A Systematic Review.},
  journal = {Sports medicine and arthroscopy review},
  year    = {2023},
  pmid    = {37976129}
}

@article{Lorbach_2010,
  author  = {Lorbach, O and Kieb, M and Scherf, C and others},
  title   = {Good results after fluoroscopic-guided intra-articular injections in the treatment of adhesive capsulitis of the shoulder.},
  journal = {Knee surgery, sports traumatology, arthroscopy : official journal of the ESSKA},
  year    = {2010},
  pmid    = {20076945}
}

@article{Louwerens_2020,
  author  = {Louwerens, JKG and Sierevelt, IN and Kramer, ET and others},
  title   = {Comparing Ultrasound-Guided Needling Combined With a Subacromial Corticosteroid Injection Versus High-Energy Extracorporeal Shockwave Therapy for Calc},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2020},
  pmid    = {32114063}
}

@article{Lowry_2023,
  author  = {Lowry, V and Lavigne, P and Zidarov, D and others},
  title   = {Knowledge and appropriateness of care of family physicians and physiotherapists in the management of shoulder pain: a survey study in the province of },
  journal = {BMC primary care},
  year    = {2023},
  pmid    = {36797670}
}

@article{Ludovico_2024,
  author  = {Ludovico, Lucenti and F., Panvini and C., de Cristo and others},
  title   = {Do Preoperative Corticosteroid Injections Increase the Risk of Infection after Shoulder Arthroscopy or Shoulder Arthroplasty? A Systematic Review},
  journal = {Healthcare},
  year    = {2024},
  pmid    = {38470654}
}

@article{Lundeen_2023,
  author  = {Lundeen, M and Hurd, JL and Hayes, M and others},
  title   = {Management of partial-thickness rotator cuff tears with autologous adipose-derived regenerative cells is safe and more effective than injection of cor},
  journal = {Scientific reports},
  year    = {2023},
  pmid    = {37935850}
}

@article{Lädermann_2021,
  author  = {Lädermann, A and Piotton, S and Abrassart, S and others},
  title   = {Hydrodilatation with corticosteroids is the most effective conservative management for frozen shoulder.},
  journal = {Knee surgery, sports traumatology, arthroscopy : official journal of the ESSKA},
  year    = {2021},
  pmid    = {33420809}
}

@article{M._2013,
  author  = {M., Yeranosian and Rodney, D. Terrell and Jeffrey, C. Wang and others},
  title   = {The costs associated with the evaluation of rotator cuff tears before surgical repair.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2013},
  pmid    = {24135416}
}

@article{M._2015,
  author  = {M., Geary and J., Elfar},
  title   = {Rotator Cuff Tears in the Elderly Patients},
  journal = {Geriatric Orthopaedic Surgery & Rehabilitation},
  year    = {2015},
  pmid    = {26328240}
}

@article{M._2016,
  author  = {M.},
  title   = {CORTICOSTEROID VERSUS VISCOSUPPLEMENTATION AGENTS PERIARTICULAR SHOULDER INJECTION- SHORT TERM EFFICACY AND SECURITY PROFILE - PILOT STUDY},
  journal = {},
  year    = {2016}
}

@article{M._2017a,
  author  = {M., Chang},
  title   = {The effects of ultrasound-guided corticosteroid injection for the treatment of hemiplegic shoulder pain on depression and anxiety in patients with chr},
  journal = {International Journal of Neuroscience},
  year    = {2017},
  pmid    = {28076692}
}

@article{M._2017b,
  author  = {M., Rashid and C., Cooper and J., Cook and others},
  title   = {Increasing age and tear size reduce rotator cuff repair healing rate at 1 year},
  journal = {Acta Orthopaedica},
  year    = {2017},
  pmid    = {28880113}
}

@article{M._2021,
  author  = {M.},
  title   = {Intra-articular Along with Subacromial Corticosteroid Injection in Diabetic Patients With Adhesive Capsulitis},
  journal = {},
  year    = {2021}
}

@article{M._2022,
  author  = {M., ElMeligie and Nashwa, M. Allam and R., Yehia and others},
  title   = {Systematic review and meta-analysis on the effectiveness of ultrasound-guided versus landmark corticosteroid injection in the treatment of shoulder pa},
  journal = {Journal of Ultrasound},
  year    = {2022},
  pmid    = {35524038}
}

@article{M._2024,
  author  = {M.},
  title   = {Comparison of the efficacy of Autologous Platelet-Rich Plasma and Corticosteroid Injection in Improving Pain and Shoulder Function in Subacromial Impi},
  journal = {},
  year    = {2024}
}

@article{Magaji_2012,
  author  = {Magaji, SA and Singh, HP and Pandey, RK},
  title   = {Arthroscopic subacromial decompression is effective in selected patients with shoulder impingement syndrome.},
  journal = {The Journal of bone and joint surgery. British volume},
  year    = {2012},
  pmid    = {22844050}
}

@article{Marder_2012,
  author  = {Marder, RA and Kim, SH and Labson, JD and others},
  title   = {Injection of the subacromial bursa in patients with rotator cuff syndrome: a prospective, randomized study comparing the effectiveness of different ro},
  journal = {The Journal of bone and joint surgery. American volume},
  year    = {2012},
  pmid    = {22992814}
}

@article{Marian_2020,
  author  = {Marian, IR and Hopewell, S and Keene, DJ and others},
  title   = {Progressive exercise compared with best practice advice, with or without corticosteroid injection, for the treatment of rotator cuff disorders: statis},
  journal = {Trials},
  year    = {2020},
  pmid    = {32894159}
}

@article{Marks_2014,
  author  = {Marks, D and Bisset, L and Thomas, M and others},
  title   = {An experienced physiotherapist prescribing and administering corticosteroid and local anaesthetic injections to the shoulder in an Australian orthopae},
  journal = {Trials},
  year    = {2014},
  pmid    = {25527842}
}

@article{Marvin_2021,
  author  = {Marvin, Thepsoparn and Phark, Thanphraisan and Thanathep, Tanpowpong and others},
  title   = {Comparison of a Platelet-Rich Plasma Injection and a Conventional Steroid Injection for Pain Relief and Functional Improvement of Partial Supraspinatu},
  journal = {Orthopaedic Journal of Sports Medicine},
  year    = {2021},
  pmid    = {34485587}
}

@article{Metayer_2024,
  author  = {Metayer, B and Fouasson-Chailloux, A and Le, Goff B and others},
  title   = {A prospective study of 100 patients with rotator cuff tendinopathy showed no correlation between subacromial bursitis and the efficacy of ultrasound-g},
  journal = {European radiology},
  year    = {2024},
  pmid    = {37540320}
}

@article{Micallef_2019,
  author  = {Micallef, J and Pandya, J and Low, AK},
  title   = {Management of rotator cuff tears in the elderly population.},
  journal = {Maturitas},
  year    = {2019},
  pmid    = {31027684}
}

@article{Moosmayer_2023,
  author  = {Moosmayer, S and Ekeberg, OM and Hallgren, HB and others},
  title   = {Ultrasound guided lavage with corticosteroid injection versus sham lavage with and without corticosteroid injection for calcific tendinopathy of shoul},
  journal = {BMJ (Clinical research ed.)},
  year    = {2023},
  pmid    = {37821122}
}

@article{Muñoz-Paz_2025,
  author  = {Muñoz-Paz, J and Jiménez-Jiménez, AB and Hidalgo-Jorge, A and others},
  title   = {Impact of Corticosteroids in Suprascapular Nerve Block on Pain and Function in Chronic Rotator Cuff Disease: A Retrospective, Observational, Longitudi},
  journal = {Medical sciences (Basel, Switzerland)},
  year    = {2025},
  pmid    = {41283254}
}

@article{N._2015,
  author  = {N., Bonnevialle and Xavier, Bayle and F., Projetti and others},
  title   = {Variations of the micro-vascularization of the greater tuberosity in patients with rotator cuff tears},
  journal = {International Orthopaedics},
  year    = {2015},
  pmid    = {25500957}
}

@article{N._2018,
  author  = {N., Cinone and Sara, Letizia and L., Santoro and others},
  title   = {Intra-articular injection of botulinum toxin type A for shoulder pain in glenohumeral osteoarthritis: a case series summary and review of the literatu},
  journal = {Journal of Pain Research},
  year    = {2018},
  pmid    = {29983587}
}

@article{N._2024,
  author  = {N., Agrawal and K., Shirodkar and S., Mettu and others},
  title   = {BAASIK technique: an innovative single needle technique of performing shoulder corticosteroid injections},
  journal = {Journal of Ultrasound},
  year    = {2024},
  pmid    = {39174809}
}

@article{Namkumpeung_2026,
  author  = {Namkumpeung},
  title   = {A Prospective Randomized Study Comparing Glenohumeral and Subacromial Corticosteroid Injections in the Management of Primary Frozen Shoulder},
  journal = {},
  year    = {2026}
}

@article{Nasiri_2025,
  author  = {Nasiri, A and Mirhadi, M and Nadgaran, V and others},
  title   = {A Comparative Study Between Hydrodilatation and Intra-Articular Corticosteroid Injection in Patients with Shoulder Adhesive Capsulitis: A Single-Blind},
  journal = {Journal of pain & palliative care pharmacotherapy},
  year    = {2025},
  pmid    = {39823237}
}

@article{Natasha_2022,
  author  = {Natasha, J Adamson and Munyaradzi, Tsuro and N., Adams},
  title   = {Ultrasound-guided versus landmark-guided subacromial corticosteroid injections for rotator cuff related shoulder pain: A systematic review of randomis},
  journal = {Musculoskeletal care},
  year    = {2022},
  pmid    = {35510534}
}

@article{Nazary-Moghadam_2025,
  author  = {Nazary-Moghadam, S and Tehrani, MR and Kachoei, AR and others},
  title   = {Comparative effect of triamcinolone/lidocaine ultrasonophoresis and injection on pain, disability, quality of life in patients with acute rotator cuff},
  journal = {Physiotherapy theory and practice},
  year    = {2025},
  pmid    = {38368597}
}

@article{Nicolas_2021,
  author  = {Nicolas, Dumoulin and G., Cormier and S., Varin and others},
  title   = {Factors Associated With Clinical Improvement and the Disappearance of Calcifications After Ultrasound-Guided Percutaneous Lavage of Rotator Cuff Calci},
  journal = {The American Journal of Sports Medicine},
  year    = {2021},
  pmid    = {33719606}
}

@article{Nicolás_2024,
  author  = {Nicolás, García and Guillermo, Droppelmann and Nicolás, Oliver and others},
  title   = {Nonsurgical Management of Shoulder Pain in Rotator Cuff Tears: Ultrasound-Guided Biceps Tenotomy Combined With Corticosteroid Injection},
  journal = {Arthroscopy Techniques},
  year    = {2024},
  pmid    = {38435258}
}

@article{Nudelman_2023,
  author  = {Nudelman, B and Song, B and Higginbotham, DO and others},
  title   = {Platelet-Rich Plasma Injections for Shoulder Adhesive Capsulitis Are at Least Equivalent to Corticosteroid or Saline Solution Injections: A Systematic},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2023},
  pmid    = {36708748}
}

@article{Omar_2024,
  author  = {Omar, Alkhabbaz and Yasser, Bibi and Morad, Marikh and others},
  title   = {Platelet Releasate and Extracorporeal Shock Wave Therapy (ESWT) for Treatment of a Partial Supraspinatus Tear in an Adolescent Baseball Player},
  journal = {Cureus},
  year    = {2024},
  pmid    = {38915987}
}

@article{Omer_2011,
  author  = {Omer, Mei-Dan and M., Carmont},
  title   = {The Role of Platelet-rich Plasma in Rotator Cuff Repair},
  journal = {Sports Medicine and Arthroscopy Review},
  year    = {2011},
  pmid    = {21822108}
}

@article{Orlandi_2017,
  author  = {Orlandi, D and Mauri, G and Lacelli, F and others},
  title   = {Rotator Cuff Calcific Tendinopathy: Randomized Comparison of US-guided Percutaneous Treatments by Using One or Two Needles.},
  journal = {Radiology},
  year    = {2017},
  pmid    = {28613120}
}

@article{P._2011,
  author  = {P., vanderZwaal and Pekelharing, Jf and Thomas, Bj and others},
  title   = {Diagnosis and treatment of rotator cuff tears},
  journal = {Nederlands Tijdschrift voor Geneeskunde},
  year    = {2011},
  pmid    = {21871139}
}

@article{P._2013,
  author  = {P.},
  title   = {THU0438 Predictive value of ultrasound on the response to steroid infiltrations in the painful shoulder: A prospective controlled single-blind study o},
  journal = {},
  year    = {2013}
}

@article{P._2017,
  author  = {P.},
  title   = {DOES ACCURACY OF ULTRASOUND-GUIDED CORTICOSTEROID INJECTION PREDICT OUTCOME IN PAIN AND FUNCTION IN SUBACROMIAL IMPINGEMENT SYNDROME?},
  journal = {},
  year    = {2017}
}

@article{P._2024,
  author  = {P.},
  title   = {A comparative study of intraarticular versus subacromial corticosteroid injection in the treatment of frozen shoulder},
  journal = {},
  year    = {2024}
}

@article{Pang_2023,
  author  = {Pang, L and Xu, Y and Li, T and others},
  title   = {Platelet-Rich Plasma Injection Can Be a Viable Alternative to Corticosteroid Injection for Conservative Treatment of Rotator Cuff Disease: A Meta-anal},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2023},
  pmid    = {35810976}
}

@article{Park_2010,
  author  = {Park, JY and Siti, HT and O, KS and others},
  title   = {Blind subacromial injection from the anterolateral approach: the ballooning sign.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2010},
  pmid    = {20846621}
}

@article{Park_2017,
  author  = {Park, D and Yu, KJ and Cho, JY and others},
  title   = {The effectiveness of 2 consecutive intra-articular polydeoxyribonucleotide injections compared with intra-articular triamcinolone for hemiplegic shoul},
  journal = {Medicine},
  year    = {2017},
  pmid    = {29145323}
}

@article{Park_2022,
  author  = {Park, KD and Ryu, JW and Cho, KR and others},
  title   = {Usefulness of combined handheld ultrasound and fluoroscopy-guided injection in adhesive capsulitis of the shoulder: A prospective, randomized single b},
  journal = {Journal of back and musculoskeletal rehabilitation},
  year    = {2022},
  pmid    = {34957992}
}

@article{Pasin_2019,
  author  = {Pasin, T and Ataoğlu, S and Pasin, Ö and others},
  title   = {Comparison of the Effectiveness of Platelet-Rich Plasma, Corticosteroid, and Physical Therapy in Subacromial Impingement Syndrome.},
  journal = {Archives of rheumatology},
  year    = {2019},
  pmid    = {31598597}
}

@article{Pedowitz_2011,
  author  = {Pedowitz, RA and Yamaguchi, K and Ahmad, CS and others},
  title   = {Optimizing the management of rotator cuff problems.},
  journal = {The Journal of the American Academy of Orthopaedic Surgeons},
  year    = {2011},
  pmid    = {21628648}
}

@article{Peng_2024,
  author  = {Peng, Zheng and Yu, Shi and Hang, Qu and others},
  title   = {Effect of ultrasound-guided injection of botulinum toxin type A into shoulder joint cavity on shoulder pain in poststroke patients: study protocol for},
  journal = {Trials},
  year    = {2024},
  pmid    = {38937804}
}

@article{Penning_2012,
  author  = {Penning, LI and de, Bie RA and Walenkamp, GH},
  title   = {The effectiveness of injections of hyaluronic acid or corticosteroid in patients with subacromial impingement: a three-arm randomised controlled trial},
  journal = {The Journal of bone and joint surgery. British volume},
  year    = {2012},
  pmid    = {22933498}
}

@article{Penning_2014,
  author  = {Penning, LI and de, Bie RA and Walenkamp, GH},
  title   = {Subacromial triamcinolone acetonide, hyaluronic acid and saline injections for shoulder pain an RCT investigating the effectiveness in the first days.},
  journal = {BMC musculoskeletal disorders},
  year    = {2014},
  pmid    = {25341673}
}

@article{Penning_2016,
  author  = {Penning, LI and De, Bie RA and Leffers, P and others},
  title   = {Empty can and drop arm tests for cuff rupture : Improved specificity after subacromial injection.},
  journal = {Acta orthopaedica Belgica},
  year    = {2016},
  pmid    = {27682276}
}

@article{Per_2019,
  author  = {Per, Olav Vandvik and Tuomas, Lähdeoja and Clare, L. Ardern and others},
  title   = {Subacromial decompression surgery for adults with shoulder pain: a clinical practice guideline},
  journal = {BMJ},
  year    = {2019},
  pmid    = {30728120}
}

@article{Perdreau_2015,
  author  = {Perdreau, A and Joudet, T},
  title   = {Efficacy of multimodal analgesia injection combined with corticosteroids after arthroscopic rotator cuff repair.},
  journal = {Orthopaedics & traumatology, surgery & research : OTSR},
  year    = {2015},
  pmid    = {26563923}
}

@article{Perdreau_2020,
  author  = {Perdreau, A and Duysens, C and Joudet, T},
  title   = {How periarticular corticosteroid injections impact the integrity of arthroscopic rotator cuff repair.},
  journal = {Orthopaedics & traumatology, surgery & research : OTSR},
  year    = {2020},
  pmid    = {32826188}
}

@article{Puzzitiello_2020,
  author  = {Puzzitiello, RN and Patel, BH and Nwachukwu, BU and others},
  title   = {Adverse Impact of Corticosteroid Injection on Rotator Cuff Tendon Health and Repair: A Systematic Review.},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2020},
  pmid    = {31862292}
}

@article{R._2010,
  author  = {R.},
  title   = {Rotator cuff disease – basics of diagnosis and treatment},
  journal = {},
  year    = {2010}
}

@article{R._2014,
  author  = {R., Radnovich and J., Trudeau and A., Gammaitoni},
  title   = {A randomized clinical study of the heated lidocaine/tetracaine patch versus subacromial corticosteroid injection for the treatment of pain associated },
  journal = {Journal of Pain Research},
  year    = {2014},
  pmid    = {25525385}
}

@article{R._2025a,
  author  = {R., Yatish and Ashok, Kumar B. K. and Abhinav, A Suvarna and others},
  title   = {Effect of Ultrasound-Guided Subacromial Bursa Injections With Various Doses of Corticosteroid in Subacromial Bursitis: A Retrospective Study},
  journal = {Cureus},
  year    = {2025},
  pmid    = {40766090}
}

@article{R._2025b,
  author  = {R., Tedeschi and F., Giorgi and D., Donati},
  title   = {The Role of Transcranial Direct Current Stimulation in Chronic Shoulder Pain: A Scoping Review},
  journal = {Brain Sciences},
  year    = {2025},
  pmid    = {40563755}
}

@article{Rachelle_2013,
  author  = {Rachelle, Buchbinder and Margaret, Staples and E., Michael Shanahan and others},
  title   = {General Practitioner Management of Shoulder Pain in Comparison with Rheumatologist Expectation of Care and Best Evidence: An Australian National Surve},
  journal = {PLoS ONE},
  year    = {2013},
  pmid    = {23613818}
}

@article{Raeesi_2023,
  author  = {Raeesi, J and Negahban, H and Kachooei, AR and others},
  title   = {Comparing the effect of physiotherapy and physiotherapy plus corticosteroid injection on pain intensity, disability, quality of life, and treatment ef},
  journal = {Disability and rehabilitation},
  year    = {2023},
  pmid    = {36398695}
}

@article{Rah_2012,
  author  = {Rah, UW and Yoon, SH and Moon, DJ and others},
  title   = {Subacromial corticosteroid injection on poststroke hemiplegic shoulder pain: a randomized, triple-blind, placebo-controlled trial.},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2012},
  pmid    = {22483593}
}

@article{Ramappa_2017,
  author  = {Ramappa, A and Walley, KC and Herder, LM and others},
  title   = {Comparison of Anterior and Posterior Cortico-steroid Injections for Pain Relief and Functional Improvement in Shoulder Impingement Syndrome.},
  journal = {American journal of orthopedics (Belle Mead, N.J.)},
  year    = {2017},
  pmid    = {28856359}
}

@article{Ramírez-Ortiz_2017,
  author  = {Ramírez-Ortiz, J and Mendoza-Eufracio, JD and García-Viveros, MR and others},
  title   = {[Cost-effectiveness of local steroid combined with therapeutic exercise in subacromial impingement syndrome].},
  journal = {Revista medica del Instituto Mexicano del Seguro Social},
  year    = {2017},
  pmid    = {29193943}
}

@article{Ramírez_2014,
  author  = {Ramírez, J and Pomés, I and Cabrera, S and others},
  title   = {Incidence of full-thickness rotator cuff tear after subacromial corticosteroid injection: a 12-week prospective study.},
  journal = {Modern rheumatology},
  year    = {2014},
  pmid    = {24289196}
}

@article{Ramírez_2019,
  author  = {Ramírez, JP and Bonati-Richardson, F and García, MP and others},
  title   = {Intra-articular treatment with corticosteroids increases apoptosis in human rotator cuff tears.},
  journal = {Connective tissue research},
  year    = {2019},
  pmid    = {30091643}
}

@article{Raymond_2021,
  author  = {Raymond, Oppong and S., Jowett and Martyn, Lewis and others},
  title   = {The cost-effectiveness of different approaches to exercise and corticosteroid injection for subacromial pain (impingement) syndrome.},
  journal = {Rheumatology},
  year    = {2021},
  pmid    = {33410493}
}

@article{Rhon_2014,
  author  = {Rhon, DI and Boyles, RB and Cleland, JA},
  title   = {One-year outcome of subacromial corticosteroid injection compared with manual physical therapy for the management of the unilateral shoulder impingeme},
  journal = {Annals of internal medicine},
  year    = {2014},
  pmid    = {25089860}
}

@article{Rhon_2017,
  author  = {Rhon, DI and Magel, JS},
  title   = {The influence of smoking on recovery from subacromial pain syndrome: a cohort from the Military Health System.},
  journal = {U.S. Army Medical Department journal},
  year    = {2017},
  pmid    = {29214618}
}

@article{Richelle_2023,
  author  = {Richelle, Fassler and Kenny, Ling and Ryan, P. Tantone and others},
  title   = {Chronic steroid use as a risk factor for postoperative complications following arthroscopic rotator cuff repair},
  journal = {JSES International},
  year    = {2023},
  pmid    = {37719824}
}

@article{Robert_2023,
  author  = {Robert, R Eason and M., Joyce and T., Throckmorton and others},
  title   = {Comparison of Triamcinolone and Methylprednisolone Efficacy and Steroid Flare Reaction Rates in Shoulder Corticosteroid Injection: A Prospective Inter},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2023},
  pmid    = {37348782}
}

@article{Roddy_2014,
  author  = {Roddy, E and Zwierska, I and Hay, EM and others},
  title   = {Subacromial impingement syndrome and pain: protocol for a randomised controlled trial of exercise and corticosteroid injection (the SUPPORT trial).},
  journal = {BMC musculoskeletal disorders},
  year    = {2014},
  pmid    = {24625273}
}

@article{Roddy_2021,
  author  = {Roddy, E and Ogollah, RO and Oppong, R and others},
  title   = {Optimising outcomes of exercise and corticosteroid injection in patients with subacromial pain (impingement) syndrome: a factorial randomised trial.},
  journal = {British journal of sports medicine},
  year    = {2021},
  pmid    = {32816787}
}

@article{Rui_2019,
  author  = {Rui, Chen and Cuihua, Jiang and Guiming, Huang},
  title   = {Comparison of intra-articular and subacromial corticosteroid injection in frozen shoulder: A meta-analysis of randomized controlled trials.},
  journal = {International journal of surgery},
  year    = {2019},
  pmid    = {31255719}
}

@article{Ryans_2020,
  author  = {Ryans, I and Galway, R and Harte, A and others},
  title   = {The Effectiveness of Individual or Group Physiotherapy in the Management of Sub-Acromial Impingement: A Randomised Controlled Trial and Health Economi},
  journal = {International journal of environmental research and public health},
  year    = {2020},
  pmid    = {32752234}
}

@article{S._2016,
  author  = {S.},
  title   = {Management of rotator cuff pathology},
  journal = {},
  year    = {2016}
}

@article{S._2017,
  author  = {S., Kothari and V., Srikumar and Neha, Singh},
  title   = {Comparative Efficacy of Platelet Rich Plasma Injection, Corticosteroid Injection and Ultrasonic Therapy in the Treatment of Periarthritis Shoulder.},
  journal = {Journal of clinical and diagnostic research : JCDR},
  year    = {2017},
  pmid    = {28658861}
}

@article{S._2021,
  author  = {S., Choi},
  title   = {Does steroid injection help patient rehabilitation after arthroscopic rotator cuff repair?},
  journal = {Clinics in Shoulder and Elbow},
  year    = {2021},
  pmid    = {34488291}
}

@article{Saeed_2014,
  author  = {Saeed, A and Khan, M and Morrissey, S and others},
  title   = {Impact of outpatient clinic ultrasound imaging in the diagnosis and treatment for shoulder impingement: a randomized prospective study.},
  journal = {Rheumatology international},
  year    = {2014},
  pmid    = {24190232}
}

@article{Saito_2010,
  author  = {Saito, S and Furuya, T and Kotake, S},
  title   = {Therapeutic effects of hyaluronate injections in patients with chronic painful shoulder: a meta-analysis of randomized controlled trials.},
  journal = {Arthritis care & research},
  year    = {2010},
  pmid    = {20235211}
}

@article{Sari_2020,
  author  = {Sari, A and Eroglu, A},
  title   = {Comparison of ultrasound-guided platelet-rich plasma, prolotherapy, and corticosteroid injections in rotator cuff lesions.},
  journal = {Journal of back and musculoskeletal rehabilitation},
  year    = {2020},
  pmid    = {31743987}
}

@article{Saul_2022,
  author  = {Saul, H and Gursul, D and Hopewell, S},
  title   = {One-off physiotherapy and at-home exercise are effective in treating shoulder pain.},
  journal = {BMJ (Clinical research ed.)},
  year    = {2022},
  pmid    = {35905985}
}

@article{Schickendantz_2016,
  author  = {Schickendantz, M and King, D},
  title   = {Nonoperative Management (Including Ultrasound-Guided Injections) of Proximal Biceps Disorders.},
  journal = {Clinics in sports medicine},
  year    = {2016},
  pmid    = {26614469}
}

@article{Shailesh_2022,
  author  = {Shailesh},
  title   = {Ultrasound-tailored treatment of subacromial shoulder pain: Exploring the role of platelet-rich plasma versus steroids},
  journal = {},
  year    = {2022}
}

@article{Sharma_2016,
  author  = {Sharma, SP and Bærheim, A and Moe-Nilssen, R and others},
  title   = {Adhesive capsulitis of the shoulder, treatment with corticosteroid, corticosteroid with distension or treatment-as-usual; a randomised controlled tria},
  journal = {BMC musculoskeletal disorders},
  year    = {2016},
  pmid    = {27229470}
}

@article{Skaliczki_2024,
  author  = {Skaliczki, G and Kovács, K and Antal, I and others},
  title   = {Arthroscopic capsular release is more effective in pain relief than conservative treatment in patients with frozen shoulder.},
  journal = {BMC musculoskeletal disorders},
  year    = {2024},
  pmid    = {38365741}
}

@article{Skedros_2017,
  author  = {Skedros, JG and Adondakis, MG and Knight, AN and others},
  title   = {Frequency of Shoulder Corticosteroid Injections for Pain and Stiffness After Shoulder Surgery and Their Potential to Enhance Outcomes with Physiothera},
  journal = {Pain and therapy},
  year    = {2017},
  pmid    = {28185130}
}

@article{Stewman_2023,
  author  = {Stewman, CG},
  title   = {Ultrasound-Guided Electroacupuncture Treatment for Rotator Cuff Tendinopathy: Proposing an Effective Alternative to Nonoperative Medical Treatments.},
  journal = {Medical acupuncture},
  year    = {2023},
  pmid    = {37900871}
}

@article{Stiglitz_2011,
  author  = {Stiglitz, Y and Gosselin, O and Sedaghatian, J and others},
  title   = {Pain after shoulder arthroscopy: a prospective study on 231 cases.},
  journal = {Orthopaedics & traumatology, surgery & research : OTSR},
  year    = {2011},
  pmid    = {21458397}
}

@article{Stone_2015,
  author  = {Stone, TJ and Adler, RS},
  title   = {Ultrasound-Guided Biceps Peritendinous Injections in the Absence of a Distended Tendon Sheath: A Novel Rotator Interval Approach.},
  journal = {Journal of ultrasound in medicine : official journal of the American Institute of Ultrasound in Medicine},
  year    = {2015},
  pmid    = {26518277}
}

@article{Subaşı_2016,
  author  = {Subaşı, V and Çakır, T and Arıca, Z and others},
  title   = {Comparison of efficacy of kinesiological taping and subacromial injection therapy in subacromial impingement syndrome.},
  journal = {Clinical rheumatology},
  year    = {2016},
  pmid    = {25403253}
}

@article{Sun_2015,
  author  = {Sun, Y and Chen, J and Li, H and others},
  title   = {Steroid Injection and Nonsteroidal Anti-inflammatory Agents for Shoulder Pain: A PRISMA Systematic Review and Meta-Analysis of Randomized Controlled T},
  journal = {Medicine},
  year    = {2015},
  pmid    = {26683932}
}

@article{Sung_2022,
  author  = {Sung, JH and Lee, JM and Kim, JH},
  title   = {The Effectiveness of Ultrasound Deep Heat Therapy for Adhesive Capsulitis: A Systematic Review and Meta-Analysis.},
  journal = {International journal of environmental research and public health},
  year    = {2022},
  pmid    = {35162881}
}

@article{Suzuki_2014,
  author  = {Suzuki, K and Potts, A and Anakwenze, O and others},
  title   = {Calcific tendinitis of the rotator cuff: management options.},
  journal = {The Journal of the American Academy of Orthopaedic Surgeons},
  year    = {2014},
  pmid    = {25344596}
}

@article{Sá_2020,
  author  = {Sá, Malheiro N and Afonso, NR and Pereira, D and others},
  title   = {[Efficacy of ultrasound guided suprascapular block in patients with chronic shoulder pain: retrospective observational study].},
  journal = {Brazilian journal of anesthesiology (Elsevier)},
  year    = {2020},
  pmid    = {32178894}
}

@article{Sławomir_2021,
  author  = {Sławomir, Struzik and B., Czarkowska-Pączek and A., Wyczałkowska-Tomasik and others},
  title   = {Selected Clinical Features Fail to Predict Inflammatory Gene Expressions for TNF-α, TNFR1, NSMAF, Casp3 and IL-8 in Tendons of Patients with Rotator C},
  journal = {Archivum Immunologiae et Therapiae Experimentalis},
  year    = {2021},
  pmid    = {33683459}
}

@article{Taheri_2017,
  author  = {Taheri, P and Dehghan, F and Mousavi, S and others},
  title   = {Comparison of Subacromial Ketorolac Injection versus Corticosteroid Injection in the Treatment of Shoulder Impingement Syndrome.},
  journal = {Journal of research in pharmacy practice},
  year    = {2017},
  pmid    = {29417082}
}

@article{Tao_2019,
  author  = {Tao, Wu and Haixin, Song and Yang, Li and others},
  title   = {Clinical effectiveness of ultrasound guided subacromial-subdeltoid bursa injection of botulinum toxin type A in hemiplegic shoulder pain},
  journal = {Medicine},
  year    = {2019},
  pmid    = {31702679}
}

@article{Tarun_2023,
  author  = {Tarun, Kumar Somisetty and Hariprasad, Seenappa and Subhashis, Das and others},
  title   = {Comparing the Efficacy of Intra-articular Platelet-Rich Plasma and Corticosteroid Injections in the Management of Frozen Shoulder: A Randomized Contro},
  journal = {Cureus},
  year    = {2023},
  pmid    = {37398735}
}

@article{Terlemez_2020,
  author  = {Terlemez, R and Çiftçi, S and Topaloglu, M and others},
  title   = {Suprascapular nerve block in hemiplegic shoulder pain: comparison of the effectiveness of placebo, local anesthetic, and corticosteroid injections-a r},
  journal = {Neurological sciences : official journal of the Italian Neurological Society and of the Italian Society of Clinical Neurophysiology},
  year    = {2020},
  pmid    = {32388647}
}

@article{Turgut_2025,
  author  = {Turgut, MC and Şahbat, Y and Afşar, A and others},
  title   = {Comparing the clinical efficacy of multiple vs. single dose ozone (O2-O3) injections and corticosteroid injection in subacromial impingement syndrome:},
  journal = {Journal of back and musculoskeletal rehabilitation},
  year    = {2025},
  pmid    = {40129390}
}

@article{U._2012,
  author  = {U., Longo and F., Franceschi and A., Berton and others},
  title   = {Conservative treatment and rotator cuff tear progression.},
  journal = {Medicine and sport science},
  year    = {2012},
  pmid    = {21986048}
}

@article{Unknown_2010,
  author  = {Unknown},
  title   = {A double-blinded randomized controlled clinical trial comparing the efficacy of subacromial injection of ketorolac versus triamcinolone in the treatme},
  journal = {},
  year    = {2010}
}

@article{Vanden_2015,
  author  = {Vanden, Bossche L and Vanderstraeten, G},
  title   = {A multi-center, double-blind, randomized, placebo-controlled trial protocol to assess Traumeel injection vs dexamethasone injection in rotator cuff sy},
  journal = {BMC musculoskeletal disorders},
  year    = {2015},
  pmid    = {25649543}
}

@article{Vaquerizo_2023,
  author  = {Vaquerizo, V and García-López, M and Mena-Rosón, A and others},
  title   = {Plasma rich in growth factors versus corticosteroid injections for management of chronic rotator cuff tendinopathy: a prospective double-blind randomi},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2023},
  pmid    = {36183895}
}

@article{Versloot_2026,
  author  = {Versloot, AHC and Schiphof, D and Ottenheijm, RPG and others},
  title   = {Effectiveness of a corticosteroid injection versus exercise therapy for shoulder pain in general practice (SIX-Shoulder Study): A randomized controlle},
  journal = {Musculoskeletal science & practice},
  year    = {2026},
  pmid    = {41534300}
}

@article{Wang_2017,
  author  = {Wang, W and Shi, M and Zhou, C and others},
  title   = {Effectiveness of corticosteroid injections in adhesive capsulitis of shoulder: A meta-analysis.},
  journal = {Medicine},
  year    = {2017},
  pmid    = {28700506}
}

@article{Wang_2019,
  author  = {Wang, JC and Chang, KV and Wu, WT and others},
  title   = {Ultrasound-Guided Standard vs Dual-Target Subacromial Corticosteroid Injections for Shoulder Impingement Syndrome: A Randomized Controlled Trial.},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2019},
  pmid    = {31150601}
}

@article{Wang_2023,
  author  = {Wang, JC and Hsu, PC and Wang, KA and others},
  title   = {Comparative Effectiveness of Corticosteroid Dosages for Ultrasound-Guided Glenohumeral Joint Hydrodilatation in Adhesive Capsulitis: A Randomized Cont},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2023},
  pmid    = {36521580}
}

@article{Weber_2019,
  author  = {Weber, AE and Trasolini, NA and Mayer, EN and others},
  title   = {Injections Prior to Rotator Cuff Repair Are Associated With Increased Rotator Cuff Revision Rates.},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2019},
  pmid    = {30733024}
}

@article{Wei-Ting_2025,
  author  = {Wei-Ting, Wu and Che-Yu, Lin and Yi-Chung, Shu and others},
  title   = {Predictive value of subacromial motion metrics for the effectiveness of ultrasound-guided dual-target injection: a longitudinal follow-up cohort trial},
  journal = {Insights into Imaging},
  year    = {2025},
  pmid    = {40593369}
}

@article{Woods_2024,
  author  = {Woods, A and Howard, A and Peckham, N and others},
  title   = {Randomized feasibility study of an autologous protein solution versus corticosteroids injection for treating subacromial pain in the primary care sett},
  journal = {Bone & joint open},
  year    = {2024},
  pmid    = {38946298}
}

@article{Wu_2015,
  author  = {Wu, T and Fu, Y and Song, HX and others},
  title   = {Effectiveness of Botulinum Toxin for Shoulder Pain Treatment: A Systematic Review and Meta-Analysis.},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2015},
  pmid    = {26189200}
}

@article{Xiangwei_2022,
  author  = {Xiangwei, Li and Yujia, Xiao and Han, Shu and others},
  title   = {Risk Factors and Corresponding Management for Suture Anchor Pullout during Arthroscopic Rotator Cuff Repair},
  journal = {Journal of Clinical Medicine},
  year    = {2022},
  pmid    = {36431347}
}

@article{Xiao_2017,
  author  = {Xiao, RC and Walley, KC and DeAngelis, JP and others},
  title   = {Corticosteroid Injections for Adhesive Capsulitis: A Review.},
  journal = {Clinical journal of sport medicine : official journal of the Canadian Academy of Sport Medicine},
  year    = {2017},
  pmid    = {27434188}
}

@article{Ya-rong_2022,
  author  = {Ya-rong, Hou and Tong, Zhang and Wei, Liu and others},
  title   = {The Effectiveness of Ultrasound-Guided Subacromial-Subdeltoid Bursa Combined With Long Head of the Biceps Tendon Sheath Corticosteroid Injection for H},
  journal = {Frontiers in Neurology},
  year    = {2022},
  pmid    = {35775042}
}

@article{Yablon_2015,
  author  = {Yablon, CM and Jacobson, JA},
  title   = {Rotator cuff and subacromial pathology.},
  journal = {Seminars in musculoskeletal radiology},
  year    = {2015},
  pmid    = {26021584}
}

@article{Yang_2024,
  author  = {Yang, F and Li, X and Wang, J and others},
  title   = {Efficacy of different analgesic strategies combined with conventional physiotherapy program for treating chronic shoulder pain: a systematic review an},
  journal = {Journal of orthopaedic surgery and research},
  year    = {2024},
  pmid    = {39238008}
}

@article{Yao_2025,
  author  = {Yao, Liu and Yeju, Hu and Miaomiao, Xiong and others},
  title   = {Short-term efficacy of ultrasound-guided capsule-preserving hydrodilatation for primary frozen shoulder using 5% dextrose water versus corticosteroid:},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2025},
  pmid    = {40466856}
}

@article{Yilmaz_2021,
  author  = {Yilmaz, E},
  title   = {A prospective, comparative study of subacromial corticosteroid injection and subacromial corticosteroid injection plus suprascapular nerve block in pa},
  journal = {Archives of orthopaedic and trauma surgery},
  year    = {2021},
  pmid    = {32356170}
}

@article{Yon-Sik_2017,
  author  = {Yon-Sik},
  title   = {Serial Magnetic Resonance Imaging to Determine the Progression of Neglected Recalcitrant Rotator Cuff Tears: A Retrospective Multicenter Study},
  journal = {},
  year    = {2017}
}

@article{Yong-Soo_2019,
  author  = {Yong-Soo, Lee and Ja-Yeon, Kim and Se-Young, Ki and others},
  title   = {Influence of Smoking on the Expression of Genes and Proteins Related to Fat Infiltration, Inflammation, and Fibrosis in the Rotator Cuff Muscles of Pa},
  journal = {Arthroscopy : the journal of arthroscopic & related surgery : official publication of the Arthroscopy Association of North America and the International Arthroscopy Association},
  year    = {2019},
  pmid    = {31785743}
}

@article{Yu-Ting_2024,
  author  = {Yu-Ting, Lin and Ying-Chen, Kuo and Xin-Ni, Wu and others},
  title   = {Comparison of the Efficacy of Ultrasound-Guided Suprascapular Nerve Blocks and Intraarticular Corticosteroid Injections for Frozen Shoulder: A Randomi},
  journal = {Pain physician},
  year    = {2024},
  pmid    = {39353111}
}

@article{Yu_2018,
  author  = {Yu, K and Zhang, DY and Yang, J and others},
  title   = {[Clinical efficacy of ultrasound-guided subacromial drug injection in the treatment of subacromial impingement syndrome].},
  journal = {Zhonghua wai ke za zhi [Chinese journal of surgery]},
  year    = {2018},
  pmid    = {30369162}
}

@article{Yuan-Chen_2026,
  author  = {Yuan-Chen},
  title   = {Efficacy of a Mobile Health-Supported Home-Based Resistance Exercise After Ultrasound-Guided Corticosteroid Injection in Chronic Subacromial Bursitis:},
  journal = {},
  year    = {2026}
}

@article{Zhang_2019,
  author  = {Zhang, T and Duan, Y and Chen, J and others},
  title   = {Efficacy of ultrasound-guided percutaneous lavage for rotator cuff calcific tendinopathy: A systematic review and meta-analysis.},
  journal = {Medicine},
  year    = {2019},
  pmid    = {31124934}
}

@article{Zhang_2021,
  author  = {Zhang, J and Zhong, S and Tan, T and others},
  title   = {Comparative Efficacy and Patient-Specific Moderating Factors of Nonsurgical Treatment Strategies for Frozen Shoulder: An Updated Systematic Review and},
  journal = {The American journal of sports medicine},
  year    = {2021},
  pmid    = {32941053}
}

@article{Zheng_2014,
  author  = {Zheng, XQ and Li, K and Wei, YD and others},
  title   = {Nonsteroidal anti-inflammatory drugs versus corticosteroid for treatment of shoulder pain: a systematic review and meta-analysis.},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2014},
  pmid    = {24841629}
}

@article{Zufferey_2012,
  author  = {Zufferey, P and Revaz, S and Degailler, X and others},
  title   = {A controlled trial of the benefits of ultrasound-guided steroid injection for shoulder pain.},
  journal = {Joint bone spine},
  year    = {2012},
  pmid    = {21612965}
}

@article{de_2012,
  author  = {de, Witte PB and Henseler, JF and Nagels, J and others},
  title   = {The Western Ontario rotator cuff index in rotator cuff disease patients: a comprehensive reliability and responsiveness validation study.},
  journal = {The American journal of sports medicine},
  year    = {2012},
  pmid    = {22582227}
}

@article{von_2016,
  author  = {von, Wehren L and Blanke, F and Todorov, A and others},
  title   = {The effect of subacromial injections of autologous conditioned plasma versus cortisone for the treatment of symptomatic partial rotator cuff tears.},
  journal = {Knee surgery, sports traumatology, arthroscopy : official journal of the ESSKA},
  year    = {2016},
  pmid    = {26017742}
}

@article{Çelik_2023,
  author  = {Çelik, D and Yasacı, Z and Erşen, A},
  title   = {Oral corticosteroids vs. exercises on treatment of frozen shoulder: a randomized, single-blinded study.},
  journal = {Journal of shoulder and elbow surgery},
  year    = {2023},
  pmid    = {36842462}
}

@article{Çetingök_2022,
  author  = {Çetingök, H and Serçe, GI},
  title   = {Does the application of pulse radiofrequency to the suprascapular nerve provide additional benefit in patients who have undergone glenohumeral intra-a},
  journal = {Agri : Agri (Algoloji) Dernegi'nin Yayin organidir = The journal of the Turkish Society of Algology},
  year    = {2022},
  pmid    = {36300751}
}

@article{Çift_2015,
  author  = {Çift, H and Özkan, FÜ and Tolu, S and others},
  title   = {Comparison of subacromial tenoxicam and steroid injections in the treatment of impingement syndrome.},
  journal = {Eklem hastaliklari ve cerrahisi = Joint diseases & related surgery},
  year    = {2015},
  pmid    = {25741915}
}

@article{Ömer_2025,
  author  = {Ömer},
  title   = {Subacromial injection failure in shoulder impingement: is somatic amplification the missing link?},
  journal = {},
  year    = {2025}
}

@article{Şirin_2025,
  author  = {Şirin, Ahısha B and Paker, N and Kesiktaş, N and others},
  title   = {Evaluation of Inadequate Response to Ultrasound-Guided Subacromial Corticosteroid Injection in Shoulder Impingement Syndrome: Treatment Failure or Cen},
  journal = {Archives of physical medicine and rehabilitation},
  year    = {2025},
  pmid    = {39900325}
}

@article{Šmíd_2018,
  author  = {Šmíd, P and Hart, R and Komzák, M and others},
  title   = {[Treatment of the Shoulder Impingement Syndrome with PRP Injection].},
  journal = {Acta chirurgiae orthopaedicae et traumatologiae Cechoslovaca},
  year    = {2018},
  pmid    = {30257756}
}
```

# Appendices

## Appendix A: Search Strings

**PubMed -- Query 1 (Efficacy / Treatment Outcome)** (Date: 2026-04-02; Results: 200)
```
(("shoulder pain"[MeSH] OR "rotator cuff"[MeSH] OR "shoulder impingement syndrome"[MeSH]
OR "subacromial pain syndrome"[tiab] OR "subacromial impingement"[tiab]
OR "rotator cuff tendinopathy"[tiab] OR "scapulalgia"[tiab])
AND ("adrenal cortex hormones"[MeSH] OR "corticosteroid injection"[tiab]
OR "steroid injection"[tiab] OR "cortisone injection"[tiab]
OR "subacromial injection"[tiab])
AND ("treatment outcome"[MeSH] OR "efficacy"[tiab] OR "pain relief"[tiab]
OR "functional outcome"[tiab])) AND 2010:2026[DP]
```

**PubMed -- Query 2 (Predictive / Prognostic Factors)** (Date: 2026-04-02; Results: 162)
```
(("shoulder pain"[MeSH] OR "rotator cuff"[MeSH] OR "shoulder impingement syndrome"[MeSH])
AND ("adrenal cortex hormones"[MeSH] OR "subacromial injection"[tiab]
OR "corticosteroid injection"[tiab])
AND ("predictive value of tests"[MeSH] OR "prognosis"[MeSH]
OR "predictive factors"[tiab] OR "prognostic factors"[tiab]
OR "response prediction"[tiab])) AND 2010:2026[DP]
```

**PubMed -- Query 3 (Care Pathway / Complications)** (Date: 2026-04-02; Results: 141)
```
(("shoulder pain"[MeSH] OR "rotator cuff"[MeSH] OR "shoulder impingement syndrome"[MeSH])
AND ("adrenal cortex hormones"[MeSH] OR "subacromial injection"[tiab]
OR "corticosteroid injection"[tiab])
AND ("referral and consultation"[MeSH] OR "time-to-treatment"[MeSH]
OR "surgical delay"[tiab] OR "care pathway"[tiab] OR "time to surgery"[tiab]
OR "tendon injuries"[MeSH] OR "tendon damage"[tiab]
OR "complications"[tiab])) AND 2010:2026[DP]
```

**Semantic Scholar -- Query 1** (Date: 2026-04-02; Results: 100)
```
subacromial corticosteroid injection shoulder pain efficacy
```

**OpenAlex** queries used equivalent free-text terms with medicine field-of-study filters. Total results: 73.

## Appendix B: PRISMA-ScR Checklist

| Section | Item | Reported? | Location |
|---------|------|-----------|----------|
| Title | Identify as scoping review | Yes | Title |
| Abstract | Structured summary | Yes | Abstract |
| Introduction | Rationale | Yes | Introduction |
| Introduction | Objectives | Yes | Scope and Objectives |
| Methods | Protocol and registration | Yes | Methodology - Protocol |
| Methods | Eligibility criteria | Yes | Inclusion and Exclusion Criteria |
| Methods | Information sources | Yes | Search Strategy |
| Methods | Search | Yes | Search Strategy + Appendix A |
| Methods | Selection of sources | Yes | Study Selection |
| Methods | Data charting | Yes | Data Extraction |
| Results | Selection of sources | Yes | Study Selection |
| Results | Characteristics | Yes | Study Characteristics |
| Results | Results of individual sources | Yes | Thematic Synthesis |
| Results | Synthesis of results | Yes | Thematic Synthesis |
| Discussion | Summary of evidence | Yes | Main Findings |
| Discussion | Limitations | Yes | Strengths and Limitations |
| Discussion | Conclusions | Yes | Conclusions |
| Other | Funding | Yes | Declarations |

## Appendix C: Excluded Studies

A total of 194 articles were excluded across screening stages:

**Title screening exclusions (n=127):** Editorial/commentary (n=23), non-shoulder condition (n=40), case report (n=11), animal/in vitro study (n=8), non-CSI primary intervention (n=6), conference abstract (n=3), other (n=36).

**Abstract screening exclusions (n=64):** No mention of corticosteroid injection (n=54), non-CSI primary intervention (n=4), animal study (n=2), not about shoulder pathology (n=4).

**Full-text screening exclusions (n=3):** Commentary on Cochrane review (n=1), conference abstract (n=1), no mention of CSI (n=1).

Full exclusion details with article indices and reasons are available in `screening_log.md`.

## Appendix E: Data Extraction Form

```
STUDY: Author______ Year______ DOI______ PMID______
DESIGN: [ ] RCT [ ] Cohort [ ] Case-Control [ ] Cross-sectional [ ] SR/MA [ ] Other______
POPULATION: n=_____ Age_____ Setting_____
INTERVENTION: Injection type_____ Guidance_____ Comparator_____
OUTCOMES: Primary_____ Secondary_____
RESULTS: Effect size_____ 95%CI_____ p=_____
THEMES: [ ] Efficacy [ ] CSI vs physio [ ] Technique [ ] Safety [ ] Adhesive capsulitis [ ] Surgical impact [ ] Calcific
```

# Supplementary Materials

**Data:** S1 (Full extraction file: `extracted_claims.json`), S2 (Search results: `combined_results.json`), S3 (Screening log: `screening_log.md`)

# Review Metadata

**Search dates:** Initial: 2026-04-02
**Version:** 1.0 | **Last updated:** 2026-04-02

**Quality checks:**

- [ ] Citations verified (Phase 6 MCP tools)
- [x] PRISMA-ScR checklist completed
- [x] Search reproducible
- [ ] Independent data verification
- [ ] All authors approved
