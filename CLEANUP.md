# Repository Cleanup Tracker

This is the living checklist for repository maintenance. Update it in the same
change that completes an item so the tracker remains useful over time.

## Project guardrails

- Audio and transcription must remain local; do not add a cloud fallback.
- Never commit real recordings, transcripts, health information, logs, or
  credentials. Any committed test fixture must be synthetic and non-sensitive.
- Keep generated transcripts and other private runtime data in ignored paths.
- Perform cleanup work on `Improvements-for-main` and merge it only after the
  relevant checks below pass.

## Completed

### 1. Protect sensitive local data

- [x] Ignore common audio and video recording formats.
- [x] Ignore generated transcripts, subtitles, and output directories.
- [x] Ignore local health/private-data directories, logs, and databases.
- [x] Ignore environment files and common credential/key formats while allowing
  safe environment templates.
- [x] Verify representative sensitive paths with `git check-ignore`.

## Remaining work

### 2. Consolidate the supported application

Goal: leave one clear, maintainable way to run the project.

- [x] Review `main1.py`, `sphinx_method.py`, and `tkapp.py` and identify which
  behavior is still wanted.
- [x] Select and document one supported entry point.
- [x] Preserve the historical Sphinx spike under `experiments/` and label it as
  unsupported.
- [x] Verify the Tkinter application with synthetic audio while confirming the
  event loop remains responsive and generated data stays untracked.
- [ ] Record the separate PocketSphinx keyword experiment and its decision-gate
  result.
- [x] Confirm the branch contains only changes intended to reach `main`.

Done when a new contributor can identify the supported application without
having to inspect every Python file and the PocketSphinx evaluation is recorded.

### 3. Replace the hard-coded script with a proper CLI

Goal: transcribe a user-selected file safely without editing source code.

- [ ] Accept an input path, output directory, and Whisper model as command-line
  options.
- [ ] Remove the hard-coded sample recording path.
- [ ] Put executable behavior behind a `main()` function and `if __name__ ==
  "__main__":` guard.
- [ ] Validate the input file and required tools, including `ffmpeg`, before
  loading the Whisper model.
- [ ] Return clear error messages and non-zero exit codes on failure.
- [ ] Save generated text under an ignored output directory; do not expose a
  transcript unexpectedly in console output or logs.

Done when the supported workflow can process a synthetic recording from an
arbitrary path and fails cleanly for invalid input.

### 4. Make installation reproducible

Goal: make setup predictable on a clean machine.

- [ ] Declare the supported Python version.
- [ ] Remove unused dependencies and add any imports that are actually required.
- [ ] Choose and document a dependency strategy (`pyproject.toml` preferred, or
  a corrected and version-constrained `requirements.txt`).
- [ ] Correct the README installation command to `pip install -r
  requirements.txt` if the requirements file remains.
- [ ] Document `ffmpeg` installation and verify setup in a fresh virtual
  environment.

Done when a clean environment can install and launch the supported entry point
using only the documented steps.

### 5. Add automated quality and safety checks

Goal: catch regressions without using private or real-world recordings.

- [ ] Add unit tests with mocked transcription and synthetic metadata only.
- [ ] Cover input validation, output naming, missing dependencies, and
  transcription failures.
- [ ] Add formatting and linting configuration with one documented check command.
- [ ] Add CI for tests and static checks.
- [ ] Add content-based secret detection to CI or pre-commit checks; `.gitignore`
  alone cannot detect a secret embedded in a tracked source file.
- [ ] Confirm automated checks never upload or retain user audio or transcripts.

Done when the documented check command passes locally and the same checks run on
each proposed change.

## Final merge checklist

- [ ] README describes the supported workflow accurately.
- [ ] Tests and static checks pass.
- [ ] A synthetic-audio smoke test succeeds locally.
- [ ] No sensitive or generated files are tracked.
- [ ] `Improvements-for-main` is reviewed and ready to merge into `main`.
