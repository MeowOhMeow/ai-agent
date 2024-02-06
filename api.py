import sounddevice as sd

import numpy as np

import sys

sys.path.append("VITS")


from GPT.OpenAI_API import OpenAI_API
from VITS.TTS import TTS
from transTTS import TransTTS


class API:
    def __init__(self) -> None:
        self.openai_api = OpenAI_API()
        self.transTTS = TransTTS()
        self.rate = self.transTTS.rate

    def regenerate_response(self, **kwargs):
        response = self.openai_api.regenerate_response()
        audio = self.transTTS(response, **kwargs)
        return response, audio

    def __call__(self, text: str, **kwargs) -> np.ndarray:
        response = self.openai_api(text)
        audio = self.transTTS(response, **kwargs)
        return response, audio


if __name__ == "__main__":
    api = API()
    rate = api.rate
    _, audio = api(
        "今天天氣真好，我們去公園玩吧。"
    )
    # play
    sd.play(audio, rate)
    sd.wait()
