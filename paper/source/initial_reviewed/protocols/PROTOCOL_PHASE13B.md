# Phase 13B: frozen data and information contract

Protocol ID: `BRACE13B-count-time-v1`. Frozen on 12 September 2026 after the verified Phase 13A Mac return and before this phase prepares selected event records. Prior results and source-wide metadata audits are known. This is a new prospective record of analysis decisions for already archived data, not a claim of untouched source metadata or a registered report accepted by a journal.

## Research question and primary family

Within each of Hurdle, QRF and NGBoost, compare a prefix-size information set I0 with I1 adding timing summaries. There are six primary contrasts: three families times two sources. For each source separately, the primary contrast is mean discrete CRPS(I1) minus mean discrete CRPS(I0), averaging the three prefix losses within each root first. Do not pool raw CRPS across sources with different scales. Negative favors I1.

A 2% relative reduction is a prespecified practical-effect reference, not an empirically established universal threshold or an acceptance gate. Report effect magnitude and uncertainty whether it passes this reference or not. If baseline CRPS is zero, relative improvement is undefined; report the absolute contrast. A confidence interval crossing zero does not establish equivalence. The six-contrast multiplicity family remains fixed, including if a model comparison is incomplete. Fit grids, seeded-procedure interpretation, interval implementation and numerical score limits will be fixed in the fitting protocol after a small TRAIN-only cost/compatibility pilot; no model is fitted here.

## Target, prefix and source selection

For root-relative integer event time t, the prefix contains nonroot records with `0 <= t < w`; the response counts records with `w <= t < 86400`. Prefix durations are exactly 300, 900 and 3600 seconds. This is a root-based 24-hour endpoint, whereas legacy BRACE results used an additional 24 hours after a prefix. Old scores are not renamed or merged with this experiment.

Weibo uses the identified bare root-marker token at zero, regardless of its position in a path list. SEISMIC uses the designated first source row at zero. Remove exactly that root, retaining other zero-time records and timestamp ties. Sort the retained times; preserve repeated activity records. Neither source establishes unique-person or independent-event counts. Weibo's root-user IDs are used only for grouping; they are not model inputs. No follower marks, global graph, origin date, root ID or outcome enter I0 or I1.

The sample comprises 6,000 TRAIN, 2,000 VALIDATION and 5,000 TEST roots per source. Membership is selected from source/root/group identity, root origin, prior-use ledger and declared quality status. Counts, labels and model scores do not rank candidates. Original source selection for popularity still limits the target population.

- **Weibo:** exclude two roots with invalid timestamps (80431, 89151) and seven with missing root-user IDs (87919, 87962, 87997, 88004, 88035, 88065, 88066), as proposed after 13A. These are known metadata exclusions, not a hidden deletion after scoring. Hash root users into 60/20/20 role pools, then select the fixed root count in each pool by a separate root hash. The same root user cannot cross roles. This is a retrospective, user-disjoint source evaluation; all source roots were published within one day. Other shared participants or events may still connect roots.
- **SEISMIC:** exclude all 18,000 roots in the retained 10C training, 10C test, Phase11 test and 12D test membership ledgers, plus all entries of the four duplicated source root IDs. Preserve raw ID strings, including scientific-notation strings; never coerce identity through a float. Select TRAIN roots with origin day <4, VALIDATION with 5.05<=day<7, and TEST with day>=8.05. Hash within each block to obtain the fixed sample sizes. Verify the latest earlier response endpoint precedes the earliest later root origin for both TRAIN→VALIDATION and VALIDATION→TEST. This enforces label maturity in a retrospective archive experiment; it does not establish live historical availability or remove the release's popularity selection.

No selected root is silently replaced following an event-preparation failure. Membership is saved before event preparation. The model-fit protocol must retain this membership unless a separately documented defect requires a new protocol version.

## Integer storage and feature contract

Store integer sufficient statistics to avoid turning platform-dependent logarithm or square-root rounding into a data-reproduction failure. `feature_values` supplies the exact whitelist for the subsequent model matrix.

