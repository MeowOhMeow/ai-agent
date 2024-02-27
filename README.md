# 輝夜姬 Agent 

## 流程
1. 文字或語音輸入
使用者輸入文字或語音。
2. 加入角色催眠 Prompt
將使用者輸入的內容添加角色催眠的提示。
3. 送入 GPT-3 生成
將加入催眠 Prompt 的內容送入 GPT-3 進行生成。
4. 後續處理
    1. 丟入翻譯模型翻譯成日文: 將生成的內容丟入翻譯模型，轉換成日文。
    2. 丟入語音合成模型合成語音: 將生成的內容丟入語音合成模型，合成語音。
5. 輸出
輸出包含中文文字和日文語音的結果。

## 資料處理
1. 去背景噪音  [facebookresearch/demucs](https://github.com/facebookresearch/demucs)
2. 分群 nemo/vad_multilingual_marblenet, nemo/titanet_large, nemo/diar_msdd_telephonic [nemo](https://github.com/NVIDIA/NeMo/tree/main)

## 輸入
1. 文字
2. TODO: 語音
    - [openai/whisper-base](https://huggingface.co/openai/whisper-base)

## 翻譯
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M)
- [translators](https://pypi.org/project/translators/)

## 語音合成
- [Plachtaa/VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning/tree/main)

## 其他參考
- [zixiiu/Digital_Life_Server](https://github.com/zixiiu/Digital_Life_Server)

## 使用方式：
如果單純想玩語音可以用 [Plachtaa/VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning/tree/main) 的release，搭配第三點的模型
1. 請在 VITS 下 build [Plachtaa/VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning/tree/main)，具體請參考 [LOCAL.md](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/LOCAL.md)
2. 在conda env update environment.yml
3. 在 VITS\output_models 放入 finetune_speaker.json, G_latest.pth [載點 - Google drive](https://drive.google.com/drive/folders/1-40Dd3CRDzVGoL5gdRj39oN_uWKdOvp2?usp=sharing)
4. 在 GPT\openai_key 放入openai api key
5. run GUI.py 或 CLI.py

## 限制
- 歷史紀錄長度上限是 hard code 成 5
