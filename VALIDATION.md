# BRACE Experimental Reproduction: Final Verification Report

**Review date:** September 21, 2026  
**Manuscript:** *What Does Timing Add to Size? Probabilistic Forecasts of Recorded Cascade Growth on Two Archives*

This English version translates the final Arabic verification report supplied with the reproduction controller. It documents the completed review; it does not represent a new experimental run.

## Assessment

The evidence supports completion of model retraining and selection, test evaluation, and noise-control fitting on the Mac, with scientific results matching the original outputs. Training was completed across two sessions rather than one uninterrupted run. Evaluation used the locked historical parent archives. SHA-256 identity of the 40 selected model files provides the documented link between the retrained models and the original models used for evaluation.

The distributed reproduction package consists of the updated controller and the original `ORIGINALS_PAYLOAD_01.zip`, `ORIGINALS_PAYLOAD_02.zip`, and `ORIGINALS_PAYLOAD_03.zip` archives. The small audit return alone is not the reproduction package, and the controller alone does not contain the large datasets. Completed experiments do not need to be repeated to finish packaging.

## Documented execution results

| Component | Result |
|---|---|
| Training and selection | 154 job reports: 87 adopted from the preceding session and 67 executed during continuation; 133 eligible and 21 preserved as ineligible. |
| Validation scoring | 924,000 attempts; 923,926 successes and 74 numerical failures matching the original run; 160 component-fitting calls. |
| Selection artifacts | `CANDIDATE_TABLE.json`, `SELECTION_REPORT.json`, `MODEL_LOCK.json`, and `VALIDATION_CONTRASTS.json` are byte-identical to their original counterparts. |
| Selected models | Locally recorded digests for all 40 newly selected model files match the originals. Those digests were checked against the original model bytes available in the independent review workspace. |
| Test evaluation | 40 completed jobs; 600,000 successful scores and no scoring failures. |
| Noise controls | 42 completed jobs; 48 component-fitting calls and 630,000 successful scores, with no scoring failures. |
| Environment | Python 3.12.14; all 33 dependencies match the lock according to the attached environment check. |
| Training budget | Original limit: 21,600 seconds. A conservative upper bound of 3,080 seconds was charged to the earlier session, followed by approximately 618 seconds for training continuation and its review. |

The 74 validation-scoring failures do not conflict with the absence of scoring failures in test evaluation and noise controls. The original failures remain part of the experimental record and were not removed to improve the outcome.

## Independent inspection of the submitted evidence

- The ZIP/CRC check passed. The archive contains 2,022 members, including the manifest itself; all 2,021 manifest entries matched their declared sizes and SHA-256 digests.
- The package contains 1,075 successful file-comparison records. These are not 1,075 independent experiments, and this count does not imply that every new large output file was submitted for remote inspection.
- A total of 788 attached JSON files were compared again with the original files available in the review workspace. They matched exactly after excluding timing fields only. These comparisons covered job reports, selection artifacts, and available results. Model digests were not excluded as acceptable differences.
- A total of 789 reference digests were checked against original files. In addition, 194 recorded large-output digests were matched against the originals for comparisons reporting byte identity.
- The recorded digests of all 40 selected models were checked against the available original model bytes.
- The difference log contains 688 differences, all classified as timing differences. No scientific differences outside the previously fixed tolerances were reported: `atol=1e-8`, `rtol=1e-10`.
- For 92 comparisons, verification does not include reading the new output bytes in the independent review workspace. These include NPZ arrays and compressed-file contents and rely on the supplied local comparison records. Inspection of the comparison script confirmed checks of rows, keys, shapes, and values using the existing tolerances. Submitted experiment scripts were not executed, and joblib models were not loaded during this review.

The machine-readable review is available at:

- `validation/mac_completed/INDEPENDENT_VERIFICATION.json`
- `validation/mac_completed/verify_continued_return.py`

The categories above overlap and must not be added together.

## Coverage of manuscript and supplementary results

| Result group | Evidence and reproduction route |
|---|---|
| Data preparation, splits, and inputs | The earlier `check-all` run rebuilt the prepared data from raw inputs and matched 22 portable-manifest entries. It was not repeated during continuation. |
| Candidates, eligibility, and selection | Training across 154 jobs and the original selection procedure; new selection reports match the originals. |
| Six primary comparisons, model families and windows, calibration, duplicate sensitivity, and bootstrap analyses | `test` regenerated predictions, scores, and analyses using the original scientific scripts. Comparison reports are included. |
| Ninety strata, MSLE, and size-reference results by stratum | Stage 14 analyses and the earlier `check-all` run; see the `stage_a` evidence. |
| Twelve noise-control contrasts and analyses across noise realizations | `noise` repeated fitting, evaluation, aggregation, and bootstrap analysis; see `stage_b`. |
| Publication figures and manuscript-number bindings | The earlier `check-all` run passed 286 reporting checks and regenerated the figures. Continuation did not recompile LaTeX or regenerate the manuscript's publication figures. |
| Some inherited editorial sample descriptions | Original outputs and reports are preserved and linked. This review does not claim that every editorial description was recomputed from raw events during continuation. |

`audit/RESULT_TO_SOURCE.csv` maps result groups to original outputs, inputs, and scientific scripts. Coverage applies to the **Revision6** manuscript snapshot in `paper/`; it does not certify later external edits that were not supplied for review. This is an experimental reproduction review, not a new audit of bibliographic references, journal requirements, or every PDF page.

## Explicit limitations

1. **One missing original process-exit record.** The job `weibo__qrf__c2__I0__s20260913` has complete results but no original process-exit report. Its outputs were adopted after rechecking 6,000 cases, digests, and metadata. There are 153 training process-exit records, not 154. The missing record was not fabricated.

2. **Evaluation used historical parent archives.** `test` and `noise` used the original archives; newly generated run archives were not passed into the original runners. Model identity establishes the link at the model-file level. It does not turn the execution into an uninterrupted chain that passes newly packaged archives between stages.

3. **New large outputs remained on the Mac.** The independent review checked the submitted evidence and recorded digests against the originals. It did not directly read the new large model and score files from the user's machine.

4. **Environment-specific evidence.** The results support reproduction in the matched environment. They do not guarantee identity on every machine or dependency version. Time limits and numerical variation can affect candidate eligibility elsewhere.

5. **Publication rendering and editorial scope.** The package does not claim to rederive every descriptive sentence or automatically build a newly compiled manuscript PDF. LaTeX sources are available for compilation, including in Overleaf.

## Updated package contents and use

- `reproduce.py`: unchanged controller for coordinating and verifying the original stages. Original scientific sources remain in the original asset archives.
- `README_AR.md`: original Arabic operating instructions, package composition, and historical-parent constraints. `README.md` provides the separately prepared English instructions when added to the repository.
- `VALIDATION_AR.md`: original Arabic review. This file, `VALIDATION.md`, is its English counterpart. Earlier instructions are retained as historical records in `validation/mac_completed/`.
- Original stopped-run and continuation audit packages, including comparison records and coordination logs.
- Independent verification script and result, together with the updated controller content manifest.
- `paper/`: Revision6 LaTeX sources, PDFs, figures, and reporting evidence.

The review did not modify original assets, use the excluded `old` directory, or run additional experiments. The retraining gap documented in the previous controller release is now closed by the completed-run evidence, subject to the explicit limits above.
