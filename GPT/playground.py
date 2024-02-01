# WARNING: 這是要錢的，不要亂用

from openai import OpenAI
import os


working_dir = os.path.dirname(os.path.abspath(__file__))
api_key = open(os.path.join(working_dir, "openai_key"), encoding='utf-8').readline().strip()
if api_key == "":
    print("請在 openai_key.txt 中放入你的 OpenAI API Key")
    exit()

# WARNING box
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()
result = messagebox.askokcancel("WARNING", "這是要錢的，不要亂用")
if not result:
    exit()

client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
        },
        {
            "role": "user",
            "content": "Compose a poem that explains the concept of recursion in programming.",
        },
    ],
)

print(completion.choices[0].message)
