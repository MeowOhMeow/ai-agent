from api import API

import sounddevice as sd

import torch
import gc

args = {
    "speaker": "kaguya",
    "language": "日本語",
    "speed": 0.7,
    "noise_scale": 0.667,
    "noise_scale_w": 0.6,
}


if __name__ == "__main__":
    api = API()
    rate = api.rate

    while True:
        text = input("Text: ")
        audio = api(text, args)
        # play
        sd.play(audio, rate)
        sd.wait()

        # clear memory
        torch.cuda.empty_cache()
        gc.collect()

