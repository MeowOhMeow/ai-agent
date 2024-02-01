from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M").to(device)

# Input text
try:
    path = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_lines = open(path, 'r', encoding='utf-8').read().split('\n')
except:
    print("input.txt not found")
    exit()

for input_text in input_lines:
    # Translate
    input_ids = tokenizer.encode(input_text, return_tensors="pt", padding=True).to(device)
    generated_ids = model.generate(input_ids, forced_bos_token_id=tokenizer.lang_code_to_id["jpn_Jpan"])
    translation = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    print(translation)
