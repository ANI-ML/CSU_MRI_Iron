import base64, os

fig_dir = 'c:/Users/sshuser/Documents/CSU_Iron/summary_figures'
figs = {}
for fname in sorted(os.listdir(fig_dir)):
    if fname.endswith('.png'):
        key = fname.replace('.png','')
        with open(os.path.join(fig_dir, fname), 'rb') as f:
            figs[key] = base64.b64encode(f.read()).decode()

def img(key, caption):
    return (
        '\n<figure>\n'
        f'<img src="data:image/png;base64,{figs[key]}" alt="{caption}" style="max-width:100%;border:1px solid #ddd;border-radius:4px;">\n'
        f'<figcaption>{caption}</figcaption>\n'
        '</figure>\n'
    )

CSS = """
  body{font-family:Georgia,serif;max-width:960px;margin:40px auto;padding:0 20px;line-height:1.7;color:#222}
  h1{color:#1a3a5c;border-bottom:3px solid #1a3a5c;padding-bottom:8px}
  h2{color:#1a3a5c;margin-top:2em;border-bottom:1px solid #aac;padding-bottom:4px}
  h3{color:#2c5f8a}
  table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.93em}
  th{background:#1a3a5c;color:#fff;padding:8px 12px;text-align:left}
  td{padding:7px 12px;border-bottom:1px solid #dde}
  tr:nth-child(even){background:#f5f8fb}
  figure{margin:1.5em 0}
  figcaption{font-size:.88em;color:#555;font-style:italic;margin-top:6px;text-align:center}
  .callout{background:#eef4fb;border-left:4px solid #2c5f8a;padding:10px 16px;margin:1em 0;border-radius:0 4px 4px 0}
  .warning{background:#fff8e1;border-left:4px solid #f5a623;padding:10px 16px;margin:1em 0;border-radius:0 4px 4px 0}
  .bad{color:#b33;font-weight:bold}
  .ok{color:#a86b00;font-weight:bold}
  .good{color:#2a7a2a;font-weight:bold}
  code{background:#f0f0f0;padding:1px 4px;border-radius:3px;font-size:.9em}
  ul li,ol li{margin-bottom:.3em}
"""

