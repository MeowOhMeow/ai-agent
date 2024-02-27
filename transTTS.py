import sounddevice as sd

import numpy as np
from typing import Any, Tuple

import sys

sys.path.append("VITS")

from VITS.TTS import TTS

version = "v1"
if version == "v1":
    from Translator.Translator_v1 import Translator
elif version == "v2":
    from Translator.Translator_v2 import Translator


class TransTTS:
    def __init__(self) -> None:
        self.translator = Translator()
        self.tts = TTS()
        self.rate = self.tts.rate

    def __call__(self, text: str, **kwargs: Any):
        print(text)
        translated = self.translator(text)
        translated = translated.replace("\n", "。")
        print(translated)
        audio = self.tts(translated, **kwargs)
        return audio


if __name__ == "__main__":
    TransTTS = TransTTS()
    rate = TransTTS.rate
    while True:
        text = input("Text: ")
        audio = TransTTS(text)
        # play
        sd.play(audio, rate)
        sd.wait()
