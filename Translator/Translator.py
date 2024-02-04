# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import torch


# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# class Translator:
#     def __init__(
#         self,
#         model_name: str = "facebook/nllb-200-distilled-600M",
#     ) -> None:
#         self.model_name = model_name
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
#         self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(device)

#     def __call__(
#         self,
#         text: str,
#         lang_code: str = "jpn_Jpan",
#     ) -> str:
#         input_ids = self.tokenizer.encode(text, return_tensors="pt", padding=True).to(
#             device
#         )
#         generated_ids = self.model.generate(
#             input_ids,
#             forced_bos_token_id=self.tokenizer.lang_code_to_id[lang_code],
#         )
#         translation = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
#         return translation

import translators as ts


class Translator:
    def __init__(self) -> None:
        pass
        # _ = ts.preaccelerate_and_speedtest()

    def __call__(
        self,
        text: str,
        lang_code: str = "ja",
    ) -> str:
        return ts.translate_text(text, to_language=lang_code, translator="google")


if __name__ == "__main__":
    translator = Translator()
    print(translator("這段話應該會被翻譯成日文。"))
    print(translator("這段話應該會被翻譯成英文。", lang_code="en"))
