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
