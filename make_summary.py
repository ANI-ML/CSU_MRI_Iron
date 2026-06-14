"""Generate study_summary.html from the figures exported from main.ipynb.

Figures live in summary_figures/ (exported from the executed notebook). Narrative,
tables and the explainability summary are written here to match the current study:
multi-sequence radiomics, histology-trained classifier comparison, radiologist
benchmark, reader combination, and feature explainability — all under
Leave-One-Dog-Out CV with dog-level bootstrap confidence intervals.
"""
import base64, os

fig_dir = 'c:/Users/sshuser/Documents/CSU_Iron/summary_figures'
figs = {}
for fname in sorted(os.listdir(fig_dir)):
    if fname.endswith('.png'):
        with open(os.path.join(fig_dir, fname), 'rb') as f:
            figs[fname.replace('.png', '')] = base64.b64encode(f.read()).decode()


def img(key, caption):
    return (
        '\n<figure>\n'
        f'<img src="data:image/png;base64,{figs[key]}" alt="{caption}" '
        'style="max-width:100%;border:1px solid #ddd;border-radius:4px;">\n'
        f'<figcaption>{caption}</figcaption>\n</figure>\n'
    )


CSS = """
  body{font-family:Georgia,serif;max-width:980px;margin:40px auto;padding:0 20px;line-height:1.7;color:#222}
  h1{color:#1a3a5c;border-bottom:3px solid #1a3a5c;padding-bottom:8px}
  h2{color:#1a3a5c;margin-top:2em;border-bottom:1px solid #aac;padding-bottom:4px}
  h3{color:#2c5f8a;margin-top:1.4em}
  table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.93em}
  th{background:#1a3a5c;color:#fff;padding:8px 12px;text-align:left}
  td{padding:7px 12px;border-bottom:1px solid #dde}
  tr:nth-child(even){background:#f5f8fb}
  figure{margin:1.5em 0}
  figcaption{font-size:.88em;color:#555;font-style:italic;margin-top:6px;text-align:center}
  .callout{background:#eef4fb;border-left:4px solid #2c5f8a;padding:10px 16px;margin:1em 0;border-radius:0 4px 4px 0}
  .warning{background:#fff8e1;border-left:4px solid #f5a623;padding:10px 16px;margin:1em 0;border-radius:0 4px 4px 0}
  .keyfind{background:#eaf6ea;border-left:4px solid #2a7a2a;padding:10px 16px;margin:1em 0;border-radius:0 4px 4px 0}
  .bad{color:#b33;font-weight:bold}
  .ok{color:#a86b00;font-weight:bold}
  .good{color:#2a7a2a;font-weight:bold}
  code{background:#f0f0f0;padding:1px 4px;border-radius:3px;font-size:.9em}
  ul li,ol li{margin-bottom:.3em}
  .muted{color:#666;font-size:.92em}
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CSU Iron Nanoparticle Radiomics Study</title>
<style>{CSS}</style>
</head>
<body>
<h1>CSU Iron Nanoparticle (Ferumoxytol) Radiomics Study</h1>
<p><em>Canine Head-and-Neck Lymph Node Characterisation &mdash; Multi-Sequence MRI</em></p>
<p class="muted">Regenerated from <code>main.ipynb</code> (<code>Data/FINAL_DATA</code>) &middot; June 2026</p>

<div class="callout">
<strong>Study in brief.</strong> We ask whether a radiomics machine-learning model, trained on the
<strong>histopathological ground truth</strong>, can match or beat the <strong>human radiologist's
imaging diagnosis</strong> at calling a head-and-neck lymph node metastatic (M) vs non-metastatic (NM).
Each node is described by radiomics from <strong>four MRI sequences</strong> (T1, T2, T1-post, gradient-echo),
modelled under leakage-free Leave-One-Dog-Out cross-validation, and benchmarked against the radiologist
on the same nodes. This is a deliberately honest <strong>proof-of-concept</strong>: every metric carries a
confidence interval and the headline result is reported as it falls.
</div>

<div class="keyfind">
<strong>Headline.</strong> On this cohort the <span class="good">radiologist clearly outperforms the
radiomics model</span> (accuracy 90% vs 76%, McNemar p&nbsp;&lt;&nbsp;0.001). All four classifier
families land at AUC&nbsp;&asymp;&nbsp;0.59&ndash;0.62 with 95% CIs that span chance, and the best model's
permutation test is non-significant (p&nbsp;&asymp;&nbsp;0.10). The limiting factor is the data
(31 metastatic events, features&nbsp;&gg;&nbsp;samples), not the algorithm.
</div>

<h2>1. Study Design &amp; Dataset</h2>
<p>
Segmentations were exported from PyRadiomics for <strong>29 dogs</strong> across three sub-cohorts and
contoured on four MRI sequences each (T1, T2, T1-post = <code>T1P</code>, gradient-echo = <code>GE</code>);
only <code>Y2&nbsp;D12</code> is missing <code>T1P</code>. Older single-acquisition exports present in the
folder were detected as duplicates (identical mask geometry) and excluded. For every lymph node the
<code>original</code> features from each sequence are concatenated into one vector
(<code>T1__&hellip;</code>, <code>T2__&hellip;</code>, &hellip;), giving <strong>171 nodes &times; 428
features</strong>. Labels come from the <em>Summary</em> sheet of <code>patient_data_labels.xlsx</code>:
<code>histo_M</code> (ground truth; Metastatic&nbsp;&rarr;&nbsp;1, Normal/Reactive/Hyperplasia&nbsp;&rarr;&nbsp;0)
and <code>imaging_M</code> (the radiologist's M/NM read).
</p>

<table>
<tr><th>Cohort</th><th>Dogs</th><th>Lymph nodes</th><th>Metastatic (M)</th><th>Sequences</th></tr>
<tr><td>Year 1 (D1&ndash;D12)</td><td>12</td><td>74</td><td>18</td><td>T1, T2, T1P, GE</td></tr>
<tr><td>Year 2 (Y2 D1&ndash;D12)</td><td>12</td><td>73</td><td>6</td><td>T1, T2, T1P, GE (Y2 D12 no T1P)</td></tr>
<tr><td>CRC model (CRC D2&ndash;D6)</td><td>5</td><td>24</td><td>7</td><td>T1, T2, T1P, GE</td></tr>
<tr><td><strong>Total</strong></td><td><strong>29</strong></td><td><strong>171</strong></td>
    <td><strong>31 (18.1%)</strong></td><td>&mdash;</td></tr>
</table>
<p class="muted">164 of 171 nodes also carry a radiologist call (Y2 D9 recorded raw signal intensities
instead of an M/NM diagnosis). Metastatic nodes are concentrated in 11 of 29 dogs.</p>
{img('fig1_eda', 'Figure 1. Lymph nodes by cohort and histology (left) and a PCA of the multi-sequence radiomic feature space coloured by histology (right). The classes overlap heavily in feature space.')}

<h2>2. Methods</h2>
<p>The model is deliberately frugal because the data are <em>p&nbsp;&gg;&nbsp;n</em>
(31 events, 428 features &rarr; events-per-variable &asymp; 0.07). The full chain is fit
<strong>inside each Leave-One-Dog-Out fold on the training dogs only</strong>, so no test node ever
informs feature selection:</p>
<ol>
<li>median imputation &rarr; near-zero-variance drop &rarr; correlation filter (|r|&nbsp;&gt;&nbsp;0.95);</li>
<li><strong>univariate screen</strong> &mdash; rank features by training-fold AUC against <code>histo_M</code>, keep the top 10;</li>
<li>standardise &rarr; <strong>classifier</strong>; the decision threshold is tuned by <strong>Youden's J</strong> on the training fold.</li>
</ol>
<p><strong>Classifiers compared:</strong> L1-penalised Logistic Regression, Linear SVM, Random Forest, and
XGBoost. All are made <strong>cost-sensitive</strong> (<code>class_weight='balanced'</code>;
<code>scale_pos_weight</code> for XGBoost). An earlier check showed SMOTE / random oversampling did not
improve on class-weighting, so weighting is used throughout. <strong>Validation</strong> is Leave-One-Dog-Out
CV (the dog, not the node, is the held-out unit). <strong>Uncertainty</strong> is quantified with
<strong>dog-level (cluster) bootstrap 95% CIs</strong> on every metric, plus a permutation test that reruns
the entire pipeline on shuffled labels.</p>

<h2>3. Results &mdash; Classifier Comparison</h2>
<p>Target = <code>histo_M</code> (histological ground truth), LODO-CV. The four families are statistically
indistinguishable; Linear SVM is nominally best.</p>
<table>
<tr><th>Classifier</th><th>AUC</th><th>AUC 95% CI</th><th>Sensitivity</th><th>Specificity</th><th>Accuracy</th></tr>
<tr><td><strong>Linear SVM</strong> (best)</td><td><strong>0.623</strong></td><td>[0.38, 0.87]</td><td>41.9%</td><td>84.3%</td><td>76.6%</td></tr>
<tr><td>Logistic (L1)</td><td>0.592</td><td>[0.35, 0.85]</td><td>41.9%</td><td>85.7%</td><td>77.8%</td></tr>
<tr><td>XGBoost</td><td>0.590</td><td>[0.37, 0.84]</td><td>19.4%</td><td>96.4%</td><td>82.5%</td></tr>
<tr><td>Random Forest</td><td>0.588</td><td>[0.34, 0.85]</td><td>38.7%</td><td>85.7%</td><td>77.2%</td></tr>
</table>
{img('fig2_roc_models', 'Figure 2. ROC curves for all four classifiers under LODO-CV (best model highlighted). All hug the diagonal.')}
<div class="warning">
<strong>Interpretation.</strong> Every classifier's 95% CI includes AUC&nbsp;=&nbsp;0.5, and the best model's
<strong>permutation test gives p&nbsp;&asymp;&nbsp;0.10 (not significant)</strong> &mdash; observed AUC 0.623 vs a
null mean of 0.48. Switching algorithm families does not rescue performance; the bottleneck is sample size.
</div>
{img('fig3_permutation', 'Figure 3. Permutation null for the best model: the observed AUC (red) sits inside the bulk of the shuffled-label distribution.')}

<h2>4. Explainability &mdash; What drives the predictions?</h2>
<p>Two complementary, leakage-aware views of the signal. <strong>(a) Univariate association</strong>
(descriptive, full cohort): each feature's AUC against <code>histo_M</code> with a Mann-Whitney U test and
Benjamini-Hochberg FDR correction. <strong>(b) Selection stability</strong> (cross-validated): how often
each feature enters the in-fold top-10 across the 29 LODO folds &mdash; the reproducible correlates worth
trusting on a small cohort.</p>

<table>
<tr><th>Feature</th><th>Univariate AUC</th><th>FDR q</th><th>Folds selected (/29)</th><th>What it captures</th></tr>
<tr><td><code>glszm LargeAreaHighGrayLevelEmphasis</code> (T1)</td><td>0.79</td><td>&lt;0.001</td><td>&mdash;</td><td>large, bright sub-regions</td></tr>
<tr><td><code>gldm LargeDependenceHighGrayLevelEmphasis</code> (GE)</td><td>0.79</td><td>&lt;0.001</td><td>29</td><td>large bright homogeneous zones</td></tr>
<tr><td><code>gldm DependenceEntropy</code> (GE)</td><td>0.75</td><td>&lt;0.001</td><td>29</td><td>textural heterogeneity</td></tr>
<tr><td><code>shape LeastAxisLength</code> (T1/T2/GE/T1P)</td><td>0.74&ndash;0.76</td><td>&lt;0.001</td><td>28</td><td><strong>node short-axis size</strong></td></tr>
<tr><td><code>shape SurfaceVolumeRatio</code> (T1)</td><td>0.74*</td><td>&lt;0.001</td><td>27</td><td>node compactness (inverse of size)</td></tr>
<tr><td><code>firstorder Skewness</code> (GE)</td><td>0.75*</td><td>&lt;0.001</td><td>28</td><td>intensity asymmetry</td></tr>
</table>
<p class="muted">*Some features are protective (AUC &lt; 0.5, i.e. higher value &rarr; less likely metastatic);
the value shown is the strength of association. 196 of 428 features pass FDR q&nbsp;&lt;&nbsp;0.05, but they
are highly collinear and dominated by the size / large-bright-region axis.</p>
{img('fig4_explainability', 'Figure 4. Left: top features by univariate AUC against histology. Right: selection frequency across the 29 LODO folds (the stable, reproducible predictors).')}
<div class="callout">
<strong>Plain-language explanation.</strong> The reproducible signal is essentially
<em>"big, bright, heterogeneous node"</em> &mdash; short-axis <strong>size</strong>
(<code>LeastAxisLength</code>, <code>SurfaceVolumeRatio</code>) together with
<strong>large-area / large-dependence high-gray-level texture</strong> and intensity heterogeneity. These
co-vary (large nodes have large bright zones). Critically, <strong>node size is exactly the cue a
radiologist already uses</strong>, so the model carries little <em>independent</em> information &mdash; which
is the mechanistic reason it cannot beat the human read (&sect;6).
</div>

<h2>5. Single-Sequence vs Combined Radiomics</h2>
<p>Each MRI sequence run alone through the identical pipeline, vs the four concatenated. Differences are
within the confidence intervals &mdash; combining sequences adds little here.</p>
<table>
<tr><th>Sequence</th><th>Features</th><th>AUC</th><th>AUC 95% CI</th><th>Sensitivity</th><th>Specificity</th></tr>
<tr><td>GE</td><td>107</td><td>0.669</td><td>[0.41, 0.90]</td><td>48.4%</td><td>85.0%</td></tr>
<tr><td>T1</td><td>107</td><td>0.638</td><td>[0.44, 0.85]</td><td>38.7%</td><td>81.4%</td></tr>
<tr><td>T2</td><td>107</td><td>0.622</td><td>[0.42, 0.85]</td><td>48.4%</td><td>82.1%</td></tr>
<tr><td>T1P</td><td>107</td><td>0.612</td><td>[0.40, 0.83]</td><td>32.3%</td><td>85.0%</td></tr>
<tr><td><strong>ALL (4-seq)</strong></td><td>428</td><td>0.623</td><td>[0.38, 0.87]</td><td>41.9%</td><td>84.3%</td></tr>
</table>
{img('fig5_sequences', 'Figure 5. Single-sequence vs combined AUC with 95% CIs. The combination does not exceed the best single sequence (GE).')}

<h2>6. Radiologist vs Model (head-to-head)</h2>
<p>On the 164 nodes that received a radiologist call (29 metastatic), the radiologist's subjective MRI read
and the best model are both scored against histology.</p>
<table>
<tr><th>Reader</th><th>Sensitivity</th><th>Specificity</th><th>Accuracy</th><th>AUC</th></tr>
<tr><td><strong>Radiologist</strong> (subjective MRI)</td><td>0.724 [0.38, 0.96]</td><td>0.933 [0.89, 0.98]</td><td><span class="good">0.896 [0.82, 0.96]</span></td><td>&mdash;</td></tr>
<tr><td>Radiomics model (Linear SVM)</td><td>0.379 [0.11, 0.77]</td><td>0.837 [0.73, 0.93]</td><td>0.756 [0.64, 0.86]</td><td>0.601 [0.34, 0.87]</td></tr>
</table>
<p>McNemar's test on discordant calls: radiologist-only-correct = 27, model-only-correct = 4,
&chi;<sup>2</sup> = 15.6, <strong>p&nbsp;&lt;&nbsp;0.001</strong> &mdash; the radiologist is significantly better.</p>
{img('fig6_radiologist', 'Figure 6. Confusion matrices for the radiologist (left) and the model (centre) against histology, and the model ROC with the radiologist operating point overlaid (right).')}

<h2>7. Combining Radiologist + Model</h2>
<p>Because the two readers make partly different errors, three combinations were tested: OR (either flags M),
AND (both flag M), and a leak-free logistic stack trained under LODO-CV.</p>
<table>
<tr><th>Reader</th><th>Sensitivity</th><th>Specificity</th><th>Accuracy [95% CI]</th><th>&kappa;</th><th>AUC</th></tr>
<tr><td><strong>Radiologist alone</strong></td><td>0.724</td><td>0.933</td><td><span class="good">0.896 [0.82, 0.96]</span></td><td>0.649</td><td>&mdash;</td></tr>
<tr><td>Model alone (Linear SVM)</td><td>0.379</td><td>0.837</td><td>0.756 [0.64, 0.86]</td><td>0.205</td><td>0.601</td></tr>
<tr><td>OR (either flags M)</td><td>0.724</td><td>0.807</td><td>0.793 [0.68, 0.88]</td><td>0.427</td><td>&mdash;</td></tr>
<tr><td>AND (both flag M)</td><td>0.379</td><td>0.963</td><td>0.860 [0.75, 0.95]</td><td>0.415</td><td>&mdash;</td></tr>
<tr><td>Logistic stack (LODO)</td><td>0.552</td><td>0.933</td><td>0.866 [0.79, 0.94]</td><td>0.513</td><td>0.650</td></tr>
</table>
{img('fig7_combination', 'Figure 7. Sensitivity/specificity/accuracy for the radiologist, the model, and the three combinations (left); confusion matrix of the OR rule (right).')}
<div class="warning">
<strong>No combination beats the radiologist alone.</strong> The model recovers <strong>0 of the 8
metastatic nodes the radiologist missed</strong> (the two readers fail on the same positives), so OR only
adds false alarms. The model's only value is on the negative class: the AND rule clears 4 of the
radiologist's 9 false alarms (specificity 0.93&nbsp;&rarr;&nbsp;0.96).
</div>

<h2>8. Summary of Key Findings</h2>
<ul>
<li><strong>The radiologist outperforms radiomics</strong> (accuracy 90% vs 76%, McNemar p&nbsp;&lt;&nbsp;0.001),
driven by much higher sensitivity.</li>
<li><strong>The model family does not matter</strong> &mdash; Logistic, SVM, RF and XGBoost all sit at
AUC&nbsp;&asymp;&nbsp;0.59&ndash;0.62 with CIs spanning chance; the best is not significant by permutation.</li>
<li><strong>The signal is "big, bright, heterogeneous node"</strong> &mdash; size and high-gray-level texture &mdash;
which is the same cue the radiologist already uses, leaving little independent information for the model.</li>
<li><strong>Combining sequences, or combining reader + model, does not help</strong> on the positive class.</li>
</ul>

<h2>9. Limitations &amp; Caveats</h2>
<ul>
<li><strong>Severely under-powered (p&nbsp;&gg;&nbsp;n)</strong> &mdash; 31 events, 428 features. This is a
proof-of-concept, not a validated model; CIs are wide by necessity.</li>
<li><strong>Cross-cohort batch effect</strong> &mdash; raw MRI intensity differs ~5&times; across CRC / Year-1 /
Year-2 (e.g. T1 first-order mean medians 2571 / 525 / 568). Intensity normalisation / ComBat harmonisation
is the highest-value next fix.</li>
<li><strong>Small nodes</strong> &mdash; 57/171 nodes are &lt; 500 mm&sup3; (16 &lt; 250 mm&sup3;); texture features
are unstable at that size.</li>
<li><strong>Label heterogeneity</strong> &mdash; CRC histology (Hyperplasia/Reactive/Normal/Metastatic) collapsed
to NM/M; reactive/hyperplastic nodes enlarge and enhance, the natural false-positive trap for both readers.</li>
<li><strong>Outlier dogs</strong> &mdash; D12 (occult-metastatic: 5/6 M, missed by radiologist <em>and</em> model)
and CRC D4 (6 of 31 positives in one dog) dominate the error and the positive class.</li>
</ul>

<h2>10. Recommended Next Steps</h2>
<ol>
<li><strong>Harmonise intensities</strong> (ComBat / per-image z-score) before re-extracting features &mdash;
likely the single biggest lever for a fair texture signal.</li>
<li><strong>Enrich the positive class</strong> (more metastatic nodes / an external cohort); the shared false
negatives show current features do not capture the occult metastases.</li>
<li><strong>Robustness analyses</strong> &mdash; exclude &lt; 250 mm&sup3; nodes; exclude reactive/hyperplastic
CRC nodes; present D12 as a case study.</li>
<li><strong>Position radiomics as a specificity aid</strong> (AND-style confirmation flagging likely false
alarms for re-review), not a sensitivity booster or a standalone replacement for the radiologist.</li>
</ol>

<p class="muted" style="margin-top:3em;border-top:1px solid #ccc;padding-top:10px">
All figures and numbers regenerated from <code>main.ipynb</code> on the <code>Data/FINAL_DATA</code> cohort.
Validation: Leave-One-Dog-Out cross-validation; intervals: dog-level bootstrap (2000 resamples).
</p>
</body>
</html>
"""

out = 'c:/Users/sshuser/Documents/CSU_Iron/study_summary.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)
print('Wrote', out, '|', len(HTML), 'chars |', len(figs), 'figures embedded')
