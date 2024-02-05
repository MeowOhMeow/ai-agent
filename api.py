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
        self.TTS = TTS()
        self.rate = self.TTS.rate

    def get_speakers(self) -> list:
        return self.TTS.get_speakers()

    def __call__(self, text: str, **kwargs) -> np.ndarray:
        response = self.openai_api(text)
        print(f"Response: {response}")
        translated = self.translator(response)
        print(f"Translated: {translated}")
        audio = self.TTS(translated, **kwargs)
        return response, audio


if __name__ == "__main__":
    api = API()
    rate = api.rate
    _, audio = api(
        "ひなの想讓一ノ瀬うるは說出福利台詞而撰寫妄想音聲，沒想到暴露後馬上收到完美前輩的配音"
    )
    # play
    sd.play(audio, rate)
    sd.wait()
