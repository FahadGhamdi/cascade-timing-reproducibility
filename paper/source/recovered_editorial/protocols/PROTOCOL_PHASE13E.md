# Phase 13E: bounded selection for the two-source information study

Protocol: `BRACE13E-shared-capacity-selection-v1`. Prepared on 12 September 2026 after the Phase 13D Mac return, before any Phase 13B VALIDATION performance evaluation. This is a prospectively frozen analysis record for existing archives, informed by disclosed TRAIN pilots; it is not a journal-accepted registered report. `CONFIG.json`, `JOBS.json`, and the executable source specify the implementation. Earlier protocols and failed results remain unchanged.

## 1. Question, scope, and decision

The research question is: **How much do prefix timing summaries improve probabilistic forecasts of recorded cascade growth beyond prefix size, within several established model families, on two archived sources?** Hurdle, QRF, and NGBoost are the three primary families. Poisson, NB2, and two empirical procedures provide competing references. No new learning algorithm is claimed.

The Phase 13D certified calculation completed all 1,536 archived NGBoost distributions. Its numerical change supports using that score implementation; it does not retrospectively erase the 17 Phase 13C score failures. The TRAIN pilot reductions for NGBoost were 5.57% on Weibo and 8.58% on SEISMIC. These observations motivated this study but are not held-out evidence.

CASPER did not qualify under the declared adapter and budget: 12 nonempty attempts, 11 iteration limits and one timeout, plus six empty cases without optimization. Its predictions and scores remained zero. This implementation branch is closed for the present study. No published CASPER accuracy comparison follows from it. A missing qualified process baseline limits comparisons with specialized cascade forecasting methods, but does not invalidate the narrower within-family information question.

## 2. Frozen data and target

The Phase 13B contract is inherited unchanged. Each source has 6,000 TRAIN roots, 2,000 VALIDATION roots, and 5,000 future TEST roots. Only TRAIN and VALIDATION are included here: 16,000 roots and 48,000 rows across both sources. Their eight compressed feature/target files were copied exactly from the verified Mac preparation and checked against the decompressed portable hashes. TEST tables and TEST cohort rows are absent from this kit.

For each nonroot record at root-relative integer time t, observed prefixes are `[0,w)` for w in {300,900,3600} seconds. The response is the recorded count in `[w,86400)`. The endpoint is 24 hours after the root, not 24 additional hours after prediction. Remove exactly the designated root record; retain other zero-time records, timestamp ties, and repeated activity. The target is recorded activity, not identified independent people or complete real-world propagation.

Weibo roles are disjoint by root user; all roots in the release share one publication day. This is retrospective evaluation, not chronological generalization. SEISMIC uses disjoint chronological blocks with label maturity and excludes all 18,000 roots already used in the retained legacy membership ledger, plus duplicated root IDs. Source popularity selection, shared events/participants, and historical availability remain limitations. Do not pool raw CRPS across sources or relabel the old 24-hours-after-prefix scores as this target.

## 3. Information sets

I0 has `log(1+n_prefix)` and `log(window_seconds)`. I1 adds seven summaries computed strictly from observed prefix records: first-event fraction, recency fraction, median-gap fraction, gap coefficient of variation, zero-gap fraction, last-quarter fraction, and last-tenth fraction. Exact formulas and empty-prefix values are in the inherited data contract and `vendor/feature_contract_13b.py`.

IDs, group IDs, absolute origin times, followers, text, full-cascade structure, and responses are excluded from the feature matrix. Target vectors are separate from feature records, and prediction rejects records carrying `future_count`. Linear-family standardization is fitted only on TRAIN. Forests and boosting use the unstandardized, fixed feature transformations. The three windows of every root remain in the same role; each root contributes three training rows and receives equal aggregate evaluation weight.

I0 and I1 use the same candidate setting and seed schedule within a source/family. This controls the declared hyperparameter choice; it does not make their parameter counts, effective complexity, or information identical. The contrast measures predictive value under these procedures, not the causal effect of changing social timing.

## 4. Models and candidates

Candidates are ordered as listed, beginning at index 0. No additional candidate, feature, seed, or training restart is introduced after VALIDATION is scored.

| Family | Four candidates | Fixed details |
|---|---|---|
| Hurdle | count ridge 1, 0.1, 0.01, 0.001 | Logistic activity gate, C=1; conditional positive count is 1+NB2 |
| NB2 GLM | ridge 1, 0.1, 0.01, 0.001 | Joint penalized likelihood for log-link mean and common size |
| Poisson GLM | ridge 1, 0.1, 0.01, 0.001 | Log link, TRAIN standardization |
| QRF | (depth,leaf) = (8,50), (8,10), (12,50), (12,10) | 128 trees, bootstrap, all features, one worker |
| NGBoost | (stages,depth) = (100,1), (300,1), (100,2), (300,2) | Leaf minimum 10; learning rate 0.03 |
| Conditional empirical | k = 250,100,50,25 | Same-window neighbors in log-prefix size, lexical root-ID tie break |