HEADER = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CSU Iron Nanoparticle Radiomics Study</title>
<style>{CSS}</style>
</head>
<body>
<h1>CSU Iron Nanoparticle (Ferumoxytol) Radiomics Study</h1>
<p><em>Canine Head-and-Neck Lymph Node Characterisation &mdash; Year 1 Dogs 7&ndash;12 + Year 2 Dogs 20&ndash;25 (Y2D1&ndash;Y2D6)</em></p>
<p style="color:#666;font-size:.92em">Generated from <code>main.ipynb</code> &middot; April 2026</p>
<div class="callout">
<strong>Study in brief:</strong> This pilot study investigates whether <strong>post-ferumoxytol</strong> MRI radiomic features can
(1) classify regional lymph nodes as metastatic or normal,
(2) predict ferumoxytol (iron nanoparticle) uptake measured by post-injection signal intensity loss (PSIL), and
(3) link primary tumour texture to lymph node metastatic burden &mdash;
in an expanded cohort of 12 dogs with head-and-neck cancers (6 Year 1 + 6 Year 2).
</div>
<div class="callout">
<strong>Imaging protocol &mdash; key framing:</strong> All lymph-node and tumour contours were drawn on the <strong>post-injection</strong> (post-ferumoxytol) MRI for every dog,
so the 107 PyRadiomics features describe each node <em>after</em> iron uptake. Functional macrophages in normal nodes phagocytose ferumoxytol, producing
a marked signal-intensity drop on T2*-weighted images; metastatic nodes have impaired or displaced macrophage populations and retain higher signal.
The biological signal therefore lives primarily in <strong>intensity-related features</strong> (first-order Mean / Median / RootMeanSquared / percentiles
and signal-magnitude GLCM features such as Autocorrelation, JointAverage, SumAverage): NM nodes should appear darker and more uniform, M nodes brighter and more heterogeneous.
Histopathologically NM nodes are the ground-truth reference; M nodes are the class of clinical interest.
</div>
"""

SEC1 = """
<h2>1. Study Design &amp; Dataset</h2>
<h3>Objectives</h3>
<ul>
<li><strong>Aim 1</strong> &mdash; Identify MRI radiomic features that distinguish histologically normal from metastatic regional lymph nodes.</li>
<li><strong>Aim 2</strong> &mdash; Correlate radiomic features with PSIL (quantitative iron nanoparticle uptake).</li>
<li><strong>Aim 3</strong> &mdash; Determine whether primary tumour radiomic features predict lymph node metastatic burden.</li>
</ul>
<h3>Cohort Summary</h3>
<table>
<tr><th>Dog</th><th>Cohort</th><th>Total LNs</th><th>Histo M</th><th>Histo NM</th><th>Mean PSIL</th><th>Notes</th></tr>
<tr><td>7</td><td>Year 1</td><td>6</td><td>2</td><td>4</td><td>&minus;0.389</td><td>&mdash;</td></tr>
<tr><td>8</td><td>Year 1</td><td>6</td><td>5</td><td>1</td><td>&minus;0.488</td><td>&mdash;</td></tr>
<tr><td>9</td><td>Year 1</td><td>6</td><td>0</td><td>6</td><td>&minus;0.654</td><td>All NM</td></tr>
<tr><td>10</td><td>Year 1</td><td>7</td><td>5</td><td>2</td><td>N/A</td><td>No PSIL; extra LparLN</td></tr>
<tr><td>11</td><td>Year 1</td><td>6</td><td>0</td><td>6</td><td>&minus;0.603</td><td>All NM</td></tr>
<tr><td>12</td><td>Year 1</td><td>6</td><td>5</td><td>1</td><td>&minus;0.532</td><td>LMLN1 discordancy (see note)</td></tr>
<tr><td>20 (Y2D1)</td><td>Year 2</td><td>6</td><td>2</td><td>4</td><td>N/A</td><td>Melanoma; no PSIL</td></tr>
<tr><td>21 (Y2D2)</td><td>Year 2</td><td>6</td><td>0</td><td>6</td><td>N/A</td><td>OMM; all NM; no PSIL</td></tr>
<tr><td>22 (Y2D3)</td><td>Year 2</td><td>6</td><td>0</td><td>6</td><td>N/A</td><td>GIII STS; all NM; primary contoured</td></tr>
<tr><td>23 (Y2D4)</td><td>Year 2</td><td>6</td><td>1</td><td>5</td><td>N/A</td><td>Melanoma; LMLN2 imaging-NM/histo-M</td></tr>
<tr><td>24 (Y2D5)</td><td>Year 2</td><td>6</td><td>0</td><td>6</td><td>N/A</td><td>Melanoma; RRPLN imaging-M/histo-NM</td></tr>
<tr><td>25 (Y2D6)</td><td>Year 2</td><td>6</td><td>0</td><td>6</td><td>N/A</td><td>Fibrosarcoma; all NM</td></tr>
<tr><td><strong>Total</strong></td><td>&mdash;</td><td><strong>73</strong></td><td><strong>20</strong></td><td><strong>53</strong></td><td>&mdash;</td><td>&mdash;</td></tr>
</table>
<div class="warning">
<strong>Year 2 cohort caveat:</strong> Dogs 20&ndash;25 lack a paired post-ferumoxytol MRI acquisition, so PSIL and MR2_SI are unavailable.
The PSIL regression in Aim 2 therefore uses Year 1 dogs only (Dogs 7&ndash;9, 11, 12 &rarr; 30 LNs). Aim 1 and Aim 3 use the full cohort where data permit.
</div>
<div class="warning">
<strong>Data note &mdash; Dog 12 LMLN1:</strong> The summary sheet records this node as histologically metastatic, but the
primary data entry sheet and PSIL value (&minus;0.863) are consistent with a normal node (robust iron uptake).
The primary data sheet is used as ground truth; LMLN1 for Dog 12 is treated as NM.
</div>
<p><strong>Radiomic features:</strong> 107 PyRadiomics features (Shape, First-order, GLCM, GLDM, GLRLM, GLSZM, NGTDM)
extracted from <strong>post-ferumoxytol</strong> MRI. After median imputation and intra-fold correlation filtering (r&thinsp;&gt;&thinsp;0.95),
~50 features are retained per fold.</p>
<p><strong>Validation:</strong> Leave-One-Dog-Out Cross-Validation (LODO-CV, 12 folds for Aim 1; 5 folds for Aim 2) prevents within-dog correlation leakage.</p>
"""

SEC2_text = """
<h2>2. Exploratory Data Analysis</h2>
<p>Within the Year 1 PSIL-bearing subset, NM nodes (median PSIL &minus;0.618) show greater iron uptake than M nodes (median PSIL &minus;0.440),
confirmed by Mann-Whitney U test (p = 0.019). Distributions overlap substantially, limiting PSIL as a stand-alone binary classifier.</p>
"""
SEC2_fig1_cap = "Figure 1. Year 1 cohort: PSIL distributions for NM vs M lymph nodes (Mann-Whitney p=0.019). Normal nodes show greater signal loss (more negative PSIL). Right: near-linear relationship between PSIL and the MR2/MR1 signal ratio."
SEC2_fig2_cap = "Figure 2. PCA of 107 radiomic features across all 73 LNs. Left (by histological class): NM and M nodes are not linearly separable in PC1/PC2. Right (by dog): nodes cluster by individual dog, indicating that inter-dog variability dominates radiomic variance even after adding the Year 2 cohort."
SEC2_callout = """
<div class="callout">
<strong>Key insight from PCA:</strong> Individual dog identity remains the dominant source of variance in radiomic space even after doubling the cohort.
Histological class (NM vs M) does not separate in principal component space. This is the primary reason
cross-validated classification performance is modest.
</div>
"""

SEC3_text = """
<h2>3. Aim 1 &mdash; Normal vs Metastatic Lymph Node Classification</h2>
<p>Three classifiers (Logistic Regression, Linear SVM, Random Forest) were trained and evaluated under LODO-CV across all 12 dogs (73 LNs),
with feature selection (variance threshold + correlation filter + standard scaling) applied within each fold to prevent data leakage.
Because the radiomics are extracted from the <strong>post-iron</strong> acquisition, the discriminative information is expected to come primarily
from intensity-level features (first-order statistics and signal-magnitude GLCM features): M nodes retain more signal and texture heterogeneity than iron-laden NM nodes.</p>
<h3>Methodological safeguards (added with Year 2)</h3>
<ul>
<li><strong>LODO-CV correctness audit</strong> &mdash; an automated check verified that across all 12 folds, no dog and no row index appears in both training and held-out sets. <span class="good">PASSED.</span> Every node is held out exactly once with all of its dog-mates withheld with it.</li>
<li><strong>Within-fold preprocessing pipeline</strong> &mdash; per fold: median imputation, variance threshold, correlation filter (r&thinsp;&gt;&thinsp;0.95), standard scaling, optional SMOTE, then classifier. All filters and scalers are <em>fit on training nodes only</em>, then applied to the held-out dog.</li>
<li><strong>Class-imbalance comparison</strong> &mdash; three training strategies were run head-to-head: baseline, <code>class_weight="balanced"</code>, and SMOTE (synthetic minority oversampling) <em>inside</em> the training fold only. Test data is never resampled.</li>
<li><strong>Permutation test</strong> &mdash; with N=73 LNs and 20 metastatic nodes, the empirical chance distribution is wide. We shuffle the histopathology labels 200&times; and recompute LODO-CV AUC each time to compare the observed AUC against an empirical null.</li>
</ul>
<h3>LODO-CV Performance (12 folds, baseline strategy)</h3>
<table>
<tr><th>Model</th><th>AUC</th><th>Accuracy</th><th>Sensitivity</th><th>Specificity</th></tr>
<tr><td>Logistic Regression</td><td class="bad">0.234</td><td>61.6%</td><td>10.0%</td><td>81.1%</td></tr>
<tr><td>Linear SVM</td><td class="bad">0.273</td><td>61.6%</td><td>10.0%</td><td>81.1%</td></tr>
<tr><td>Random Forest</td><td class="ok">0.574</td><td>61.6%</td><td>25.0%</td><td>75.5%</td></tr>
</table>
<h3>Class-imbalance strategy comparison (Random Forest, 12-fold LODO-CV)</h3>
<table>
<tr><th>Strategy</th><th>AUC</th><th>Notes</th></tr>
<tr><td>Baseline</td><td class="ok">0.574</td><td>No reweighting, no resampling.</td></tr>
<tr><td>Class-weighted (<code>balanced</code>)</td><td>0.532</td><td>Inverse-frequency loss weights; did not beat baseline.</td></tr>
<tr><td>SMOTE within fold</td><td>0.516</td><td>Synthetic minority oversampling on training set only; did not beat baseline.</td></tr>
</table>
<p>With the expanded cohort, Random Forest reaches AUC = 0.574 &mdash; modestly above chance &mdash; while the linear models (LR, SVM)
remain below chance. Accuracy is inflated by the larger NM class (53/73 = 73% NM); sensitivity for metastasis remains low across all models
(10&ndash;25%). Class-weighting and SMOTE did <em>not</em> improve AUC, indicating the bottleneck is the radiomic signal-to-noise ratio at
this sample size, not the imbalance per se.</p>
"""
SEC3_perm = """
<h3>Permutation Significance Test</h3>
<p>To check whether the observed Random-Forest AUC is statistically distinguishable from chance under LODO-CV, we permuted the
histopathology labels 200&times; and re-ran the full pipeline (median imputation &rarr; variance threshold &rarr; correlation filter
&rarr; standardisation &rarr; RF) inside each fold for every shuffle.</p>
<table>
<tr><th>Quantity</th><th>Value</th></tr>
<tr><td>Observed RF AUC</td><td class="ok">0.574</td></tr>
<tr><td>Null distribution mean</td><td>0.476</td></tr>
<tr><td>Null distribution 95th percentile</td><td>0.638</td></tr>
<tr><td>Empirical p-value</td><td class="bad">0.184</td></tr>
</table>
<div class="warning">
<strong>Honest interpretation:</strong> The observed AUC of 0.574 falls inside the empirical null distribution (p&nbsp;=&nbsp;0.184).
At the current sample size, radiomic models do <strong>not</strong> yet provide statistically credible discrimination of metastatic
from normal lymph nodes under leave-one-dog-out validation. This is consistent with the modest absolute AUC and with the PCA showing
inter-dog variance dominating class-related variance.
</div>
"""
SEC3_perm_fig_cap = "Figure 4. Permutation null distribution for LODO-CV Random-Forest AUC (200 label shuffles). The observed AUC=0.574 (red line) lies inside the null distribution; empirical p=0.184."
SEC3_fig1_cap = "Figure 3. Left: LODO-CV ROC curves for all three classifiers and three class-imbalance strategies (12 folds). Random Forest baseline reaches AUC=0.574; SMOTE and class-weighted variants do not improve performance. Right: pooled confusion matrix for the best Random Forest configuration."
SEC3_perdog = """
<h3>Per-Dog Breakdown (Random Forest)</h3>
<table>
<tr><th>Dog</th><th>Cohort</th><th>n LNs</th><th>n M</th><th>Correct</th><th>Accuracy</th><th>Note</th></tr>
<tr><td>7</td><td>Y1</td><td>6</td><td>2</td><td>3</td><td>50%</td><td>&mdash;</td></tr>
<tr><td>8</td><td>Y1</td><td>6</td><td>5</td><td>1</td><td>17%</td><td>&mdash;</td></tr>
<tr><td>9</td><td>Y1</td><td>6</td><td>0</td><td>4</td><td>67%</td><td>All NM; 2 false positives</td></tr>
<tr><td>10</td><td>Y1</td><td>7</td><td>5</td><td>4</td><td>57%</td><td>&mdash;</td></tr>
<tr><td>11</td><td>Y1</td><td>6</td><td>0</td><td>0</td><td>0%</td><td>All NM; all predicted M</td></tr>
<tr><td>12</td><td>Y1</td><td>6</td><td>5</td><td>1</td><td>17%</td><td>&mdash;</td></tr>
<tr><td>20 (Y2D1)</td><td>Y2</td><td>6</td><td>2</td><td>4</td><td>67%</td><td>2 M nodes missed</td></tr>
<tr><td>21 (Y2D2)</td><td>Y2</td><td>6</td><td>0</td><td>5</td><td>83%</td><td>All NM; 1 false positive</td></tr>
<tr><td>22 (Y2D3)</td><td>Y2</td><td>6</td><td>0</td><td>6</td><td>100%</td><td>All NM; all correct</td></tr>
<tr><td>23 (Y2D4)</td><td>Y2</td><td>6</td><td>1</td><td>5</td><td>83%</td><td>Single M node missed</td></tr>
<tr><td>24 (Y2D5)</td><td>Y2</td><td>6</td><td>0</td><td>6</td><td>100%</td><td>All NM; all correct</td></tr>
<tr><td>25 (Y2D6)</td><td>Y2</td><td>6</td><td>0</td><td>6</td><td>100%</td><td>All NM; all correct</td></tr>
</table>
<p>Performance varies dramatically across folds. The Year 2 cohort is dominated by NM-only dogs (5 of 6), so high accuracy on those folds reflects
correct rejection of the (numerous) NM nodes rather than improved metastasis detection. Year 1 metastatic-rich dogs (8, 10, 12) remain difficult,
with Dog 11 still wholly misclassified.</p>
"""
SEC3_fig2_cap = "Figure 5. Top 20 radiomic features by Random Forest mean decrease in impurity (full cohort, 12 dogs). First-order intensity statistics and GLCM/GLRLM texture features dominate; shape features contribute minimally. Consistent with post-iron biology: signal-magnitude features lead the ranking."

SEC4_text = """
<h2>4. Aim 2 &mdash; Radiomic Correlates of Iron Nanoparticle Uptake (PSIL)</h2>
<p>Regression performed on 30 LNs from 5 Year 1 dogs (Dog 10 and the entire Year 2 cohort excluded &mdash; no post-ferumoxytol acquisition).
PSIL range: &minus;0.863 to +0.139 (mean &minus;0.533, SD 0.228).</p>
<h3>LODO-CV Regression Performance (5 folds)</h3>
<table>
<tr><th>Model</th><th>R&sup2;</th><th>RMSE</th><th>Pearson r</th><th>p-value</th></tr>
<tr><td>Ridge</td><td class="bad">&minus;3.071</td><td>0.459</td><td>&minus;0.288</td><td>0.123</td></tr>
<tr><td>Lasso</td><td class="bad">&minus;1.590</td><td>0.366</td><td>&minus;0.335</td><td>0.071</td></tr>
<tr><td>SVR (linear)</td><td class="bad">&minus;1.512</td><td>0.361</td><td>&minus;0.012</td><td>0.951</td></tr>
<tr><td>Random Forest</td><td class="bad">&minus;0.203</td><td>0.250</td><td>+0.020</td><td>0.915</td></tr>
</table>
<p>All models have negative R&sup2;, meaning they perform worse than predicting the mean PSIL for every node.
No model achieves statistical significance. <strong>Zero Bonferroni-corrected significant features</strong>
were identified across all 107 univariate Spearman correlations. The Year 2 cohort cannot contribute here
because PSIL is undefined without paired post-ferumoxytol imaging.</p>
"""
SEC4_fig1_cap = "Figure 6. Random Forest PSIL regression (best model by R-squared). Left: predicted vs actual PSIL showing predictions cluster near the mean regardless of actual value. Right: residual plot."
SEC4_fig2_cap = "Figure 7. Top 15 univariate Spearman correlates with PSIL (Year 1 cohort). GLCM texture features (Idn, Idmn) and first-order features (Kurtosis, Skewness) show |r| ~0.27-0.30; none survive Bonferroni correction."

SEC5_text = """
<h2>5. Aim 3 &mdash; Primary Tumour Radiomics vs LN Metastatic Burden</h2>
<div class="warning">
<strong>Critical limitation:</strong> Primary tumour segmentations are now available for <strong>4 dogs</strong>
(Dogs 7, 11, 12, and 22 / Y2D3). With n=4, p-values still carry essentially no statistical meaning, and most rank correlations
return |r| at or near 1.0 by construction. This analysis remains strictly hypothesis-generating.
</div>
<table>
<tr><th>Dog</th><th>Cohort</th><th>Tumour</th><th>Metastatic Burden (fraction of M LNs)</th></tr>
<tr><td>7</td><td>Y1</td><td>&mdash;</td><td>0.333 (2/6)</td></tr>
<tr><td>11</td><td>Y1</td><td>&mdash;</td><td>0.000 (0/6)</td></tr>
<tr><td>12</td><td>Y1</td><td>&mdash;</td><td>0.833 (5/6)</td></tr>
<tr><td>22 (Y2D3)</td><td>Y2</td><td>GIII STS</td><td>0.000 (0/6)</td></tr>
</table>
<p>Top-ranked primary tumour features include first-order intensity statistics (<code>Mean</code>, <code>Median</code>,
<code>RootMeanSquared</code>) and GLCM/GLRLM texture features. With n=4 the maximum achievable Spearman |r| is 1.0,
so feature ranking reflects which features are perfectly monotone with the four burden values rather than a generalizable signal.
A minimum of approximately 8&ndash;10 dogs with primary segmentations is still recommended before drawing interpretable conclusions.</p>
"""
SEC5_fig1_cap = "Figure 8. Heatmap of the 30 primary tumour features most strongly rank-correlated with LN metastatic burden across the 4 dogs (z-scored)."
SEC5_fig2_cap = "Figure 9. Top 6 primary tumour features vs LN metastatic burden (n=4 dogs). All correlations are visually monotone but limited by sample size."

SEC6_text = """
<h2>6. Supplementary &mdash; Subjective MRI vs Histopathology</h2>
<p>As a clinical reference, subjective radiologist MRI classification was evaluated against histopathological
ground truth across all 73 LNs.</p>
<table>
<tr><th>Method</th><th>Sensitivity</th><th>Specificity</th><th>Accuracy</th><th>Cohen Kappa</th></tr>
<tr><td>Subjective MRI read (12 dogs, 73 LNs)</td><td class="good">60.0%</td><td class="good">96.2%</td><td class="good">86.3%</td><td class="good">0.620</td></tr>
<tr><td>PSIL threshold (&ge;&minus;0.20 implies M; Year 1 only, 30 LNs)</td><td>25.0%</td><td>100%</td><td>70.0%</td><td>&mdash;</td></tr>
</table>
"""
SEC6_fig_cap = "Figure 10. Left: confusion matrix for subjective MRI vs histopathology (all 73 LNs across 12 dogs). Right: ROC for PSIL as binary classifier (Year 1 cohort only)."
SEC6_callout = """
<div class="callout">
<strong>The subjective radiologist read (kappa=0.620, 86.3% accuracy) continues to outperform all radiomic models</strong>
across the expanded 12-dog cohort. Specificity is now 96.2% (one false positive in Y2D5 RRPLN; one in Y2D1 RRPLN counted in earlier Year 1 reads is already in the FP tally).
The radiomic approach does not yet add diagnostic value over the existing clinical standard.
</div>
"""

SEC7 = """
<h2>7. Summary of Key Findings</h2>
<table>
<tr><th>Aim</th><th>Approach</th><th>Metric</th><th>Result</th><th>Interpretation</th></tr>
<tr>
  <td>1 &mdash; NM vs M classification</td>
  <td>LR, SVM, RF; LODO-CV (12 folds); &plus; SMOTE / class-weighted; permutation test</td>
  <td>AUC (perm. p)</td>
  <td class="ok">RF AUC 0.574 (p=0.184)</td>
  <td>Audit confirms no leakage. RF marginally above chance but <strong>not</strong> significantly different from a permuted-label null. Class-weighting / SMOTE did not help.</td>
