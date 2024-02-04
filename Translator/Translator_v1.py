import translators as ts


class Translator:
    def __init__(self, translator: str = 'bing') -> None:
        self.translator = translator
        # _ = ts.preaccelerate_and_speedtest()

    def __call__(
        self,
        text: str,
        lang_code: str = "ja",
    ) -> str:
        return ts.translate_text(text, to_language=lang_code, translator=self.translator)


if __name__ == "__main__":
    translator = Translator()
    print(translator("這段話應該會被翻譯成日文。"))
    print(translator("這段話應該會被翻譯成英文。", lang_code="en"))
