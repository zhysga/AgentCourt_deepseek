from openai import OpenAI

class DeepseekLLM:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, instruction: str = "", prompt: str = "") -> str:
        # 你可以根据实际需要调整 messages 结构
        messages = []
        if instruction:
            messages.append({"role": "system", "content": instruction})
        if prompt:
            messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model="deepseek-chat",  # 你实际使用的 deepseek 模型名
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content