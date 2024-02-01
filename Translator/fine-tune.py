from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Trainer,
    TrainingArguments,
)

from torch.utils.data import Dataset
import torch

import pandas as pd
import csv


class FineTuneDataset(Dataset):
    def __init__(self, tokenizer, path=None):
        self.tokenizer = tokenizer
        self.lang = tokenizer.lang_code_to_id["jpn_Jpan"]
        if path is not None:
            self.dataframe = pd.read_csv(
                path, quoting=csv.QUOTE_NONNUMERIC, encoding="utf-8", header=None
            )
        else:
            self.dataframe = pd.DataFrame(columns=["text", "translation"])
            # add data to dataframe
            self.dataframe.loc[0] = ["I am a student.", "Je suis étudiant."]

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        text = self.dataframe.iloc[idx, 0]
        translation = self.dataframe.iloc[idx, 1]

        # tokenize the input and target texts
        input_ids = self.tokenizer.encode(text, return_tensors="pt", padding=True)
        labels = self.tokenizer.encode(translation, return_tensors="pt", padding=True)

        # labels = eos + lang + labels
        labels = torch.cat(
            (
                torch.tensor([[self.tokenizer.eos_token_id]]),
                torch.tensor([[self.lang]]),
                labels,
            ),
            dim=1,
        )

        return {"input_ids": input_ids, "labels": labels}


model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)

train_dataset = FineTuneDataset(tokenizer, path="Translator/dataset/train/train.csv")
val_dataset = FineTuneDataset(tokenizer, path="Translator/dataset/val/val.csv")

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=1,
    save_steps=10,
    evaluation_strategy="steps",
    eval_steps=10,
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()

# save the fine-tuned model
# trainer.save_model("Translate/fine-tuned-model")

# testing
print("Testing")
test_dataframe = pd.read_csv(
    "Translator/dataset/test/test.csv",
    quoting=csv.QUOTE_NONNUMERIC,
    encoding="utf-8",
    header=None,
)
for idx in range(len(test_dataframe)):
    text = test_dataframe.iloc[idx, 0]
    translation = test_dataframe.iloc[idx, 1]

    # tokenize the input and target texts
    input_ids = tokenizer.encode(text, return_tensors="pt", padding=True).to(device)
    generated_ids = model.generate(
        input_ids, forced_bos_token_id=tokenizer.lang_code_to_id["jpn_Jpan"]
    )
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    print(f"Input text: {text}")
    print(f"Target text: {translation}")
    print(f"Generated text: {generated_text}")
    print()
