import os
#from openai import OpenAI
import whisper

# Init full path instances TODO: AA to improve so only name of file is needed.
# Get the current working directory
working_directory = os.getcwd()

# Initialize the relative path to the sample audio file
audio_loc = os.path.join("Input Audio", "AR_Sample.m4a")
full_audio_path = os.path.join(working_directory, audio_loc)
print(full_audio_path)

# Prompt the user to decide whether to run the sample file or their own file
run_sample_input = input("Would you like to run the sample file? Yes or No: ").strip().lower()

# Determine the file path based on user input
if run_sample_input == "no":
  full_audio_path = input("Please provide full audio path/location: ")
  if not os.path.isfile(full_audio_path):  # Check if the provided path is valid
        print("Provided file path is invalid. Please try again.")
        exit(1)
else:
  # if statement does not take into account any other inputs #TODO: AA Revist logic.
  print("Running sample file now.")

def transcribe_audio_whisper(source_file): 
  try:
      model = whisper.load_model("small")
      result = model.transcribe(source_file)
      return result["text"]
  except Exception as e:
      print(f"An error occurred during transcription: {e}")
      return None

output_text = transcribe_audio_whisper(full_audio_path)

print("Your output Transcript: \n", "\"",output_text, "\"")

# -- Older OpenAI code [Requires API key] -- 
#client = OpenAI()

#audio_file = open(f"{working_directory}/Input Audio/AR_Sample.m4a", "rb")
#transcription = client.audio.transcriptions.create(
#  model="whisper-1", 
#  file=audio_file, 
#  response_format="text"
#)
#print(transcription.text)