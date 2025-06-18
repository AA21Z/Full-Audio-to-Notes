# Full-Audio-to-Notes
 Goal: Fully convert an audio recording to a summary and store as an editable document. Running completely offline, do not send any unnecessary data out, and store output locally. Allows for personalization to learn words or acronyms outside that of typical conversations.

Important Dependency:
ffmpeg - install on MaxOS as `brew install ffmpeg` (https://brew.sh/)

May use pip install requirements.txt to install the rest of the dependencies.

To run:
1. Activate venv environment -- source env/bin/activate
2. Run app -- python3 main1.py
3.A. Run sample question -- 'No' if you have a specific recording to run.
3.B. Provide full pathname for audio recording, do not include ' or " if not in Pathname
4. 