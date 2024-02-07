import tkinter as tk
from tkinter import Scale
import threading
import sounddevice as sd
import soundfile as sf
import os
from api import API
from PIL import Image, ImageTk


class ScaleFrame(tk.Frame):
    def __init__(self, master, label, from_, to, resolution, init_val):
        super().__init__(master)
        self.label = label
        self.scale = Scale(
            self, from_=from_, to=to, resolution=resolution, orient=tk.HORIZONTAL
        )
        self.scale.set(init_val)
        self.label = tk.Label(self, text=label)

        self.label.grid(row=0, column=0)
        self.scale.grid(row=0, column=1)

    def get(self):
        return self.scale.get()


class RightFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.api = API()
        self.rate = self.api.rate

        self.create_widgets()

        self.master.bind("<<Generate>>", self.generate_audio)
        self.task_thread = None
        self.play_thread = None
        self.lock = threading.Lock()

    def create_widgets(self):

        current_pic_directory = os.getcwd()
        output_pic_folder = os.path.join(current_pic_directory, "widgets_picture")
        os.makedirs(output_pic_folder, exist_ok=True)
        img_path = os.path.join(output_pic_folder, "widgets_picture.png")
        print(img_path)
        self.img = ImageTk.PhotoImage(Image.open(img_path))
        # 创建一个 Label 来显示图像，并将图像插入其中
        label_pic = tk.Label(self, image=self.img)
        label_pic.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.speed_scale = ScaleFrame(
            self, label="Speed", from_=0.1, to=2, resolution=0.1, init_val=0.7
        )
        self.speed_scale.grid(row=2, column=0)
        self.noise_scale_scale = ScaleFrame(
            self,
            label="Noise Scale",
            from_=0.0,
            to=1.0,
            resolution=0.05,
            init_val=0.665,
        )
        self.noise_scale_scale.grid(row=3, column=0)

        self.noise_scale_w_scale = ScaleFrame(
            self,
            label="Noise Scale W",
            from_=0.0,
            to=1.0,
            resolution=0.05,
            init_val=0.6,
        )
        self.noise_scale_w_scale.grid(row=4, column=0)

        self.replay_button = tk.Button(self, text="Replay", command=self.play)
        self.replay_button.grid(row=5, column=0)

        self.regenerate_response_button = tk.Button(
            self,
            text="Regenerate_response",
            command=self.regenerate_response_button_click,
        )
        self.regenerate_response_button.grid(row=6, column=0)

        self.regenerate_audio_button = tk.Button(
            self,
            text="Regenerate_audio",
            command=self.regenerate_audio_button_click,
        )
        self.regenerate_audio_button.grid(row=7, column=0)

        self.save_audio_button = tk.Button(
            self, text="Save audio response ", command=self.save_audio_button_click
        )
        self.save_audio_button.grid(row=8, column=0)

    def get_response(self):
        return self.response

    def generate_audio(self, event: tk.Event):
        if self.task_thread and self.task_thread.is_alive():
            return
        text = event.widget.get_text()
        self.task_thread = threading.Thread(
            target=self.generate_response,
            args=(text,),
        )
        self.task_thread.start()

    def generate_response(self, text):
        self.response, self.audio = self.api(text, **self.get_kwargs())
        self.master.event_generate("<<Generated>>")
        self.play()

    def regenerate_response(self):
        self.response, self.audio = self.api.regenerate_response(**self.get_kwargs())
        self.master.event_generate("<<Regenerated>>")
        self.play()

    def regenerate_audio(self):
        self.audio = self.api.regenerate_audio(**self.get_kwargs())
        self.play()

    def play_audio(self):
        sd.play(self.audio, self.rate)
        sd.wait()

    def play(self):
        with self.lock:
            if self.play_thread and self.play_thread.is_alive():
                sd.stop()
                self.play_thread.join()
            self.play_thread = threading.Thread(target=self.play_audio)
            self.play_thread.start()

    def regenerate_audio_button_click(self):
        if self.task_thread and self.task_thread.is_alive():
            return
        self.task_thread = threading.Thread(target=self.regenerate_audio())
        self.task_thread.start()

    def regenerate_response_button_click(self):
        if self.task_thread and self.task_thread.is_alive():
            return
        self.task_thread = threading.Thread(target=self.regenerate_response)
        self.task_thread.start()

    def save_audio_button_click(self):
        try:
            current_directory = os.getcwd()
            output_folder = os.path.join(current_directory, "output_audio_response")
            os.makedirs(output_folder, exist_ok=True)
            wav_path = os.path.join(output_folder, "audio_response.wav")
            sf.write(wav_path, self.audio, self.rate)
            print(f"Audio saved successfully to {wav_path}")
        except Exception as e:
            print(f"Error saving audio: {e}")

    def get_kwargs(self):
        return {
            "speed": self.speed_scale.get(),
            "noise_scale": self.noise_scale_scale.get(),
            "noise_scale_w": self.noise_scale_w_scale.get(),
        }


class LeftFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Text(
            self,
            width=55,
            height=20,
            state=tk.DISABLED,
            font=("Microsoft JhengHei", 12),
            fg=self.master.font_color,
            bg=self.master.input_background_color,
        )
        self.text.grid(row=0, column=0)

        self.text_entry = tk.Entry(
            self,
            width=55,
            font=("Microsoft JhengHei", 12),
            fg=self.master.font_color,
            bg=self.master.input_background_color,
        )
        self.text_entry.grid(row=1, column=0, columnspan=2, pady=2)
        self.text_entry.bind("<Return>", self.on_enter)
        self.master.bind("<<Generated>>", self.on_generated)
        self.master.bind("<<Regenerated>>", self.on_regenerated)

    def on_enter(self, event: tk.Event):
        self.master.event_generate("<<Generate>>")

    def on_generated(self, event: tk.Event):
        self.append_text("[Kaguya] >> " + event.widget.get_response() + "\n")

    def on_regenerated(self, event: tk.Event):
        self.text.delete("end-2l", tk.END)
        self.append_text("[Kaguya] >> " + event.widget.get_response() + "\n")

    def get_text(self):
        text = self.text_entry.get()
        self.text_entry.delete(0, tk.END)
        self.append_text("[You] >> " + text + "\n")
        return text

    def append_text(self, text):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, text + "\n")
        self.text.config(state=tk.DISABLED)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Voice Assistant Kaguya-sama")
        self.geometry("710x430")
        self.main_color = "#DDDDDD"  # 444444
        self.background_color = self.main_color  # 444444
        self.input_background_color = self.main_color  # 444444
        self.output_background_color = self.main_color  # 444444
        self.font_color = "#000000"  # FFFFFF

        self.configure(
            bg=self.background_color
        )  # Set background color of the whole application

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left_frame = LeftFrame(self)
        self.left_frame.configure(
            bg=self.background_color
        )  # Set background color of the left frame
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = RightFrame(self)
        self.right_frame.configure(
            bg=self.background_color
        )  # Set background color of the right frame
        self.right_frame.grid(row=0, column=1, sticky="nsew")

    def get_text(self):
        return self.left_frame.get_text()

    def get_response(self):
        return self.right_frame.get_response()


if __name__ == "__main__":
    app = App()
    app.mainloop()