| Information | Feature | Definition |
|---|---|---|
| I0 | log1p_n_prefix | log(1+n), with n the nonroot prefix count |
| I0 | log_window_seconds | log(w); the same fixed endpoint applies to every prefix |
| I1 addition | first_event_fraction | first nonroot event time / w; 1 if n=0 |
| I1 addition | recency_fraction | (w−last nonroot event time) / w; 1 if n=0 |
| I1 addition | median_gap_fraction | median consecutive nonroot gap / w; 0 if n<2 |
| I1 addition | gap_cv | population gap standard deviation / mean; 0 when no positive gap mean exists |
| I1 addition | zero_gap_fraction | fraction of consecutive nonroot gaps equal to zero; 0 if n<2 |
| I1 addition | last_quarter_fraction | fraction of prefix records at t>=0.75w; 0 if n=0 |
| I1 addition | last_tenth_fraction | fraction of prefix records at t>=0.9w; 0 if n=0 |

I0 has two model inputs; I1 has nine. Sentinel interpretation is fixed and n remains available, so empty prefixes are distinguishable from active prefixes with zero-valued interval statistics. No learned imputation or scaling is performed here. If a later model requires scaling, fit it on TRAIN only. Do not add count duplicates such as both root-inclusive and nonroot log counts as separate predictors.

The integer table contains first/last times, counts and exact sums/squared sums of gaps; the median is stored as twice its value. These are sufficient to obtain the listed features. A separate prefix stream retains timestamps below 3,600 seconds for a domain-method feasibility study, without future timestamps. Targets are in separate files and are not accepted by the feature function.

## Quality sensitivity and uncertainty

Keep the nine excluded source roots in the public quality ledger with their recorded sizes and reasons. There is no defensible exact target for an event with an unknown timestamp; do not assign it to a guessed time, count it as non-growth, or promise that excluding two large roots is harmless. Primary findings are conditional on the eligible release. The original record files remain available for any later explicitly labeled partial-record analysis.

Exact duplicate path tokens remain under the released-record estimand. For a fixed descriptive sensitivity after the primary analysis, also report paired test-root contrasts after excluding Weibo TEST roots flagged for exact duplicate tokens, with no refitting, replacements or new significance tests. This evaluates the influence of duplicate-affected test cases; it does not remove their possible influence during training or recover unique social events. A distinct unique-event dataset cannot be constructed from these assumptions alone.

For final uncertainty, aggregate losses within root first. Weibo resampling must keep a root user's roots together and estimate the root-weighted mean through total loss/total root counts in each resample. SEISMIC has no root-user grouping field, so root resampling carries the explicitly unresolved event-dependence limitation. Repeated prefixes or seeds are not independent observations. Calibration diagnostics are secondary and must use a count-appropriate PIT construction, Brier for no growth and fixed interval diagnostics.

## Outputs and completion

This stage produces cohort and quality ledgers, integer feature tables, separate response files, prefix-only event streams, and a TRAIN-only pilot membership of 512 fit and 128 internal-validation roots per source. The pilot partition also respects available group IDs and uses identity alone. No pilot is executed here.

The selected tables contain 26,000 roots and 78,000 prefix rows overall. Only TRAIN prefix-count summaries may be printed for estimating computational scale; do not summarize held-out targets, calculate scores, tune models, bootstrap, or execute author model code. Materializing and hashing an outcome file is distinguished from using it for model selection or evaluation.

Run data preparation once on Mac. The Mac task runs 13 synthetic contract tests, reconstructs these outputs from the pinned raw sources, compares every portable file to the reference, preserves a failure if present, and stops. During reference construction a nonmatching local source copy stopped before event preparation; the same pinned edition was recovered. A subsequent parser failure on an integral timestamp written as `1e+05` was preserved and corrected using exact Decimal conversion, with a regression test. Neither correction changes the cohort, target or feature contract. Successful preparation closes data engineering for this contract. The next substantive task is the bounded TRAIN-only baseline/cost pilot, followed by one frozen held-out comparison—not another unrestricted data search or a return to PPO.

## Source rationale

The strict prefix and fixed-root endpoint conventions were checked against [CasFlow preprocessing](https://github.com/Xovee/casflow/blob/master/gene_cas.py). The selected retweet release and its collection description come from [SEISMIC](https://snap.stanford.edu/seismic/). Timing features have established predictive relevance in [Cheng et al.](https://arxiv.org/abs/1403.4608), so the proposed novelty must be an empirical insight about their incremental value for count distributions and calibration, not discovery that timing can help. [CASPER](https://proceedings.mlr.press/v162/zhang22a.html) motivates the finite-horizon domain candidate; a mean and variance alone do not define the full count CDF required for CRPS. The retained 22-study literature matrix records further precedents and implementation distinctions.
