# CSU MRI Iron Nanoparticle Radiomics Study

Canine head-and-neck lymph node characterisation with **post-ferumoxytol** MRI and PyRadiomics features.

> **One-line summary:** Across 12 dogs / 73 lymph nodes, post-iron MRI radiomics provide *modest* and *not-yet-statistically-credible* discrimination of metastatic from normal nodes (Random-Forest LODO-CV AUC = 0.574, permutation p = 0.184). Subjective radiologist read remains the strongest classifier (kappa = 0.620).

---

## Cohort

| Cohort | Dogs | LNs | Histo M | Histo NM | PSIL? |
|---|---|---|---|---|---|
| Year 1 | 7, 8, 9, 10, 11, 12 | 37 | 17 | 20 | yes (5/6) |
| Year 2 | 20-25 (Y2D1-Y2D6) | 36 | 3 | 33 | no |
| **Total** | **12** | **73** | **20** | **53** | mixed |

All MRI contours were drawn on the **post-ferumoxytol** acquisition. The 107 PyRadiomics features therefore describe each node *after* iron uptake. Functional macrophages in normal nodes phagocytose ferumoxytol, producing a marked T2*-weighted signal-intensity drop; metastatic nodes have impaired or displaced macrophage populations and retain higher signal. Histopathologically NM nodes are the ground-truth reference; M nodes are the class of clinical interest.

---

## Aims

1. **Aim 1** - Identify MRI radiomic features that distinguish histologically normal from metastatic regional lymph nodes.
2. **Aim 2** - Correlate radiomic features with PSIL (post-injection signal-intensity loss; quantitative iron nanoparticle uptake). *Year 1 only - Year 2 lacks pre-iron acquisition.*
3. **Aim 3** - Determine whether primary tumour radiomic features predict lymph node metastatic burden.

---

## Methodology

### Validation
- **Leave-One-Dog-Out Cross-Validation (LODO-CV)** - 12 folds for Aim 1, 5 folds for Aim 2.
- **Correctness audit** - across all 12 folds, no dog and no row index appears in both train and held-out sets. **PASSED.**
- **Within-fold pipeline:** median imputation -> variance threshold -> correlation filter (r > 0.95) -> standard scaling -> *(optional SMOTE)* -> classifier. All filters fit on training nodes only.

### Class-imbalance handling (Aim 1)
Three training strategies compared head-to-head:
- baseline,
- `class_weight="balanced"` (inverse-frequency loss weights),
- **SMOTE within fold** (synthetic minority oversampling on training set only - test data is never resampled).

### Statistical significance
- **Permutation test (200 shuffles):** histopathology labels permuted, full LODO-CV pipeline re-run for each shuffle, observed AUC compared to the empirical null distribution.

---

## Headline Results

### Aim 1 - NM vs M classification (12 dogs, 73 LNs)

| Model | AUC | Sensitivity | Specificity |
|---|---|---|---|
| Logistic Regression | 0.234 | 10.0% | 81.1% |
| Linear SVM | 0.273 | 10.0% | 81.1% |
| **Random Forest** | **0.574** | 25.0% | 75.5% |

Class-imbalance comparison (Random Forest):

| Strategy | AUC |
|---|---|
| Baseline | **0.574** |
| Class-weighted (`balanced`) | 0.532 |
| SMOTE within fold | 0.516 |

Class-weighting and SMOTE did **not** improve AUC, suggesting the bottleneck is radiomic signal-to-noise at the current sample size, not the imbalance per se.

**Permutation test:**

| | Value |
|---|---|
| Observed RF AUC | 0.574 |
| Null mean | 0.476 |
| Null 95th percentile | 0.638 |
| **Empirical p-value** | **0.184** |

The observed AUC lies **inside** the empirical null distribution. At n = 12 dogs / 73 LNs, radiomic models do not yet provide statistically credible discrimination under leave-one-dog-out validation.