The unconditional empirical reference has one fixed distribution for each window, using all TRAIN responses at that window. Conditional empirical uses equal mass on the k nearest TRAIN roots in that window. These references have only I0 and are not added to the six primary contrasts.

Hurdle uses a Bernoulli activity model and the **shifted** positive law Y=1+NB2; it is not fitted as a zero-truncated NB. Gate settings are fixed: lbfgs, C=1, tolerance 1e-7, maximum 1,000 iterations. NB slope coefficients have L2 penalty; the intercept is unpenalized. Intercept/slopes are bounded in [-20,20], size in [0.001,1e6], with L-BFGS-B limits 1,000 iterations/1,500 function evaluations, ftol=1e-10, gtol=1e-6. Boundary activity is reported. Poisson uses maximum 1,000 iterations and tolerance 1e-7. Degenerate all-zero/count-one branches use the explicit constant law without pretending an optimizer was called.

QRF routes all original TRAIN rows through each bootstrap-grown tree and averages normalized leaf memberships. The saved model includes those memberships and TRAIN responses; this convention is inherited from the pilot and is not silently substituted with a different forest distribution.

NGBoost fits Normal LogScore to log1p(Y), with natural gradients, full rows/features at each stage, no VALIDATION-based early stopping, and internal tolerance 1e-4. Its frozen count mapping is X=max(0,floor(exp(Z)-0.5)). This is a rounded transformed-Normal procedure, not a native negative-binomial NGBoost distribution. Returned stage counts are recorded; the prescribed boosting length is a training budget, not a likelihood-convergence certificate.

QRF and NGBoost use seeds 20260913, 20260914, 20260915. Deterministic procedures use the first seed only. The stochastic estimand is the average loss across these fixed seeded procedures, not the score of a mixture CDF and not inference over an unlimited seed population.

## 5. Finite execution budget and failure handling

| Quantity | Upper bound |
|---|---:|
| Learned procedures | 144 |
| Component fit calls | 160 |
| Reference preparations | 10 |
| Candidate/source/information/seed jobs | 154 |
| VALIDATION distributions/score rows | 924,000 |
| Selected model objects, including references | 40 |
| New fits after selection | 0 |
| TEST evaluations, bootstrap draws, CASPER attempts | 0 |

Each job fits on 18,000 TRAIN rows and evaluates 6,000 VALIDATION rows. Initialization has a 180-second limit and execution a 900-second limit; the global main-process budget is six hours. Packaging is outside this model-execution budget. These are limits, not predicted runtime. Jobs are sequential with numerical thread counts set to one. Reference jobs run first; learned jobs interleave source, information set and seed within each ordered candidate/family. `JOBS.json` fixes the full order.

The output directory must not already exist. Each scheduled fit is attempted at most once. A timeout is preserved, not retried; remaining jobs proceed within the global budget. If that budget ends, remaining jobs are explicitly unattempted. Reports distinguish requested procedures, component fit calls, forecasts attempted/returned, and score successes/failures. Counters from an interrupted worker are labeled lower bounds because its last chunk may not have been fully logged.

Prediction or score failures retain root/window identity and available distribution parameters. Do not drop failed windows and then report a complete-sample mean. Nonconverged likelihood fits can be inspected but cannot qualify a candidate. Forest/boosting jobs must finish their prescribed fitting procedure and all predictive checks. A source/family can remain unsupported if no candidate completes its entire information/seed comparison. The resulting inference family still has six slots.

## 6. Scores and diagnostics

Primary loss is discrete CRPS, sum over k>=0 of [F(k)-1{Y<=k}]². Empirical distributions use the exact finite-support identity, up to floating-point arithmetic. Poisson/NB2/Hurdle use the inherited score routine with an omitted-tail bound of 1e-8 and maximum grid 1,048,576. Parameter means above 1e7 are rejected under the fixed numerical contract, not clipped.

Rounded transformed-Normal CRPS uses the exact Phase 13D scoring source: a direct body plus adaptive convex tail bounds, target 1e-8, direct range 4,096 to 1,048,576, tail/body switch 0.1, at most 65,536 blocks, far index at most 2^50, and 30 seconds per score. The returned error bracket is recorded. The analytic tail certificate and floating-point guard are not a formal directed-rounding proof of every machine operation. No new truncation or relaxed tolerance is selected on VALIDATION.

Secondary outputs are Brier loss for no growth, median absolute error, 90% interval score and width, and coverage of 50%, 80%, 90%, and 95% central intervals. Count calibration uses both nonrandomized PIT-bin mass and randomized PIT. The randomized uniform is fixed by SHA-256 of source/root/window with salt `BRACE13E-PIT-v1`, shared across models and seeds. Histograms have ten equal bins; no-growth reliability also has ten fixed probability bins. Coverage alone is not calibration. No recalibration is fitted.

Each source/seed/model aggregate averages three prefix losses within a root, then roots. All roots have the same three windows. VALIDATION calibration is descriptive and shares its selection limitation. Saved row scores support later per-window diagnostics without refitting.

