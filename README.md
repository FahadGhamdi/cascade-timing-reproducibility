# Cascade Timing: Reproducibility Materials

Reproduction materials for **“What Does Timing Add to Size? Probabilistic Forecasts of Recorded Cascade Growth on Two Archives.”**

**Author:** Fahad AlGhamdi, Department of Computer Science, Faculty of Computing and Information, Al-Baha University, Saudi Arabia.  
**ORCID:** https://orcid.org/0000-0002-4161-2658

This package provides a controller for restoring and running the original experimental code, checking archived inputs and outputs, and reproducing the analyses and figures associated with the included manuscript snapshot.

## Verification status

The documented Mac reproduction completed training and selection across **154 jobs**, followed by **40 test jobs** and **42 noise-control jobs**. Training was completed across two sessions: 87 previously completed outputs were verified and adopted, and 67 remaining jobs were executed.

| Stage | Documented result |
|---|---|
| Training and selection | 154 job reports; 133 eligible and 21 preserved as ineligible |
| Validation scoring | 924,000 attempts; 923,926 successes and 74 numerical failures, matching the original run |
| Selection artifacts | Candidate table, selection report, model lock, and validation contrasts identical to the originals at the byte level |
| Selected models | Locally recorded SHA-256 digests of all 40 selected models matched the original model files |
| Test evaluation | 600,000 successful scores; no scoring failures |
| Noise controls | 630,000 successful scores; no scoring failures |

The return package records 1,075 successful file comparisons. Independent inspection verified 2,021 manifest entries and compared 788 attached JSON files with the originals, finding exact agreement after excluding timing fields. New large model and score files remained on the Mac; their recorded digests and local comparison reports were supplied as evidence. Those new large files were not independently read in the remote audit.

One adopted training job has complete verified outputs but no original process-exit report. This absence remains documented; no exit record was reconstructed. See `VALIDATION_AR.md` and the evidence in `validation/mac_completed/` for details. The detailed narrative reports are in Arabic; machine-readable evidence is also included.

## Package components

The complete distributed package consists of the controller and these three original archives:

- `ORIGINALS_PAYLOAD_01.zip`
- `ORIGINALS_PAYLOAD_02.zip`
- `ORIGINALS_PAYLOAD_03.zip`

The controller alone does **not** contain the large experimental datasets and models. The three archives must be obtained separately and placed together in an assets directory. Use complete ZIP archives rather than split parts.

Keep `DISTRIBUTION_INDEX.json` beside `reproduce.py`; it identifies the expected original assets. The `paper/` directory contains the IEEE Access **Revision6** manuscript snapshot included in this package. It does not represent subsequent external manuscript edits.

## Requirements

Training, test evaluation, and noise-control experiments require **Python 3.12** and the exact dependency versions in:

```text
environment/requirements.lock.txt
```

The documented Mac environment used Python 3.12.14 and passed all 33 locked-package checks. The controller does not install dependencies automatically. Analysis and figure generation require the relevant scientific Python packages, including NumPy, SciPy, and Matplotlib.

Use the Python interpreter from the matching experimental environment for the commands below. Do not weaken the environment checks to force execution with different versions.

## Restore the original assets

Run commands from the directory containing `reproduce.py`.

The following shell variables are examples: replace each `/absolute/path/to/...` value with an actual absolute path on your machine. The restored workspace and output directories must be outside the controller directory. Use a fresh workspace and fresh output directories for a new reproduction attempt.

```bash
BRACE_ASSETS="/absolute/path/to/original-archives"
BRACE_WORK="/absolute/path/to/restored-originals"
BRACE_RUNS="/absolute/path/to/new-reproduction-outputs"

python reproduce.py restore --assets "$BRACE_ASSETS" --work "$BRACE_WORK"
python reproduce.py environment --work "$BRACE_WORK"
```

`restore` verifies the original archives and restores their contents. The scientific scripts, data, and models retain their original bytes. The excluded legacy `old` directory is not used.

## Recompute analyses from archived scores

```bash
python reproduce.py check-all --work "$BRACE_WORK" --out "$BRACE_RUNS/check-all"
```

This command:

- Rebuilds the prepared data from the raw inputs and compares the results with the archived reference.
- Recomputes primary analyses and bootstrap results from saved scores.
- Recomputes stratum and noise-control analyses from saved scores.
- Checks the manuscript evidence and regenerates publication figures.

