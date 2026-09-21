# Phase 13F — one locked TEST evaluation

Prepared 13 September 2026. Protocol ID: `BRACE13F-locked-test-v1`.

This implements Section 8 of the Phase 13E protocol and the Phase 13B data contract. The model grid, information sets, selected settings, score limits and six primary contrasts are unchanged. Phase 13E VALIDATION outcomes are known. No new TEST model evaluation was performed while preparing this kit; TEST tables were copied and hashed, and cohort metadata were checked. Prior archive metadata/data-preparation access is disclosed rather than described as never having accessed a TEST byte.

## Evidence permitting this step

The uploaded Phase 13E return has SHA-256 `b38668401ae3e1094fa8c9853983348b99f6d5bed525a3f397cbd4ee7a8770a8`, 370,201,877 bytes, and 1,756 manifest payloads. All were checked. The 133 complete VALIDATION means were independently reaggregated from saved row scores; the maximum difference was 2.842170943040401e-14. All 14 source/family selection decisions and 40 selected model hashes were verified.

All 21 ineligible jobs had numerical score failures and converged fits. Their 74 score failures were confined to Weibo: Hurdle 11, NB2 9, NGBoost 54. The selected 40 models completed VALIDATION. Their future TEST completeness is unknown. Neither incomplete candidates nor their failures are erased by moving to TEST.

## Inputs and exact model binding

The lightweight kit contains the four exact Phase 13B TEST feature/target tables and filtered TEST cohort: 5,000 roots per source, 15,000 windows per source, 30,000 distinct target rows altogether. Features and responses stay separate. Prefix windows are 300/900/3600 seconds and the endpoint is 86,400 seconds after the root, with strict `[0,w)` prefix and `[w,86400)` response.

The preceding return ZIP remains an external input already on the Mac. Verify its exact size/hash and all manifest entries, then extract only the 40 model objects identified by the immutable `MODEL_LOCK.json`. Their combined size is 85,494,884 bytes. No pickle object is loaded until its binding is verified. The old model/feature/score implementations are copied byte-for-byte under `locked_source/`; Python/package versions remain pinned. Models use the same TRAIN-fitted scaling, forest weights and count-law definitions as Phase 13E.

Weibo metadata flags are `0`/`1`. SEISMIC's duplicate flag `unavailable_without_event_ids` is retained as unknown; it is not converted to zero. These metadata fields never enter the feature matrix. No raw event-data recovery or reinterpretation is needed here.

## Execution and stopping

Run once in a new output directory. The runner checks integrity and 18 synthetic tests, then verifies/extracts the locked models. The optional `--verify-only` mode stops before loading any real model object or evaluating TEST; it is for source preparation, not the requested Mac experiment.

The real pass has 40 jobs, one per locked model. The upper bound is 600,000 TEST forecast/score rows; 200,000 complete model/root summaries; 120,000 complete source/family/information/root summaries after seed averaging. There are 24 source/family/information procedures: five learned families with I0/I1 and two I0 references, on two sources. New fits, selection, TRAIN/VALIDATION rescoring and CASPER calls are zero. `CountProcedure.fit` is guarded against invocation inside the evaluator.

Fixed execution details not specified in the earlier statistical plan: one numerical worker, prediction chunks of 128, 180 seconds initialization per job, 1,800 seconds execution per job, and a six-hour global forecast-pass limit. The larger per-job limit accommodates 15,000 TEST rows versus 6,000 VALIDATION rows. Setup, analysis and packaging are separate. Analysis has a 1,800-second budget; figure rendering has its own short limit. These limits are declared before TEST scoring, not tuned on its outcomes. References run first, followed by the deterministic frozen job order in `TEST_JOBS.json`.

Each job is attempted at most once. Preserve timeouts and continue only to remaining scheduled jobs within the global budget. Record unattempted jobs if it expires. A preexisting run blocks another invocation. No automatic restart/resume, substitution, new fit, or score-limit revision is allowed. Interrupted counters are explicitly lower bounds. Packaging and viewing existing results do not trigger model work.

## Completeness and metrics

Use the exact Phase 13E score routines, including the Phase 13D rounded-log1p-Normal certificate and the absolute 1e-8 score tolerances. Do not change distributions, clip predictions, relax the tail budget, or drop a failed root. Every row retains its status and identity. Parametric distribution parameters are saved; empirical CDFs are defined by the locked model and frozen query.

