import tkinter as tk
import sounddevice as sd
import threading
from api import API


class ScaleFrame(tk.Frame):
    def __init__(self, master, label, from_, to, resolution, init_val, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        scale_label = tk.Label(self, text=label)
        scale_label.grid(row=0, column=0)

        self.scale = tk.Scale(
            self,
            from_=from_,
            to=to,
            resolution=resolution,
            orient=tk.HORIZONTAL,
        )
        self.scale.set(init_val)
        self.scale.grid(row=0, column=1)

    def get(self):
        return self.scale.get()


class RightFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.speed_scale = ScaleFrame(
            self, label="Speed", from_=0.1, to=2, resolution=0.1, init_val=0.7
        )
        self.speed_scale.grid(row=0, column=0)

        self.noise_scale_scale = ScaleFrame(
            self,
            label="Noise Scale",
            from_=0.0,
            to=1.0,
            resolution=0.05,
            init_val=0.665,
        )
        self.noise_scale_scale.grid(row=1, column=0)

        self.noise_scale_w_scale = ScaleFrame(
            self,
            label="Noise Scale W",
            from_=0.0,
            to=1.0,
            resolution=0.05,
            init_val=0.6,
        )
        self.noise_scale_w_scale.grid(row=2, column=0)

    def get_kwargs(self):
        return {
            "speed": self.speed_scale.get(),
            "noise_scale": self.noise_scale_scale.get(),
            "noise_scale_w": self.noise_scale_w_scale.get(),
        }


class LeftFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.text = tk.Text(self, width=30, height=20, state=tk.DISABLED)
        self.text.grid(row=0, column=0)

        self.text_entry = tk.Entry(self, width=30)
        self.text_entry.grid(row=10, column=0, columnspan=2)
        self.text_entry.bind("<Return>", self.master.generate_audio)

    def append_text(self, text):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, text + "\n")
        self.text.config(state=tk.DISABLED)

    def get_text(self):
        return self.text_entry.get()

    def clear_text(self):
        self.text_entry.delete(0, tk.END)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Text to Speech App")
        self.geometry("430x350")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.api = API()
        self.rate = self.api.rate

        self.left_frame = LeftFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = RightFrame(self)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.task_thread = None

    def generate_audio(self, event=None):
        text = self.left_frame.get_text()
        self.left_frame.clear_text()
        self.left_frame.append_text("[You] >> " + text + "\n")

        self.task_thread = threading.Thread(target=self.generate_and_play, args=(text,))
        self.task_thread.start()

    def generate_and_play(self, text):
        kwargs = self.right_frame.get_kwargs()
        response, audio = self.api(text, **kwargs)
        self.left_frame.append_text("[Kaguya] >> " + response + "\n")
        sd.play(audio, self.rate)
        sd.wait()
        self.task_thread.join()


if __name__ == "__main__":
    app = App()
    app.mainloop()
