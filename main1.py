"""Shared local Whisper workflow and legacy interactive entry point."""

import os
from functools import lru_cache

import torch
import whisper


MODEL_NAME = "medium"
MODEL_DEVICE = "cpu"
OUTPUT_DIRECTORY = "outputs"


@lru_cache(maxsize=1)
def load_whisper_model():
    """Load the fixed Whisper model once for the current process."""
    return whisper.load_model(MODEL_NAME, device=MODEL_DEVICE)


def _vocabulary_prompt(vocabulary):
    """Convert session vocabulary into a compact Whisper prompt."""
    if not vocabulary:
        return None

    terms = vocabulary.splitlines() if isinstance(vocabulary, str) else vocabulary
    cleaned_terms = [term.strip() for term in terms if term and term.strip()]
    return ", ".join(cleaned_terms) or None


def transcribe_audio_whisper(source_file, vocabulary=None):
    """Transcribe one local file, optionally guiding domain vocabulary."""
    model = load_whisper_model()
    transcribe_options = {"verbose": None}
    prompt = _vocabulary_prompt(vocabulary)
    if prompt:
        transcribe_options.update(
            initial_prompt=prompt,
            carry_initial_prompt=True,
        )

    result = model.transcribe(source_file, **transcribe_options)
    return result["text"]


def save_transcript(source_file, output_text, working_directory=None):
    """Save a transcript using the project's existing output convention."""
    base_directory = working_directory or os.getcwd()
    output_dir = os.path.join(base_directory, OUTPUT_DIRECTORY)
    os.makedirs(output_dir, exist_ok=True)

    audio_filename = os.path.basename(source_file)
    transcript_filename = os.path.splitext(audio_filename)[0] + "_transcript.txt"
    transcript_path = os.path.join(output_dir, transcript_filename)
    with open(transcript_path, "w", encoding="utf-8") as file:
        file.write(output_text)
    return transcript_path


def main():
    """Run the original interactive transcription workflow."""
    detected_device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {detected_device}")

    working_directory = os.getcwd()
    audio_loc = os.path.join("Input Audio", "AR_Sample.m4a")
    full_audio_path = os.path.join(working_directory, audio_loc)
    print(full_audio_path)

    run_sample_input = input(
        "Would you like to run the sample file? Yes or No: "
    ).strip().lower()
    if run_sample_input == "no":
        full_audio_path = input("Please provide full audio path/location: ")
        if not os.path.isfile(full_audio_path):
            print("Provided file path is invalid. Please try again.")
            return 1
    else:
        print("Running sample file now.")

    try:
        output_text = transcribe_audio_whisper(full_audio_path)
    except Exception as error:
        print(f"An error occurred during transcription: {error}")
        return 1

    if output_text:
        transcript_path = save_transcript(
            full_audio_path,
            output_text,
            working_directory,
        )
        print(f"Transcript saved to: {transcript_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# Older hosted OpenAI example retained for historical reference. It is not used.
# from openai import OpenAI
# client = OpenAI()
# audio_file = open(f"{os.getcwd()}/Input Audio/AR_Sample.m4a", "rb")
# transcription = client.audio.transcriptions.create(
#     model="whisper-1",
#     file=audio_file,
#     response_format="text",
# )
# print(transcription.text)