</tr>
<tr>
  <td>2 &mdash; PSIL regression</td>
  <td>Ridge, Lasso, SVR, RF; LODO-CV (Year 1, 5 folds)</td>
  <td>R&sup2;</td>
  <td class="bad">&minus;3.07 to &minus;0.20 (all negative)</td>
  <td>No radiomic model predicts iron uptake; no univariate feature survives correction</td>
</tr>
<tr>
  <td>3 &mdash; Tumour to LN burden</td>
  <td>Spearman only, n=4 dogs</td>
  <td>|r|</td>
  <td>up to 0.95 (trivial at n=4)</td>
  <td>Hypothesis-generating only; no statistical conclusions possible</td>
</tr>
<tr>
  <td>Ref &mdash; Subjective MRI</td>
  <td>Radiologist read vs histo (12 dogs, 73 LNs)</td>
  <td>Kappa</td>
  <td class="good">0.620 (86.3% accuracy)</td>
  <td>Clinical read continues to outperform all radiomic models</td>
</tr>
</table>

<h2>8. Limitations &amp; Caveats</h2>
<ul>
<li><strong>Cohort still small (n=12 dogs, 73 LNs):</strong> Doubling the cohort improved Aim 1 RF AUC from 0.28 to 0.57, but a 200-shuffle permutation test gives an empirical p=0.184. The observed AUC sits inside the chance distribution at this sample size; external validation is not yet possible.</li>
<li><strong>Dog-dominated variance:</strong> PCA continues to show inter-dog variation exceeding class-related variation, making cross-dog generalisation challenging.</li>
<li><strong>Class imbalance:</strong> 53 NM vs 20 M (73% NM) inflates accuracy and specificity; sensitivity for metastasis remains the limiting metric.</li>
<li><strong>All-NM dogs (9, 11, 21, 22, 24, 25):</strong> These six folds trivially inflate specificity and cannot be used to estimate sensitivity individually.</li>
<li><strong>Year 2 cohort lacks PSIL:</strong> Aim 2 still uses only Year 1 (30 LNs). Adding post-ferumoxytol acquisitions to future Year 2 dogs is the highest-yield improvement.</li>
<li><strong>Tumour heterogeneity:</strong> Cohort spans MCT, OMM, FSA, STS, melanoma, and fibrosarcoma &mdash; limiting tumour-specific interpretation.</li>
<li><strong>Single MRI sequence:</strong> Radiomics here are from the post-ferumoxytol acquisition only. Adding pre-iron radiomics on the same nodes (pre/post delta features) or multi-parametric sequences (T2*, DWI) may improve discrimination.</li>
<li><strong>Primary tumour analysis (Aim 3):</strong> n=4 &mdash; hypothesis generation only; no statistical conclusions.</li>
</ul>

