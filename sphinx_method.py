import cmu_sphinx4

#Read in audio file into sphinx
#audio_url = 
transcriber = cmu_sphinx4.Transcriber(audio_URL)

# Print out text
for line in transcriber.transcript_stream():
    print (line)