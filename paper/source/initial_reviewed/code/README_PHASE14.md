# Phase 14 review code

`review_saved_phase14.py` verifies a return ZIP, its extracted source/run payloads, saved score rows, aggregates and saved bootstrap quantiles. It imports only standard-library modules and NumPy. It never loads model objects or executes a model/prediction/scoring/resampling pipeline. The optional fourth path checks exact identity with the original supplementary kit.

Usage: `python review_saved_phase14.py RETURN.zip EXTRACTED_INPUT REVIEW_OUTPUT_DIR ORIGINAL_KIT.zip`

The full return archive is required; this compact editorial package intentionally does not duplicate models and all score streams. `figures14_original.py` is the unchanged figure script from the supplied source kit, retained as provenance and requiring that kit's utilities. It was not executed during this review. Original Phase 13F code and evidence remain under their original names.
