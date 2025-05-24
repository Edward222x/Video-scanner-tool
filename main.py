import os
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import subprocess

# Load offensive words from file
def load_offensive_words(filepath="offensive_words.txt"):
    if not os.path.exists(filepath):
        print(f"{filepath} not found.")
        return []
    with open(filepath, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

# Open file dialog to choose a video
def get_video_file():
    root = tk.Tk()
    root.withdraw()
    video_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv *.wmv *.flv")]
    )
    return video_path

# Extract audio
def extract_audio(video_path):
    clip = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    clip.audio.write_audiofile(audio_path)
    return audio_path

# Transcribe audio
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Request error: {e}")
        return ""

# Scan transcript
def scan_transcript(transcript, offensive_words):
    words = transcript.lower().split()
    results = []
    for i, word in enumerate(words):
        if word.strip(".,!?") in offensive_words:
            results.append((i, word))
    return results

# Main function
def main():
    offensive_words = load_offensive_words()
    if not offensive_words:
        print("No offensive words loaded.")
        return
    video_path = get_video_file()
    if not video_path:
        print("No file selected.")
        return
    print("Extracting audio...")
    audio_path = extract_audio(video_path)
    print("Transcribing...")
    transcript = transcribe_audio(audio_path)
    print("Scanning for offensive words...")
    results = scan_transcript(transcript, offensive_words)

    report_path = "report.txt"
    with open(report_path, "w") as report:
        for i, word in results:
            report.write(f"{word} at word index {i}\n")

    print(f"Scan complete. Report saved to {report_path}")
    os.remove(audio_path)

if __name__ == "__main__":
    main()