`check-all` does **not** retrain models or regenerate predictive-distribution scores from new model predictions. It does not compile LaTeX into PDF. The included manuscript sources can be compiled separately, including in Overleaf.

The prior verified `check-all` run passed 286 manuscript-reporting checks and regenerated the publication figures. It was not repeated during the subsequent training continuation.

## Re-run the original experimental stages

```bash
python reproduce.py train --work "$BRACE_WORK" --out "$BRACE_RUNS/train"
python reproduce.py test --work "$BRACE_WORK" --out "$BRACE_RUNS/test"
python reproduce.py noise --work "$BRACE_WORK" --out "$BRACE_RUNS/noise"
```

| Command | Scope |
|---|---|
| `train` | Runs original training and selection, including candidates that become ineligible. Records whether the new model-lock file is byte-identical to the reference. |
| `test` | Runs original prediction and evaluation using the approved historical training archive, then compares evaluation summaries with the reference. |
| `noise` | Runs the original supplementary stage, including noise-control fitting, using the approved historical test archive; compares results and bootstrap outputs. |

The internal archive identifiers are **13E** for training and selection, **13F** for test evaluation, and **14** for supplementary and noise-control analyses.

Successful process completion alone is not evidence of numerical reproduction. Inspect the output reports and comparisons before interpreting a new run as a match.

## Historical-parent constraints and model identity

The original test runner requires the exact SHA-256 digest of the historical training archive. The supplementary runner likewise requires the historical test archive. Consequently, the controller does **not** pass a newly generated training archive into `test`, or a newly generated test archive into `noise`.

The verified Mac reproduction preserved these constraints. It established an identity bridge by verifying that the 40 newly selected model files had the same SHA-256 digests as the original models used in evaluation. This supports model-file equivalence, while retaining an accurate account of the archives actually supplied to the runners.

Do not replace expected historical digests or remove execution locks to bypass these constraints. Repackaging a scientifically equivalent run can produce a different archive digest because logs, timestamps, and other metadata differ.

## Numerical comparisons and output handling

Aggregate numerical comparisons use the previously declared tolerances:

```text
atol = 1e-8
rtol = 1e-10
```

Archive hashes and original-file provenance require exact matches. Tolerances are not adjusted after observing a reproduction result. Time-limited candidate eligibility can differ across machines; numerical failures and ineligible candidates must remain in the record.

`reproduce.py` is a new coordination and verification script. During the original primary-analysis call, it uses a gzip output adapter that flushes the text writer every 128 writes to address an incomplete compressed-output issue observed during validation. This changes output handling, not the scientific calculations. Full decompressed output is compared with the reference, and the original scientific source files remain unchanged.

Verification and saved-score analysis paths do not deserialize model objects. Experimental evaluation uses the verified original models under the required dependency environment.

## Outputs and evidence

Stage runs produce reports and logs, including `RUN_REPORT.json` for controller execution. Existing outputs and failed attempts are preserved. Use a new output location for an intentional new run; do not delete locks to trigger automatic retries.

| Location | Contents |
|---|---|
| `README_AR.md` | Arabic operating instructions |
| `VALIDATION_AR.md` | Detailed reproduction review and its limitations |
| `audit/RESULT_TO_SOURCE.csv` | Mapping from result groups to original inputs, outputs, and scientific code |
| `validation/mac_completed/` | Stopped-run and continuation evidence packages, independent verification script, and audit result |
| `environment/requirements.lock.txt` | Original dependency versions |
| `paper/` | Included manuscript snapshot, LaTeX sources, figures, and reporting materials |

Earlier collection reports and pre-completion instructions are retained as historical evidence. Their status statements should be interpreted according to their date and scope; the completed-run review is in `VALIDATION_AR.md`.

## Scope of the reproduction claim

The evidence supports reproduction of the documented experimental stages and analyses in the matched environment. It does not guarantee identical behavior on every platform or with different dependency versions.

The continuation did not recompile the manuscript PDF or independently recompute every inherited editorial sample description from raw events. The included manuscript snapshot and its reporting checks define the publication-material scope of this package.

Data and third-party components retain their applicable terms. This README does not grant permission to redistribute third-party datasets or relicense third-party code.
