import requests
from typing import List
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class ChatClient:
    def __init__(self):
        self.system_message = {"role": "system", "content": "You are a helpful assistant. You do your best to fulfill any user request. If you lack information or tools to fulfill it, you say so. "}
        self.messages = [self.system_message]
        self.response = None

    def generate(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        response = requests.post('http://localhost:8000/chat/', json={"messages": self.messages})
        self.response = response.json()
        self.messages.append({"role": "assistant", "content": self.response['output']['choices'][0]['text']})
        return self.response['output']['choices'][0]['text']

    def reset(self):
        self.messages = [self.system_message]
        self.response = None
