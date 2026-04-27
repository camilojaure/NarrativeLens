# NarrativeLens

**Master's Thesis — Management & Analytics, ITBA (2025)**
*Camilo Jaureguiberry*

---

## Research Overview

This repository contains the full analysis supporting the thesis:

> **"Creative Diversity and Ad Performance on TikTok: An Analysis of CDS Dimensions and CTR"**

**Research question:** Which creative dimensions are associated with higher click-through rate (CTR) in TikTok paid social campaigns, and can this relationship be identified reliably enough to guide creative strategists?

**Methodology:** OLS regression + Random Forest with SHAP values on 578 TikTok Top Ads. Both models cross-validate findings: OLS provides interpretable coefficients; RF + SHAP captures non-linearities without distributional assumptions. Convergence between models (Spearman ρ = 0.74, p < 0.0001) constitutes robust evidence independent of each model's assumptions (Breiman, 2001).

**Key results:**
- OLS R² out-of-sample (5-fold CV): 0.496 ± 0.07
- RF R² out-of-sample (5-fold CV): 0.519 ± 0.14
- Top predictors of CTR: `creative_theme` → `talent_type` → `creative_concept`
- Strongest finding: *Humor & Entertainment* is the highest-SHAP predictor — negatively associated with CTR — a counterintuitive result for TikTok that warrants discussion.

---

## Repository Structure

```
NarrativeLens/
├── regression_analysis.ipynb   ← main analysis: OLS, Random Forest, SHAP
├── eda.ipynb                   ← exploratory data analysis
│
├── data/
│   └── datasets/               ← tiktok_topads_clean.csv (578 ads)
│
├── pipeline/                   ← data extraction & ETL scripts
│   ├── feature_extractor.py    ← Gemini API: multimodal classification of 8 CDS dimensions
│   ├── ugc_detector.py         ← UGC classification
│   ├── etl.py                  ← MongoDB → CSV transformation
│   ├── data_model.py           ← Pydantic validation (AdAnalysis model)
│   └── prompts/                ← Gemini prompt templates
│
├── thesis/                     ← thesis document (LaTeX + PDF), research papers, pre-dictámenes
├── docs/                       ← architecture diagrams
└── archive/                    ← previous notebook versions, early POCs
```

---

## About the Name

**NarrativeLens** is the name given to the system built to implement the findings of this research — a tool that classifies ad creative dimensions and benchmarks them against high-performing campaigns. The research in this repository constitutes the analytical foundation for that product.

---

## Data Pipeline

```
TikTok Top Ads (~578 videos)
    ↓ pipeline/feature_extractor.py
Gemini API → multimodal classification of 8 creative dimensions
    ↓ Pydantic validation (pipeline/data_model.py)
MongoDB
    ↓ pipeline/ugc_detector.py
MongoDB updated with is_ugc flag
    ↓ pipeline/etl.py
data/datasets/tiktok_topads_clean.csv
    ↓ eda.ipynb → regression_analysis.ipynb
OLS + Random Forest + SHAP → thesis results
```

---

## Setup

```bash
source .venv/bin/activate
jupyter notebook
```
