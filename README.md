# CSU MRI Iron Nanoparticle Radiomics Study

Canine head-and-neck lymph node characterisation with **multi-sequence MRI** and PyRadiomics features.

**Authors:** Christopher J. Pinard, Tyler J. Poore, Aleena Shabbir, Nolan Chai, Markus Gruendler,
Kuan-Chuen Wu, and Lynn Griffin.

> **One-line summary:** Across 29 dogs / 171 lymph nodes, a histology-trained radiomics model gives
> *modest and not-yet-statistically-credible* discrimination of metastatic from normal nodes
> (best classifier Linear SVM, LODO-CV AUC = 0.62, 95% CI 0.38–0.87, permutation p ≈ 0.10). The
> **subjective radiologist read remains the strongest classifier** (accuracy 90%, κ = 0.65; McNemar
> p < 0.001 vs the model), and no reader+model combination beats it.

---

## Cohort

| Cohort | Dogs | Lymph nodes | Metastatic (M) | Sequences |
|---|---|---|---|---|
| Year 1 (D1–D12) | 12 | 74 | 18 | T1, T2, T1P, GE |
| Year 2 (Y2 D1–D12) | 12 | 73 | 6 | T1, T2, T1P, GE (Y2 D12 no T1P) |
| CRC model (CRC D2–D6) | 5 | 24 | 7 | T1, T2, T1P, GE |
| **Total** | **29** | **171** | **31 (18.1%)** | 4 sequences |

