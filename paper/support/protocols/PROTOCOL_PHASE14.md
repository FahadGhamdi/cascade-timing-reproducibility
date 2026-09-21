# BRACE Phase 14: bounded supplementary interpretation after Phase 13F

Protocol `BRACE14-post13F-supplement-v1`, prepared 13 September 2026.

## Status and scope

The six Phase 13F test contrasts, their per-window summaries, calibration diagnostics and sample profiles have already been observed. Expert feedback motivates these additional analyses. This is a prospectively specified **post-test supplementary protocol**, not a preregistration of unseen primary test outcomes. The six original comparisons, their multiplicity correction, selected models and historical failures remain unchanged.

The manuscript concerns the incremental value of compact timing summaries within general-purpose count-distribution learners. It does not claim a new algorithm, a universal predictability ceiling, causal containment, or superiority over specialized cascade architectures. A new finite-horizon SEISMIC distribution and renewed TiDeH/CASPER fitting are outside this task. The domain-comparator scope is decided before the final venue is chosen.

## Stage A: saved-score stratification

Inputs are the exact Phase 13F archive, all 40 saved score streams and frozen TEST features, targets and cohort metadata. No model object is loaded. No fitting, prediction, distribution generation, or recalculation of CRPS is permitted. Compute supplementary MSLE only from the already saved predictive medians and responses. Score averaging is over model seeds, never over a mixture CDF.

First verify archive SHA-256, CRC, all 496 payload hashes, row keys, target/feature agreement, complete seed schedules, and recovery of the previously published aggregate CRPS values. Derive each source's lexical root order; retain three windows and all model seeds within root. The independent sample is not the collection of 600,000 score rows.

Use exactly five nonroot-prefix-count bins: 0, 1–2, 3–9, 10–49, and at least 50. Analyze each source and each window (300, 900, 3600 seconds) separately. There are 30 source/window/bin slots, with explicit empty slots, and 90 timing-contrast slots across the three primary families. Never merge bins, search thresholds, pool windows for the density claim, or pick the most favorable family after seeing results.

Report root counts, root-user group counts on Weibo, all 24 procedure-level CRPS values in their applicable slots, and absolute/relative I1−I0 contrasts for Hurdle/QRF/NGBoost. Also report the window-specific unconditional and conditional empirical levels, conditional-minus-unconditional deltas, and each primary I1-minus-conditional-reference delta descriptively. The latter are comparisons between procedures, not an information decomposition.

At zero nonroot events and fixed window, all seven timing summaries take deterministic defaults. Differences between I0 and I1 in that subgroup cannot be attributed to observed within-prefix event times. Do not assume the differences must vanish, because the procedures were fitted over all training cases.

For the 90 timing contrasts only, use 2,000 paired bootstrap vectors per source, seed 2026091701, PCG64, sources Weibo then SEISMIC, lexical group order, batches of 100. Resample Weibo root-user clusters, or SEISMIC roots, from the **whole source**; use the same draws across all windows, bins and families. For each slot divide the sampled sum of root-specific losses by sampled eligible-root counts. Keep all windows and seeds with their root. Preserve the root-weighted estimand under unequal cluster sizes. Save every replicate, including undefined denominators.

Report pointwise 95% percentile intervals with linear interpolation only for slots with at least 30 observed sampling units and at least 99% valid bootstrap replicates. This is an a priori reporting safeguard, not a theorem of adequate coverage. Smaller slots retain counts and point estimates. These intervals are exploratory, not simultaneous guarantees or additional confirmatory significance tests. Do not relabel them as the original six-comparison intervals or infer a universal density threshold from them. No p-values or fitted cross-source alignment curve are requested.

MSLE uses natural logarithms, `(log1p(saved_median)−log1p(y))²`, averaged over seeds within a case, windows within root, then roots. Provide all procedures, overall and per window. This evaluates saved median forecasts; the median is not generally the Bayes-optimal point action for MSLE. Different cohorts, target definitions, log bases and information access prevent direct leader-board comparisons with published DeepHawkes/CasFlow numbers. MSLE is supplementary and does not select models.

## Stage B: dimension-matched noise negative control

Use the same source-specific 6,000 TRAIN roots, 5,000 TEST roots, fixed selected candidate settings, count-law definitions, numerical score contracts and model-seed schedule as Phase 13E/F. VALIDATION is not evaluated and no hyperparameter selection is repeated. The existing I0 and I1 results are read from Stage A; existing models are neither loaded nor refitted.

