import sounddevice as sd

import numpy as np
from typing import Tuple

import sys

sys.path.append("VITS")


from GPT.OpenAI_API import OpenAI_API
from Translator.Translator import Translator
from VITS.TTS import TTS


class API:
    def __init__(self) -> None:
        self.openai_api = OpenAI_API()
        self.translator = Translator()
        self.TTS = TTS()
        self.rate = self.TTS.rate

    def get_speakers(self) -> list:
        return self.TTS.get_speakers()

    def __call__(self, text: str, **kwargs) -> Tuple[str, int, np.ndarray]:
        response = self.openai_api(text)
        print(f"Response: {response}")
        translated = self.translator(response)
        print(f"Translated: {translated}")
        audio = self.TTS(translated, **kwargs)
        return audio


if __name__ == "__main__":
    api = API()
    rate = api.rate
    audio = api("ひなの想讓一ノ瀬うるは說出福利台詞而撰寫妄想音聲，沒想到暴露後馬上收到完美前輩的配音")
    # play
    sd.play(audio, rate)
    sd.wait()