Each lymph node is described by `original` PyRadiomics features from **four MRI sequences**
(T1, T2, T1-post = `T1P`, gradient-echo = `GE`), concatenated into one ~428-feature vector. Labels are
read from the *Summary* sheet of `patient_data_labels.xlsx`: `histo_M` (histopathology ground truth;
Metastatic → 1, Normal/Reactive/Hyperplasia → 0) and `imaging_M` (the radiologist's subjective M/NM read).
164 of 171 nodes carry a radiologist call; metastatic nodes sit in 11 of 29 dogs.

---

## Aims & current status

1. **Aim 1** — Identify MRI radiomic features that distinguish histologically normal from metastatic
   regional lymph nodes. — ✅ **Implemented** (classifier comparison + explainability).
2. **Aim 2** — Correlate radiomic features with PSIL (post-injection signal-intensity loss; quantitative
   iron nanoparticle uptake). — ⏳ **Not in current notebook.** PSIL is absent from the `FINAL_DATA`
   label set; it was only ever measured for the original 5 Year-1 dogs (~30 nodes). Restorable for that
   subset only.
3. **Aim 3** — Determine whether primary tumour radiomic features predict lymph node metastatic burden.
   — ⏳ **Not in current notebook.** Only 3 dogs (D7, D11, D12) have a primary-tumour contour in
   `FINAL_DATA`; descriptive at best.

---

## Methodology (Aim 1)

### Validation
- **Leave-One-Dog-Out Cross-Validation (LODO-CV)** — 29 folds; the *dog*, not the node, is the held-out
  unit, and a leakage audit confirms no dog or row appears in both train and test.
- **Within-fold pipeline (fit on training dogs only):** median imputation → near-zero-variance drop →
  correlation filter (|r| > 0.95) → **univariate top-10 screen** (training-fold AUC vs `histo_M`) →
  standardise → classifier, with the **decision threshold tuned by Youden's J** on the training fold.

### Classifiers compared
L1-penalised **Logistic Regression**, **Linear SVM**, **Random Forest**, and **XGBoost**, all made
cost-sensitive (`class_weight='balanced'`; `scale_pos_weight` for XGBoost). SMOTE / random oversampling
were tested and did not improve on class-weighting, so weighting is used throughout.

### Uncertainty & significance
- **Dog-level (cluster) bootstrap 95% CIs** on every metric (dogs, not nodes, are resampled).
- **Permutation test (200 shuffles)** — the entire selection+classification pipeline is re-run on shuffled
  labels, so the null accounts for the optimism of in-fold feature selection.

---

## Headline Results

### Classifier comparison (LODO-CV)

| Classifier | AUC | 95% CI | Sensitivity | Specificity | Accuracy |
|---|---|---|---|---|---|
| **Linear SVM** (best) | **0.623** | [0.38, 0.87] | 41.9% | 84.3% | 76.6% |
| Logistic (L1) | 0.592 | [0.35, 0.85] | 41.9% | 85.7% | 77.8% |
| XGBoost | 0.590 | [0.37, 0.84] | 19.4% | 96.4% | 82.5% |
| Random Forest | 0.588 | [0.34, 0.85] | 38.7% | 85.7% | 77.2% |

All four CIs span 0.5, and the best model's **permutation p ≈ 0.10 (not significant)** — the bottleneck is
sample size (31 events, features ≫ samples), not the algorithm.

### Explainability — what drives the predictions

The reproducible signal is essentially **"big, bright, heterogeneous node"**: node short-axis **size**
(`shape_LeastAxisLength`, selected in 28/29 folds) together with **large-area / large-dependence
high-gray-level texture** (`glszm`/`gldm`, univariate AUC ≈ 0.79, FDR q < 0.001). Because size is exactly
the cue the radiologist already uses, the model carries little *independent* information.

### Radiologist vs model (164 nodes with a radiologist call)

| Reader | Sensitivity | Specificity | Accuracy | AUC |
|---|---|---|---|---|
| **Radiologist** (subjective MRI) | 0.724 | 0.933 | **0.896** | — |
| Radiomics model (Linear SVM) | 0.379 | 0.837 | 0.756 | 0.601 |

McNemar p < 0.001 — the radiologist is significantly better. Reader+model combinations (OR / AND /
logistic stack) **do not beat the radiologist alone**: the model recovers 0 of the 8 metastases the
radiologist missed (shared false negatives); its only value is on the negative class (the AND rule raises
specificity to 0.96).

---

## Key Limitations

- **Severely under-powered (p ≫ n):** 31 metastatic events, 428 features (events-per-variable ≈ 0.07).
  This is a **proof-of-concept**, not a validated model; CIs are wide by necessity.
- **Cross-cohort batch effect:** raw MRI intensity differs ~5× across CRC / Year-1 / Year-2 (e.g. T1
  first-order mean medians 2571 / 525 / 568). Intensity normalisation / ComBat is the highest-value fix.
- **Small nodes:** 57/171 nodes < 500 mm³ (16 < 250 mm³); texture features unstable at that size.
- **Label heterogeneity:** CRC histology (Hyperplasia/Reactive/Normal/Metastatic) collapsed to NM/M;
  reactive/hyperplastic nodes enlarge and enhance — the natural false-positive trap for both readers.
- **Outlier dogs:** D12 (occult-metastatic, 5/6 M missed by radiologist *and* model) and CRC D4 (6 of 31
  positives in one dog) dominate the error and the positive class.

---

## Recommended Next Steps

1. **Harmonise intensities** (ComBat / per-image z-score) before re-extracting features.
2. **Enrich the positive class** (more metastatic nodes / external cohort) toward credible discrimination.
3. **Restore Aims 2 & 3** as the data allow: PSIL correlation for the 5 original Year-1 dogs, and a
   descriptive primary-tumour vs nodal-burden analysis for D7/D11/D12 (completing more primary contours
   would strengthen it).
4. Robustness analyses: exclude < 250 mm³ nodes; exclude reactive/hyperplastic CRC nodes; D12 case study.
5. Position radiomics as a **specificity aid** (AND-style confirmation), not a standalone replacement.

---

## Repository Layout

```
.
|-- main.ipynb              # Primary analysis notebook (Aim 1: data, models, explainability, radiologist)
|-- make_summary.py         # Builds study_summary.html from summary_figures/
|-- study_summary.html      # Standalone HTML report (figures embedded as base64)
|-- summary_figures/        # fig1..fig7 PNGs exported from the notebook
|-- Results/                # Selected legacy figures + text dumps from earlier runs
`-- Data/                   # PyRadiomics CSVs + patient_data_labels.xlsx (NOT pushed to GitHub)
```

The `Data/` folder contains protected patient information and is excluded via `.gitignore`.

---

## Reproducing

Requirements: Python 3.11+, `pandas`, `numpy`, `scikit-learn>=1.5`, `imbalanced-learn`, `xgboost`,
`matplotlib`, `seaborn`, `scipy`, `openpyxl`.

```bash
jupyter nbconvert --to notebook --execute main.ipynb --inplace
python make_summary.py    # regenerates study_summary.html from the exported figures
```

PyRadiomics CSVs and `patient_data_labels.xlsx` must be present in `Data/FINAL_DATA/`; obtain them from
the study coordinators.

---

## Citation / contact

CSU Iron Nanoparticle (Ferumoxytol) Radiomics Study — Pinard CJ, Poore TJ, Shabbir A, Chai N,
Gruendler M, Wu K-C, Griffin L. ANI-ML / Animl Health collaboration with Colorado State University.