### Aim 2 - PSIL regression (Year 1 only, 30 LNs)

All four regressors (Ridge, Lasso, SVR, Random Forest) had **negative R^2** under LODO-CV - none beat predicting the mean PSIL for every node. Zero univariate features survive Bonferroni correction across the 107 Spearman tests.

### Aim 3 - Primary tumour vs LN metastatic burden (n = 4 dogs)

Hypothesis-generating only. With four dogs (Dogs 7, 11, 12, Y2D3), the maximum achievable Spearman |r| is 1.0 by construction. Top features are first-order intensity statistics and GLCM/GLRLM textures, but no statistical conclusions can be drawn at this sample size.

### Supplementary - Subjective MRI vs histopathology

| Method | Sensitivity | Specificity | Accuracy | Cohen's kappa |
|---|---|---|---|---|
| Subjective radiologist read | 60.0% | 96.2% | 86.3% | **0.620** |
| PSIL threshold (Year 1 only) | 25.0% | 100% | 70.0% | - |

The radiologist read continues to outperform every radiomic model on the expanded cohort.

---

## Key Limitations

- **Sample size:** 12 dogs / 73 LNs - LODO-CV variance remains high; external validation is not yet possible.
- **Dog-dominated variance:** PCA shows inter-dog variation exceeding class-related variation.
- **Class imbalance:** 53 NM vs 20 M (73% NM) inflates accuracy/specificity.
- **All-NM dogs (9, 11, 21, 22, 24, 25):** these six folds trivially inflate specificity and cannot be used to estimate per-dog sensitivity.
- **Year 2 PSIL absent:** Aim 2 limited to Year 1 (30 LNs); adding post-iron acquisitions to Year 2 is the highest-yield improvement.
- **Tumour heterogeneity:** cohort spans MCT, OMM, melanoma, FSA, STS, fibrosarcoma.
- **Single MRI sequence:** post-ferumoxytol only; pre/post delta features and multi-parametric (T2*, DWI) sequences may improve discrimination.

---

## Recommended Next Steps

1. Extend Year 2 acquisitions to include post-ferumoxytol imaging so PSIL can be computed (would roughly double the Aim 2 sample).
2. Continue cohort expansion toward >= 20 dogs to push Aim 1 LODO-CV beyond modest discrimination.
3. Include multi-parametric sequences (T2*, DWI) in radiomic extraction.
4. Harmonise MRI acquisition (or apply ComBat-style harmonisation post-hoc) to reduce inter-dog radiomic variance.
5. Complete primary tumour segmentations for the remaining dogs (8, 9, 10, 20, 21, 23, 24, 25) for a meaningful Aim 3.

---

## Repository Layout

```
.
|-- main.ipynb              # Primary analysis notebook (3 aims + audit + permutation test)
|-- make_summary.py         # Builds study_summary.html from summary_figures/
|-- study_summary.html      # Standalone HTML report (figures embedded as base64)
|-- summary_figures/        # PNGs of every published figure
|-- Results/                # Selected legacy figures + text dump from earlier runs
`-- Data/                   # PyRadiomics CSVs + Patient summaries.xlsx (NOT pushed to GitHub)
```

The `Data/` folder contains protected patient information and is excluded via `.gitignore`.

---

## Reproducing

Requirements: Python 3.11+, `pandas`, `scikit-learn>=1.5`, `imbalanced-learn`, `matplotlib`, `seaborn`, `scipy`, `openpyxl`.

```bash
jupyter nbconvert --to notebook --execute main.ipynb --inplace
python make_summary.py    # regenerates study_summary.html
```

PyRadiomics CSVs and the patient-summary spreadsheet must be present in `Data/`; obtain them from the study coordinators.

---

## Citation / contact

CSU Iron Nanoparticle (Ferumoxytol) Radiomics Study
ANI-ML / Animl Health collaboration with Colorado State University.
