"""Historical, non-runnable CMU Sphinx experiment.

See README.md in this directory before attempting to continue this work.
"""

import cmu_sphinx4

# Read in audio file into Sphinx.
# audio_url =
transcriber = cmu_sphinx4.Transcriber(audio_URL)

# Print out text.
for line in transcriber.transcript_stream():
    print(line)