## 7. Selection rule and model lock

For each source and learned family, a candidate is eligible only if **both I0/I1 and all prescribed seeds** pass fit and full-score requirements. Its criterion is the average VALIDATION root-mean CRPS over both information sets and all those seeds. Select the minimum; values within 1e-8 of the best tie and choose the lowest declared candidate index. This avoids selecting the setting that merely maximizes the apparent I1 benefit. References choose k by their I0 validation CRPS; the unconditional reference has one candidate.

Save the selected TRAIN-fitted model objects and their SHA-256 values in `MODEL_LOCK.json`. Do not refit on TRAIN+VALIDATION. Keep all nonselected models, scores, warnings, and failures. The six VALIDATION contrasts in `VALIDATION_CONTRASTS.json` are **selection-set descriptive results**, not unbiased evidence or hypothesis tests. No bootstrap is conducted at this stage. Selection-set improvement is not a gate for proceeding to the planned TEST evaluation of qualified models; null or adverse VALIDATION differences must not trigger new tuning.

## 8. Locked plan for the subsequent TEST evaluation

After the selection package is reviewed for integrity, apply the saved models once to the original 5,000 TEST roots per source, without fitting or feature changes. At most 40 selected models produce 600,000 TEST row forecasts altogether. TEST remains excluded from Phase 13E. Missing family slots and failed full-sample comparisons are retained explicitly.

The six primary contrasts remain Hurdle/QRF/NGBoost times Weibo/SEISMIC. For every root, first average its three window losses and then its prescribed seed losses. Report delta=mean(CRPS_I1−CRPS_I0) and relative reduction=1−mean(CRPS_I1)/mean(CRPS_I0). Negative delta favors timing. Relative improvement is undefined if the I0 denominator is zero. A 2% relative reduction is the inherited practical reference, not a publication criterion.

Use 10,000 paired bootstrap draws, seed 20260916, reusing the same resampling indices across model comparisons within each source. For Weibo sample root-user clusters uniformly with replacement; compute total sampled root losses divided by total sampled root counts, preserving the root-weighted estimand. For SEISMIC resample roots, with unresolved cross-root dependence stated. Keep all windows/seeds of a root together. These intervals are conditional on the fitted models, selected samples, and declared resampling assumptions; they do not include model-selection, source-selection, or retraining uncertainty.

The family alpha is 0.05 over six contrasts. Use paired percentile bounds at 0.05/12 and 1−0.05/12 for each absolute contrast, with linear empirical-quantile interpolation. Relative reductions are point summaries; the six absolute contrasts carry the primary uncertainty statements. Describe this as bootstrap Bonferroni adjustment, without claiming exact finite-sample coverage. Intervals crossing zero do not establish equivalence. Do not reduce multiplicity because a slot fails.

Report secondary per-window scores, PIT/reliability, and intervals for the full selected set, with no new primary significance claims. For seed-replicated families average diagnostic bin masses across seeds, preserving their procedure-average interpretation. Retain the Phase 13B descriptive sensitivity excluding duplicate-token-flagged Weibo TEST roots: use the frozen flags and existing predictions only, no refit, no new significance tests, and no alteration of the primary sample. It cannot remove training effects of duplicates or reconstruct unique social events.

## 9. Completion and paper claims

The planned sequence is finite: selection, fixed-model TEST evaluation, then synthesis and manuscript revision. A further repair would require a demonstrated implementation defect and a separate record; unfavorable scores do not justify it. Preserve a missing domain baseline as a limitation rather than filling it with a failed or misidentified method.

The defensible contribution sought is a controlled, reproducible estimate of incremental timing information for count distributions and calibration across two archives, with competitive simple references. Timing features, QRF, NGBoost, proper scores, and count PIT are established techniques. The work does not demonstrate causal containment, necessity of reinforcement learning, superiority to full published CASPER/TiDeH, generalization to all social platforms, or journal acceptance.

## Primary methodological sources

- [Meinshausen, Quantile Regression Forests, JMLR 2006](https://www.jmlr.org/papers/v7/meinshausen06a.html).
- [Duan et al., NGBoost, ICML 2020](https://proceedings.mlr.press/v119/duan20a.html).
- [Czado, Gneiting and Held, Predictive Model Assessment for Count Data, Biometrics 2009](https://onlinelibrary.wiley.com/doi/10.1111/j.1541-0420.2009.01191.x).
- [Cawley and Talbot, Model Selection and Subsequent Selection Bias, JMLR 2010](https://www.jmlr.org/papers/v11/cawley10a.html).
- [Zhang et al., CASPER, ICML 2022](https://proceedings.mlr.press/v162/zhang22a.html).
- [scikit-learn documentation: data leakage and preprocessing](https://scikit-learn.org/stable/common_pitfalls.html).

The inherited literature matrix contains the cascade-specific precedents. These sources motivate the study design; they do not establish that its unobserved TEST result will be positive.
