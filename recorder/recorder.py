import tkinter as tk
from tkinter import messagebox
import threading
import datetime
import cv2
import numpy as np
import pyautogui
import sounddevice as sd
from scipy.io.wavfile import write
from moviepy import VideoFileClip, AudioFileClip
import os

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen & Audio Recorder")

        self.is_recording = False
        self.video_filename = ""
        self.audio_filename = ""
        self.final_output = ""

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording, bg="green", fg="white", width=20)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, bg="red", fg="white", width=20, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Idle", fg="blue")
        self.status_label.pack(pady=5)

    def start_recording(self):
        self.is_recording = True
        self.start_time = datetime.datetime.now()
        self.timestamp = self.start_time.strftime('%Y%m%d_%H%M%S')
        self.video_filename = f"video_{self.timestamp}.avi"
        self.audio_filename = f"audio_{self.timestamp}.wav"
        self.final_output = f"recording_{self.timestamp}.mp4"
        self.audio_frames = []

        self.status_label.config(text="Status: Recording...")

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.video_thread = threading.Thread(target=self.record_video)
        self.audio_thread = threading.Thread(target=self.record_audio)

        self.video_thread.start()
        self.audio_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.video_thread.join()
        sd.stop()
        self.audio_thread.join()

        self.status_label.config(text="Status: Merging...")

        # Save audio
        duration = (datetime.datetime.now() - self.start_time).total_seconds()
        trimmed_audio = self.audio_frames[:int(44100 * duration)]
        write(self.audio_filename, 44100, trimmed_audio)

        # Merge video + audio
        video_clip = VideoFileClip(self.video_filename)
        audio_clip = AudioFileClip(self.audio_filename)
        final_clip = video_clip.with_audio(audio_clip)
        final_clip.write_videofile(self.final_output, codec='libx264', audio_codec='aac')

        # Clean up raw files
        os.remove(self.video_filename)
        os.remove(self.audio_filename)

        self.status_label.config(text=f"✅ Saved: {self.final_output}")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Done", f"Recording saved as {self.final_output}")

    def record_video(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.video_filename, fourcc, 20.0, screen_size)

        while self.is_recording:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame)
            cv2.waitKey(1)

        out.release()

    def record_audio(self):
        self.audio_frames = sd.rec(int(44100 * 3600), samplerate=44100, channels=2, dtype='int16')
        sd.wait()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