<h2>9. Recommended Next Steps</h2>
<ol>
<li>Extend Year 2 acquisitions to include post-ferumoxytol imaging so PSIL can be computed for those dogs (would roughly double the Aim 2 sample).</li>
<li>Continue cohort expansion toward &ge;20 dogs to push Aim 1 LODO-CV beyond modest discrimination.</li>
<li>Include multi-parametric sequences (post-ferumoxytol, T2*, DWI) in radiomic extraction.</li>
<li>Harmonise MRI acquisition across sessions/protocols to reduce inter-dog radiomic variance (or apply ComBat-style harmonisation post-hoc).</li>
<li>Complete primary tumour segmentations for the remaining dogs (8, 9, 10, 20, 21, 23, 24, 25) to enable a meaningful Aim 3 analysis.</li>
</ol>

<hr>
<p style="font-size:.82em;color:#888">Report generated from <code>main.ipynb</code>
(CSU Iron Nanoparticle Ferumoxytol Radiomics Study).
Analysis used Python 3, pandas 2.2, scikit-learn 1.5+, and PyRadiomics.
All cross-validation results are internal LODO-CV estimates only.</p>
</body>
</html>
"""

html = (
    HEADER +
    SEC1 +
    SEC2_text +
    img('cell08_fig0', SEC2_fig1_cap) +
    img('cell09_fig0', SEC2_fig2_cap) +
    SEC2_callout +
    SEC3_text +
    img('cell16_fig0', SEC3_fig1_cap) +
    SEC3_perm +
    img('cell19_fig0', SEC3_perm_fig_cap) +
    SEC3_perdog +
    img('cell20_fig0', SEC3_fig2_cap) +
    SEC4_text +
    img('cell24_fig0', SEC4_fig1_cap) +
    img('cell26_fig0', SEC4_fig2_cap) +
    SEC5_text +
    img('cell30_fig0', SEC5_fig1_cap) +
    img('cell31_fig0', SEC5_fig2_cap) +
    SEC6_text +
    img('cell33_fig0', SEC6_fig_cap) +
    SEC6_callout +
    SEC7
)

out_path = 'c:/Users/sshuser/Documents/CSU_Iron/study_summary.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written {len(html):,} chars to {out_path}")
