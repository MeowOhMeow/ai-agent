
import sounddevice as sd

import os
import torch

from pathlib import Path
import utils
from models import SynthesizerTrn
import torch
from torch import no_grad, LongTensor
import librosa
from text import text_to_sequence, _clean_text
import commons
import scipy.io.wavfile as wavf
import os


from typing import Tuple
import numpy as np

CWD = os.getcwd()
if CWD.endswith("VITS"):
    config_path = os.path.join(CWD, "output_models/finetune_speaker.json")
    checkpoint_path = os.path.join(CWD, "output_models/G_latest.pth")
else:
    config_path = os.path.join(CWD, "VITS/output_models/finetune_speaker.json")
    checkpoint_path = os.path.join(CWD, "VITS/output_models/G_latest.pth")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

language_marks = {
    "Japanese": "",
    "日本語": "[JA]",
    "简体中文": "[ZH]",
    "English": "[EN]",
    "Mix": "",
}


def get_text(text, hps, is_symbol):
    text_norm = text_to_sequence(
        text, hps.symbols, [] if is_symbol else hps.data.text_cleaners
    )
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


class TTS:
    def __init__(
        self, config_path: str = config_path, checkpoint_path: str = checkpoint_path
    ) -> None:
        self.hps = utils.get_hparams_from_file(config_path)
        self.net_g = SynthesizerTrn(
            len(self.hps.symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            n_speakers=self.hps.data.n_speakers,
            **self.hps.model,
        ).to(device)
        _ = self.net_g.eval()
        _ = utils.load_checkpoint(checkpoint_path, self.net_g, None)
        self.speaker_ids = self.hps.speakers
        self.speakers = list(self.hps.speakers.keys())
        self.rate = self.hps.data.sampling_rate

    def get_speakers(self):
        return self.speakers

    def __call__(
        self,
        text: str,
        speaker: str = "kaguya",
        language: str = "日本語",
        speed: float = 0.7,
        noise_scale: float = 0.667,
        noise_scale_w: float = 0.6,
    ) -> Tuple[int, np.ndarray]:
        text = language_marks[language] + text + language_marks[language]

        speaker_id = self.speaker_ids[speaker]
        stn_tst = get_text(text, self.hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
            sid = LongTensor([speaker_id]).to(device)
            audio = (
                self.net_g.infer(
                    x_tst,
                    x_tst_lengths,
                    sid=sid,
                    noise_scale=noise_scale,
                    noise_scale_w=noise_scale_w,
                    length_scale=1.0 / speed,
                )[0][0, 0]
                .data.cpu()
                .float()
                .numpy()
            )
        del stn_tst, x_tst, x_tst_lengths, sid
        return audio


if __name__ == "__main__":
    tts = TTS(
        config_path=config_path,
        checkpoint_path=checkpoint_path,
    )
    rate = tts.rate

    print(f"noise_scale: 0.667, noise_scale_w: 0.6")
    audio = tts("こんにちは、私は日本語を話します。")
    # play
    sd.play(audio, rate)
    sd.wait()
    print(f"noise_scale: 0.333, noise_scale_w: 0.6")
    audio = tts("こんにちは、私は日本語を話します。", noise_scale=0.333, noise_scale_w=0.6)
    # play
    sd.play(audio, rate)
    sd.wait()
    print(f"noise_scale: 1, noise_scale_w: 0.6")
    audio = tts("こんにちは、私は日本語を話します。", noise_scale=1, noise_scale_w=0.6)
    # play
    sd.play(audio, rate)
    sd.wait()
    print(f"noise_scale: 0.667, noise_scale_w: 0.3")
    audio = tts("こんにちは、私は日本語を話します。", noise_scale=0.667, noise_scale_w=0.3)
    # play
    sd.play(audio, rate)
    sd.wait()
    print(f"noise_scale: 0.667, noise_scale_w: 0.9")
    audio = tts("こんにちは、私は日本語を話します。", noise_scale=0.667, noise_scale_w=0.9)
    # play
    sd.play(audio, rate)
    sd.wait()
