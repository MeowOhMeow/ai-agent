import sounddevice as sd

import numpy as np

import sys

sys.path.append("VITS")


from GPT.OpenAI_API import OpenAI_API
from VITS.TTS import TTS
version = "v1"
if version == "v1":
    from Translator.Translator_v1 import Translator
elif version == "v2":
    from Translator.Translator_v2 import Translator


class API:
    def __init__(self) -> None:
        self.openai_api = OpenAI_API()
        self.translator = Translator()
        self.tts = TTS()
        self.rate = self.tts.rate

    def regenerate_response(self, **kwargs):
        response = self.openai_api.regenerate_response()
        translated = self.translator(response)
        audio = self.tts(translated, **kwargs)
        print(f"Response: {response}")
        print(f"Translated: {translated}")
        return response, audio
    
    def regenerate_audio(self, **kwargs):
        response = self.openai_api.get_last_response()
        translated = self.translator(response)
        audio = self.tts(translated, **kwargs)
        return audio

    def __call__(self, text: str, **kwargs) -> np.ndarray:
        response = self.openai_api(text)
        translated = self.translator(response)
        audio = self.tts(translated, **kwargs)
        print(f"Response: {response}")
        print(f"Translated: {translated}")
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
