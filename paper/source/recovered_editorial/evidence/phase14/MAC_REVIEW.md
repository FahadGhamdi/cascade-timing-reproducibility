# Mac Phase 14 review

Completed the single authorized Mac invocation of A followed by B. No previous execution marker, run directory or return archive existed at preflight. The Linux Stage A reference supplied inside the kit was retained and was not treated as a prior Mac invocation. The execution lock remains in place. The shell process-list check was unavailable in the sandbox; prior-execution checking used the workspace artifacts. No runner restart or alternate output directory was used.

## Inputs and environment

Independently verified all 108 kit MANIFEST entries by byte count and SHA-256 before and after execution. The exact Phase13F archive is 160,964,430 bytes with SHA-256 592e185fc9a0ad96265b407af71a3e80e9d66ccbe9da140a3bd32c36bfb51ce0. Its identity was checked again after execution. The runner verified CRC and all 496 parent payload hashes, TRAIN bindings, and TEST byte bindings. Existing Phase13C Python 3.12.14 environment previously used by Phase13F matched every one of the 33 locked dependency versions and was used unchanged. No installation was needed; setup.log records verification.

## Synthetic checks and A

All 17 synthetic unit tests passed with zero errors/failures. Three synthetic procedure fits used four component fits; 18 synthetic scores and 18 replay scores were checked. These counts are separate from real work.

A reaggregated 600,000 saved rows for 24 procedures. It performed zero new fits, predictions or CRPS computations and calculated 600,000 supplementary saved-median MSLE values, producing 96 MSLE summary rows, 360 stratum-level slots, 90 timing contrasts and 4,000 bootstrap vectors. Six retained tables and the complete bootstrap arrays matched the supplied reference at atol 1e-8 / rtol 1e-10; maximum historical aggregate metric difference was 4.547473508864641e-13.

All 90 timing point estimates are present: 64 negative (favor I1) and 26 positive. Direction varies by family, window and bin; no universal threshold is established. There are 84 exploratory pointwise intervals. Six intervals are withheld for the SEISMIC 3,600-second window at bins 0 and 1–2 (26 and 20 sampling units), for all three families. Their counts and point estimates remain present. At zero nonroot events, timing defaults are deterministic; procedure differences cannot be attributed to observed within-prefix event times.

## B and independent accounting

All 42 scheduled jobs completed once: 42 real procedure-fit attempts, 48 component-fit calls, 630,000 attempted and returned TEST predictions, and 630,000 score attempts and successes. There are zero prediction failures, score failures, nonconverged jobs, timeouts, or recorded warnings. All per-job reports, process logs, warning fields and failure files remain present, including empty failure lists. Independently checked scheduled job identities, model file hashes without loading models, score-stream unique keys and row-status counts, and agreement with final accounting. The numerical and time budgets were not increased. No old model was refitted, no TRAIN/VALIDATION performance was evaluated, and no new selection occurred.

All six source/family procedures and all 12 supplementary contrasts are available; none is withheld. All three noise realizations and their separate summaries are retained. B used 20,000 bootstrap vectors across the two sources with a separate Bonferroni family of 12.

Noise-minus-I0 point differences are negative for Weibo Hurdle (-0.001998) and SEISMIC QRF (-0.215576), and positive for Weibo QRF (+0.953466), Weibo NGBoost (+0.033271), SEISMIC Hurdle (+0.026735) and SEISMIC NGBoost (+0.174242). Every corresponding adjusted interval includes zero; this does not establish equivalence. I1-minus-noise is negative with adjusted intervals entirely below zero in all six source/family cases. All directions, including favorable noise results, are retained in stage_b/RESULTS_REPORT.md and the full tables. These are post-13F supplementary results conditional on fitted models, fixed noise realizations and sampling assumptions, not a new independent primary test or a pure capacity/causal identification.

## Visual review and limits

Visually reviewed both figures_a PNGs and all three figures_final PNGs: strata_weibo, strata_seismic and noise_contrasts. Titles, labels, legends, counts and intervals are readable without visible clipping. No figures were edited. Narrow intervals in the noise plot are compressed by its shared panel scale; exact limits remain in the tables. PDF files were retained and covered by archive integrity checking but were not separately rendered for visual review. No models were loaded or scientific scores recomputed during the independent audit. The manuscript and frozen source files were not edited.

## Return packages

The automatic archive was retained unchanged and independently passed unique/safe entry-name checks, exact inventory against its manifest, every payload byte count and SHA-256, ZIP metadata sizes, all CRC checks, and a full-archive SHA-256 calculation. Its verification receipt is included in this run.

This review and independent audit are added after automatic packaging. A new final archive is therefore created with package14.package on the existing run only. The final archive is identified by FINAL_RETURN_VERIFICATION.json in recovery and the final user response. Its independent verification occurs after packaging and is stored alongside it to avoid a self-referential archive hash. No subsequent experimental phase is started.
