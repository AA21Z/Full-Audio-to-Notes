# Full-Audio-to-Notes

Goal: Fully convert an audio recording to a summary and store as an editable
document. Run completely offline, do not send unnecessary data elsewhere, and
store output locally. Allow personalization for words or acronyms outside
typical conversations.

## Supported application

The Tkinter desktop application is the sole supported entry point:

```sh
python3 tkapp.py
```

Select a local recording, optionally enter vocabulary or acronyms one per line,
and select **Transcribe**. Vocabulary is used only to guide that transcription
and is not saved. The application uses the fixed Whisper `medium` model on the
CPU and saves text under `outputs/` without displaying the transcript.

`main1.py` contains the shared Whisper implementation. Its original interactive
workflow remains available as a legacy script until the command-line work in
`CLEANUP.md` item 3.

Files under `experiments/` are unsupported research spikes and are not used by
the application.

## Current setup

Important dependency: install `ffmpeg` on macOS with
`brew install ffmpeg` (<https://brew.sh/>).

May use `pip install requirements.txt` to install the rest of the dependencies.