The new input is I0 plus seven independent Uniform(−sqrt(3),sqrt(3)) variables. Its columns have population mean zero and variance one; this choice matches the number of columns, not their temporal meanings, marginal shapes, correlations, split opportunities or effective model capacity. It is a negative control for adding uninformative coordinates under a specific fitting procedure.

Use three noise realizations, IDs 0,1,2. Generate a matrix once for each source/role/realization in frozen lexical `(cascade_id,window_s)` order, using PCG64 with SeedSequence `[2026091801, realization, source_index, role_index]`; source indices are Weibo=0/SEISMIC=1 and roles TRAIN=0/TEST=1. Neither outcomes nor observed feature values enter random-number generation. The same matrix is reused across families and fitting seeds. Generate TRAIN and TEST separately. Save matrix hashes and matrices. Do not reject a realization because its empirical correlation or forecast result is unfavorable. The noise changes no source record or original timing field.

Hurdle uses its original one fitting seed; QRF and NGBoost each use all three seeds (20260913–20260915) **for every noise realization**. The schedule is fully crossed: 42 learned procedures, at most 48 component fits, and 630,000 new TEST forecasts/scores. Hurdle/forest/boosting code and scoring code remain byte-identical to the retained source. An isolated adapter supplies the explicit I0-plus-noise matrix. Scaling for linear models is fitted only on TRAIN. No fitting of empirical references is needed.

Fit each scheduled job once, save its fitted object before scoring, and preserve all warnings, convergence states and failures. A nonconverged likelihood fit is ineligible; its performance is withheld. Never repair a score by clipping, enlarging tail limits or dropping a row. A complete noise procedure requires all prescribed realizations/seeds and all 15,000 TEST windows per job. Incomplete procedures keep diagnostics and per-job records, but their full-sample comparisons are withheld. The original I0/I1 comparisons remain available regardless.

The noise-procedure root loss is the mean over windows, fitting seeds and the three fixed noise realizations. It is not a mixture score or inference over an unlimited population of seeds. Report each noise realization's average separately, without choosing a winner.

There are 12 supplementary absolute CRPS contrasts: noise−I0 and I1−noise, for each of three families and two sources. Both directions are interpreted using negative=lower CRPS for the first named procedure. Use 10,000 paired bootstrap vectors per source, PCG64 seed 2026091802, with the same Weibo cluster/SEISMIC root sampling and root weighting as Stage A. Reuse vectors for the six contrasts within each source. Use percentile probabilities 0.05/24 and 1−0.05/24, Bonferroni over all 12 slots, even if some are withheld. Report relative changes as descriptive points. Intervals condition on the fitted models, fixed noise realizations, selected samples and grouping assumptions. They do not capture retraining or source-selection uncertainty.

A nonsignificant noise−I0 contrast does not establish equality. I1−noise is evaluated directly. Favorable performance of noise is retained and does not trigger an alternative generator. Neither outcome isolates capacity perfectly or establishes causality.

## Execution, limits and stop rule

Synthetic unit/integration checks precede any real new fit. Synthetic fits are counted separately from the 42 real jobs. Initialization is limited to 180 seconds per worker; each real job has 2,400 execution seconds; the complete noise pass has six hours; prediction chunks contain 128 cases; numerical workers are one. Analysis has a separate 1,800-second limit. These are ceilings, not runtime promises.

The Mac runner invokes A once, verifies its output against the separately retained Linux reaggregation when present, then invokes B once. A B failure does not erase A. A unique output path and an adjacent invocation marker block accidental repeated execution. Do not automatically resume or start another directory to circumvent this guard. Package whatever completed, with interrupted/unattempted jobs explicitly labeled. Source/hash failure blocks new model work. The task ends after analysis, figures and return-package verification regardless of scientific direction.

No extra model family, new data, further noise realization, feature-importance sweep, timing permutation, threshold search, PPO training, or subsequent experiment is authorized by this protocol. The user's current instruction authorizes this specific supplement to the earlier closed experimental sequence; earlier records are preserved.

## Methodological sources

- Hooker, Mentch and Zhou, unrestricted permutation and extrapolation: https://arxiv.org/abs/1905.03151
- Strobl et al., predictor-type effects in random forests: https://doi.org/10.1186/1471-2105-8-25
- Gneiting, matching point forecasts to losses: https://arxiv.org/abs/0912.0902
- Cawley and Talbot, model-selection bias: https://www.jmlr.org/papers/v11/cawley10a.html

These sources motivate interpretation and safeguards; none establishes the outcome of the proposed supplementary experiments.
