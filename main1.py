import os
#from openai import OpenAI
import whisper
import torch

# Check if GPU acceleration via Metal is available
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

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
      model = whisper.load_model("medium", device="cpu")  # Use CPU explicitly
      result = model.transcribe(source_file)
      return result["text"]
  except Exception as e:
      print(f"An error occurred during transcription: {e}")
      return None

output_text = transcribe_audio_whisper(full_audio_path)

#print("Your output Transcript: \n", "\"",output_text, "\"")

if output_text:
  # Define the output directory and ensure it exists
  output_dir = os.path.join(working_directory, "outputs")
  os.makedirs(output_dir, exist_ok=True) 
  # Generate a filename based on the audio file name
  audio_filename = os.path.basename(full_audio_path)
  transcript_filename = os.path.splitext(audio_filename)[0] + "_transcript.txt"
  transcript_path = os.path.join(output_dir, transcript_filename)  
  # Write the transcript to a .txt file
  with open(transcript_path, "w", encoding="utf-8") as file:
    file.write(output_text)  
  print(f"Transcript saved to: {transcript_path}")

# -- Older OpenAI code [Requires API key] -- 
#client = OpenAI()

#audio_file = open(f"{working_directory}/Input Audio/AR_Sample.m4a", "rb")
#transcription = client.audio.transcriptions.create(
#  model="whisper-1", 
#  file=audio_file, 
#  response_format="text"
#)
#print(transcription.text)