from llama_cpp import Llama
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class Chat(BaseModel):
    messages: List[Message] = [
        {"role": "system", "content": "You are a helpful assistant. You do your best to fulfill any user request. " + \
        "If you lack information or tools to fulfill it, you say so. "},
        {"role": "user", "content": ""}
    ]

llm = Llama(
    model_path="/var/models/TheBloke/dolphin-2.5-mixtral-8x7b-GGUF/dolphin-2.5-mixtral-8x7b.Q6_K.gguf",  # Download the model file first
    n_ctx=32768,  # The max sequence length to use - note that longer sequence lengths require much more resources
    n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
    n_gpu_layers=99999         # The number of layers to offload to GPU, if you have GPU acceleration available
)

@app.post("/chat/")
async def create_chat(chat: Chat):
    formatted_messages = "\n".join([f"<|im_start|>{message.role}\n{message.content}<|im_end|>" for message in chat.messages]) \
     + "<|im_start|>assistant\n"
    output = llm(
        formatted_messages,  # Prompt
        max_tokens=16384,  # Generate up to 16384 tokens (note: mixtral base was, I believe, 32k, dolphin fine-tuned 16k)
        stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
        echo=False        # Whether to echo the prompt
    )
    return {"output": output}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
