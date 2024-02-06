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
    audio = TransTTS(
        "ひなの想讓一ノ瀬うるは說出福利台詞而撰寫妄想音聲，沒想到暴露後馬上收到完美前輩的配音\nFuwawa問Reine夜這い(夜襲)的印尼話？ 上網查了一下意思之後發現超牙敗的..."
    )
    # play
    sd.play(audio, rate)
    sd.wait()
