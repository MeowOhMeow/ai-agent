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
        self.request_history = deque(maxlen=message_history_length)
        self.response_history = deque(maxlen=message_history_length)

    def regenerate_response(self):
        self.response_history.pop()
        return self(self.request_history.pop())

    def get_last_response(self):
        return self.response_history[-1]

    def __call__(self, text: str) -> str:
        gpt_prompt = kaguya_prompt  # 塞入一開始的洗腦咒語
        for request, response in zip(self.request_history, self.response_history):
            gpt_prompt += f"'user:{request}, 四宮輝夜:{response}'"
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
        self.request_history.append(text)
        self.response_history.append(response)

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
