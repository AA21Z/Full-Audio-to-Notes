import os
#from openai import OpenAI
import whisper

working_directory = os.getcwd()

model = whisper.load_model("base")
result = model.transcribe(f"{working_directory}/Input Audio/AR_Sample.m4a")

print(result["text"])
#client = OpenAI()

#audio_file = open(f"{working_directory}/Input Audio/AR_Sample.m4a", "rb")
#transcription = client.audio.transcriptions.create(
#  model="whisper-1", 
#  file=audio_file, 
#  response_format="text"
#)
#print(transcription.text)