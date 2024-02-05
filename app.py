import tkinter as tk
import sounddevice as sd
import threading
from api import API

class LeftFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.speed_scale = tk.Scale(
            self,
            from_=0.1,
            to=2,
            resolution=0.1,
            orient=tk.HORIZONTAL,
        )
        self.speed_scale.set(0.7)
        speed_scale_label = tk.Label(text="Speed")
        speed_scale_label.grid(row=0, column=1, columnspan=2)
        self.speed_scale.grid(row=0, column=2)

        self.noise_scale_scale = tk.Scale(
            self,
            from_=0.0,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
        )
        self.noise_scale_scale.set(0.667)
        noise_scale_scale_label = tk.Label(text="Noise Scale")
        noise_scale_scale_label.grid(row=1, column=1, columnspan=2)
        self.noise_scale_scale.grid(row=1, column=2)

        self.noise_scale_w_scale = tk.Scale(
            self,
            from_=0.0,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
        )
        self.noise_scale_w_scale.set(0.6)
        noise_scale_w_scale_label = tk.Label(text="Noise Scale W")
        noise_scale_w_scale_label.grid(row=2, column=1, columnspan=2)
        self.noise_scale_w_scale.grid(row=2, column=2)

        self.text_entry = tk.Entry(self, width=30)
        self.text_entry.grid(row=10, column=0, columnspan=2)
        self.text_entry.bind("<Return>", self.master.generate_audio)

    def get_text(self):
        return self.text_entry.get()

    def clear_text(self):
        self.text_entry.delete(0, tk.END)



class RightFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.text = tk.Text(self, width=30, height=20, state=tk.DISABLED)
        self.text.grid(row=0, column=0)

    def append_text(self, text):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, text + "\n")
        self.text.config(state=tk.DISABLED)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Text to Speech App")
        self.geometry("430x270")

        self.api = API()
        self.rate = self.api.rate

        self.left_frame = LeftFrame(self)
        self.left_frame.grid(row=0, column=1, sticky="nsew")

        self.right_frame = RightFrame(self)
        self.right_frame.grid(row=0, column=0, sticky="nsew")

    def generate_audio(self, event=None):
        t1 = threading.Thread(target = self.moving_text)
        t2 = threading.Thread(target=self.generate_and_play)
        t1.start()
        t2.start()

    def moving_text(self, event=None):
        self.text = self.left_frame.get_text()
        self.left_frame.clear_text()
        self.right_frame.append_text("[You] >> " + self.text + "\n")

    def generate_and_play(self):
        text = self.left_frame.get_text()
        
        kwargs = {
            "speaker": "kaguya",
            "language": "日本語",
            "speed": self.left_frame.speed_scale.get(),
            "noise_scale": self.left_frame.noise_scale_scale.get(),
            "noise_scale_w": self.left_frame.noise_scale_w_scale.get(),
        }
        
        response, audio = self.api(text, **kwargs)
        self.right_frame.append_text("[Kaguya] >> " + response + "\n")
        sd.play(audio, self.rate)
        sd.wait()

if __name__ == "__main__":
    app = App()
    app.mainloop()