A model's complete-sample means are withheld if any of its 15,000 rows fail. A seeded information procedure is complete only when all its prescribed seed jobs are complete. A primary I1−I0 comparison requires both complete procedures. A surviving seed or selected subset is not substituted for the declared procedure. The six-comparison multiplicity family remains fixed even with unavailable slots. Other complete procedures can still be reported.

Primary CRPS, zero-growth Brier, median absolute error, 90% interval score/width, 50/80/90/95% coverage, randomized and nonrandomized count PIT, and ten-bin no-growth reliability follow Phase 13E unchanged. Aggregate the three windows within root, then prescribed seed losses within root, then roots. This averages losses of fixed seeded procedures; it does not score a mixture CDF or treat seeds/windows as independent observations. Calibration-bin masses and counts are averaged over seeds; these are not counts of additional independent roots. Per-window and calibration outputs are secondary descriptive analyses; no recalibration is fitted.

## Primary inference, unchanged

There are six absolute CRPS contrasts: Hurdle/QRF/NGBoost × Weibo/SEISMIC. Delta is mean root CRPS(I1)−mean root CRPS(I0); negative favors timing. Report relative reduction `1−mean(I1)/mean(I0)` as a point summary, undefined for a zero I0 denominator. The inherited 2% reference is descriptive, not an acceptance or stopping gate.

Use 10,000 paired bootstrap draws per source with seed 20260916. This is 20,000 source resampling vectors and up to 60,000 contrast replicates, not 60,000 independent samples. Implementation details are fixed before TEST: NumPy PCG64, source order Weibo then SEISMIC, lexical unit order, batches of 100, int64 sample indices. Reuse the exact same indices across the three contrasts in each source and retain a SHA-256 digest of each index stream. Placeholder internal columns for unavailable comparisons are masked and never reported as zero effects.

For Weibo, sample root-user clusters uniformly with replacement and divide total sampled root-loss sums by total sampled root counts. This preserves the root-weighted estimand when cluster sizes differ. For SEISMIC, resample roots; its unresolved cross-root event dependence remains a limitation. Keep all windows and seeds with their root. Use percentile quantiles 0.05/12 and 1−0.05/12, with linear interpolation, for each absolute contrast. These are approximate 99.1667% intervals with Bonferroni adjustment over six contrasts for family alpha 0.05, conditional on the fixed models, selected sample and resampling assumptions. They do not incorporate source selection, retraining or model-selection uncertainty and do not guarantee exact finite-sample coverage. Crossing zero does not establish equivalence.

Keep the predeclared Weibo sensitivity: remove duplicate-token-flagged TEST roots from descriptive contrasts only, using existing scores, without refitting, replacing roots, changing the primary sample or adding significance tests. If the primary comparison is incomplete, its sensitivity is withheld too. This cannot remove effects of duplicates during training or recover unique social events.

## Outputs and interpretation

The return preserves all 40 input models, raw row scores, failures, complete root summaries, procedure metrics, six comparison slots, bootstrap replicates/design, duplicate sensitivity, calibration and figures, with logs and integrity manifests. Figures show adjusted absolute contrasts, all complete procedures including references, and count PIT panels. Missing procedures are marked or omitted as unavailable rather than assigned favorable values.

After this pass, the substantive task is analysis and manuscript synthesis. A negative result does not trigger a new grid, source, seed, or experiment. A demonstrated implementation defect would require a separate transparent correction record; no such future repair is preauthorized by unfavorable performance. The potential contribution is a two-source empirical estimate of timing information's incremental value for count distributions, not a new algorithm or a causal containment result. The unqualified CASPER adapter still does not establish superiority to published CASPER/TiDeH.

## Sources

The separation of selection and evaluation addresses documented selection bias: [Cawley and Talbot, JMLR 2010](https://www.jmlr.org/papers/v11/cawley10a.html). Count-specific calibration and proper-score assessment have established precedents: [Czado, Gneiting and Held, Biometrics 2009](https://onlinelibrary.wiley.com/doi/10.1111/j.1541-0420.2009.01191.x). See the inherited protocols for the QRF, NGBoost and cascade-method precedents. These sources justify design choices, not the outcome of the unexecuted TEST comparison.
