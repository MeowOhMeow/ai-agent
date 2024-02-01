import tkinter as tk
import sounddevice as sd

from api import API


class TextToSpeechApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Text to Speech App")
        self.geometry("400x500")

        self.api = API()
        self.speakers = self.api.get_speakers()

        self.text_entry = tk.Text(width=40, height=15)
        self.generate_button = tk.Button(
            text="Generate Audio", command=self.generate_audio
        )
        self.audio_button = tk.Button(
            text="Play Audio", command=self.play_audio, state=tk.DISABLED
        )
        self.speaker = tk.StringVar()
        self.speaker.set(self.speakers[0])
        self.speaker_dropdown = tk.OptionMenu(self, self.speaker, *self.speakers)
        self.speed_scale = tk.Scale(
            from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Speed"
        )
        self.speed_scale.set(0.7)
        self.noise_scale_scale = tk.Scale(
            from_=0.0,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            label="Noise Scale",
        )
        self.noise_scale_scale.set(0.65)
        self.noise_scale_w_scale = tk.Scale(
            from_=0.0,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            label="Noise Scale W",
        )
        self.noise_scale_w_scale.set(0.6)

        self.text_entry.pack()
        self.speaker_dropdown.pack()
        self.speed_scale.pack()
        self.noise_scale_scale.pack()
        self.noise_scale_w_scale.pack()
        self.generate_button.pack()
        self.audio_button.pack()

    def get_args(self):
        args = {
            "speaker": self.speaker.get(),
            "speed": self.speed_scale.get(),
            "noise_scale": self.noise_scale_scale.get(),
            "noise_scale_w": self.noise_scale_w_scale.get(),
        }
        return args

    def generate_audio(self):
        self.audio_button.configure(state=tk.DISABLED)
        # Get text from start (line 1, character 0) to end
        text = self.text_entry.get("1.0", tk.END)
        if text:
            text = text.replace("\n", " ")
            self.audio = self.api(text, self.get_args())
            self.audio_button.configure(state=tk.NORMAL)

    def play_audio(self):
        sd.play(self.audio, self.api.rate)


if __name__ == "__main__":
    app = TextToSpeechApp()
    app.mainloop()
