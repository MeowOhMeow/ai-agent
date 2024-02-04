import sounddevice as sd

import numpy as np
from typing import Any, Tuple

import sys

sys.path.append("VITS")

from Translator.Translator import Translator
from VITS.TTS import TTS

class transTTS:
    def __init__(self) -> None:
        self.translator = Translator()
        self.tts = TTS()

    def __call__(self, text: str, **kwargs: Any) -> Tuple[np.ndarray, int]:
        print(text)
        translated = self.translator(text)
        print(translated)
        audio = self.tts(translated, **kwargs)
        return audio, self.tts.rate
    
if __name__ == "__main__":
    transTTS = transTTS()
    audio, rate = transTTS("ひなの想讓一ノ瀬うるは說出福利台詞而撰寫妄想音聲，沒想到暴露後馬上收到完美前輩的配音")
    # play
    sd.play(audio, rate)
    sd.wait()

