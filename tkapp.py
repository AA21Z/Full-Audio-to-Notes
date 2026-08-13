"""Primary Tkinter interface for local Whisper transcription."""

import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import main1


class TranscriptionApp:
    """Focused desktop interface for selecting and transcribing one recording."""

    def __init__(self, root):
        self.root = root
        self.is_running = False
        self.worker_messages = queue.Queue()
        self.recording_path = tk.StringVar()
        self.status = tk.StringVar(value="Select a recording to begin.")

        root.title("Full Audio to Notes")
        root.geometry("640x420")
        root.minsize(520, 360)
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        frame = ttk.Frame(root, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(3, weight=1)

        ttk.Label(frame, text="Recording").grid(row=0, column=0, sticky="w")
        path_row = ttk.Frame(frame)
        path_row.grid(row=1, column=0, sticky="ew", pady=(4, 16))
        path_row.columnconfigure(0, weight=1)

        self.path_entry = ttk.Entry(path_row, textvariable=self.recording_path)
        self.path_entry.grid(row=0, column=0, sticky="ew")
        self.browse_button = ttk.Button(
            path_row,
            text="Browse…",
            command=self.browse_for_recording,
        )
        self.browse_button.grid(row=0, column=1, padx=(8, 0))

        ttk.Label(
            frame,
            text="Vocabulary and acronyms (optional, one term or phrase per line)",
        ).grid(row=2, column=0, sticky="w")
        self.vocabulary_text = tk.Text(frame, height=9, wrap="word")
        self.vocabulary_text.grid(row=3, column=0, sticky="nsew", pady=(4, 16))

        self.transcribe_button = ttk.Button(
            frame,
            text="Transcribe",
            command=self.start_transcription,
        )
        self.transcribe_button.grid(row=4, column=0, sticky="w")

        ttk.Separator(frame).grid(row=5, column=0, sticky="ew", pady=14)
        self.status_label = ttk.Label(
            frame,
            textvariable=self.status,
            wraplength=580,
        )
        self.status_label.grid(row=6, column=0, sticky="w")
        root.after(100, self._poll_worker_messages)

    def browse_for_recording(self):
        """Choose a local recording without copying it into the repository."""
        selected_path = filedialog.askopenfilename(
            title="Select a recording",
            filetypes=(
                (
                    "Audio and video",
                    "*.aac *.aif *.aiff *.flac *.m4a *.mp3 *.mp4 *.mov "
                    "*.ogg *.opus *.wav *.webm *.wma",
                ),
                ("All files", "*.*"),
            ),
        )
        if selected_path:
            self.recording_path.set(selected_path)
            self.status.set("Ready to transcribe.")

    def start_transcription(self):
        """Validate the selection and start one background transcription."""
        source_file = self.recording_path.get().strip()
        if not source_file:
            self._show_input_error("Select a recording before transcribing.")
            return
        if not os.path.isfile(source_file):
            self._show_input_error(f"Recording not found: {source_file}")
            return

        vocabulary = self.vocabulary_text.get("1.0", "end").splitlines()
        self._set_running(True)
        self.status.set(f"Loading Whisper {main1.MODEL_NAME} model…")

        worker = threading.Thread(
            target=self._transcribe,
            args=(source_file, vocabulary),
            daemon=True,
        )
        worker.start()

    def _transcribe(self, source_file, vocabulary):
        """Load, transcribe, and save without blocking Tk's event loop."""
        try:
            main1.load_whisper_model()
            self.worker_messages.put(("status", "Transcribing recording locally…"))
            output_text = main1.transcribe_audio_whisper(source_file, vocabulary)
            if not output_text:
                raise RuntimeError("Whisper returned an empty transcript.")
            transcript_path = main1.save_transcript(source_file, output_text)
        except Exception as error:
            self.worker_messages.put(("error", str(error)))
            return

        self.worker_messages.put(("success", transcript_path))

    def _poll_worker_messages(self):
        """Apply worker results from Tk's event-loop thread."""
        while True:
            try:
                message_type, payload = self.worker_messages.get_nowait()
            except queue.Empty:
                break

            if message_type == "status":
                self.status.set(payload)
            elif message_type == "success":
                self._finish_successfully(payload)
            elif message_type == "error":
                self._finish_with_error(payload)
        self.root.after(100, self._poll_worker_messages)

    def _finish_successfully(self, transcript_path):
        self._set_running(False)
        self.status.set(f"Transcript saved to: {transcript_path}")

    def _finish_with_error(self, error_message):
        self._set_running(False)
        self.status.set("Transcription failed.")
        messagebox.showerror(
            "Transcription failed",
            error_message or "An unknown transcription error occurred.",
            parent=self.root,
        )

    def _show_input_error(self, message):
        self.status.set(message)
        messagebox.showerror("Recording required", message, parent=self.root)

    def _set_running(self, running):
        self.is_running = running
        widget_state = "disabled" if running else "normal"
        self.path_entry.configure(state=widget_state)
        self.browse_button.configure(state=widget_state)
        self.vocabulary_text.configure(state=widget_state)
        self.transcribe_button.configure(state=widget_state)

    def on_close(self):
        if self.is_running:
            messagebox.showinfo(
                "Transcription in progress",
                "Wait for transcription to finish before closing the application.",
                parent=self.root,
            )
            return
        self.root.destroy()


def main():
    root = tk.Tk()
    TranscriptionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
