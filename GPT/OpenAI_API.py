from openai import OpenAI
from collections import deque
import os

working_dir = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(working_dir, "prompt"), "r", encoding="utf-8") as file:
        kaguya_prompt = file.read()
except:
    raise Exception("Error: prompt file not found. Make sure 'prompt' file exists.")
try:
    with open(os.path.join(working_dir, "openai_key"), "r", encoding="utf-8") as file:
        API_KEY = file.readline().strip()
except FileNotFoundError:
    raise Exception(
        "Error: API key file not found. Make sure 'openai_key' file exists."
    )
if not API_KEY:
    raise Exception(
        "Error: API key is empty. Please fill in your OpenAI API key in 'openai_key' file."
    )


class OpenAI_API:
    def __init__(self, message_history_length: int = 5) -> None:
        self.api_key = API_KEY
        self.client = OpenAI(api_key=self.api_key)
        self.message_history = deque(maxlen=message_history_length)
        self.last_message = ""
        self.last_response = ""

    def regenerate_response(self):
        self.message_history.pop()
        return self(self.last_message)

    def get_last_response(self):
        return self.last_response

    def __call__(self, text: str) -> str:
        self.last_message = text
        gpt_prompt = kaguya_prompt  # 塞入一開始的洗腦咒語
        for element in self.message_history:  # 加入之前的對話紀錄
            gpt_prompt += element + "\n"
        gpt_prompt += "请不要忘记给你的设定，不要作任何评论，接下来我们继续进行对话："

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": gpt_prompt,  # prompt
                },
                {
                    "role": "user",
                    "content": text,  # 輸入的文字
                },
            ],
        )

        response = completion.choices[0].message.content
        self.last_response = response

        self.message_history.append(
            f"'user:{text}, 四宮輝夜:{response}'"
        )  # 將此對話紀錄進message_history的頭(當前的對話紀錄)

        print(f"Number of tokens in the prompt: {completion.usage.prompt_tokens}")
        print(
            f"Number of tokens in the generated completion: {completion.usage.completion_tokens}"
        )
        print(
            f"Total number of tokens used in the request (prompt + completion): {completion.usage.total_tokens}"
        )

        return response


if __name__ == "__main__":
    api = OpenAI_API()
    while True:
        text = input("input: ")
        response = api(text)
        print(f"output: {response}")
