# Experiments

Nothing in this directory is part of the supported application.

`sphinx_method.py` preserves an early, non-runnable speech-recognition spike. Its
`cmu_sphinx4` import and `Transcriber` API do not correspond to a maintained
Python package, while Sphinx4 itself is a Java project. The maintained Python
continuation is PocketSphinx.

PocketSphinx custom-vocabulary work is intentionally isolated on the
`codex/pocketsphinx-keyword-experiment` branch. It must demonstrate useful
keyword detection on synthetic audio before it is considered for the primary
application.

## PocketSphinx evaluation result

The isolated evaluation was completed on 2026-08-13 with PocketSphinx 5.1.1,
Python 3.13, and synthetic macOS `say` audio. Using `CODEX` with pronunciation
`K OW D EH K S` and threshold `1e-30`, it detected two of three positive
utterances with timestamps and produced no detection on the negative control.
Vocabulary-prompted Whisper transcribed all three positive utterances. A wider
two-term vocabulary also produced a false `FHIR` detection on the control.

Decision: keep PocketSphinx on the experiment branch. It did not improve on
prompted Whisper in this test, so it is not integrated into Tkinter or the
primary dependency set. Full commands and results remain on the experiment
branch.
