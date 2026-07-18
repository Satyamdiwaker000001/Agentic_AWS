# agent.py
"""Simple chat agent integration for the SRS Compliance Analyzer.
Provides a lightweight LLM based chatbot using the locally available model.
"""

import os
from typing import List

try:
    from transformers import pipeline, set_seed
except ImportError:
    pipeline = None  # type: ignore

class ChatAgent:
    def __init__(self, model_name: str = "gpt-oss-120b", max_new_tokens: int = 200, temperature: float = 0.7):
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.generator = None
        if pipeline is not None:
            try:
                self.generator = pipeline(
                    "text-generation",
                    model=self.model_name,
                    device_map="auto",
                    torch_dtype="auto",
                )
                set_seed(42)
            except Exception as e:
                print(f"[ChatAgent] Failed to load model {self.model_name}: {e}")
                self.generator = None
        else:
            print("[ChatAgent] transformers not installed; chat agent will be a placeholder.")

    def generate(self, prompt: str, history: List[dict] = None) -> str:
        if self.generator is None:
            return "(Chat agent unavailable – echo) " + prompt
        if history:
            context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + "\n"
        else:
            context = ""
        full_prompt = context + f"user: {prompt}\nassistant:"
        try:
            outputs = self.generator(
                full_prompt,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id,
            )
            response = outputs[0]["generated_text"][len(full_prompt):].strip().split("\n")[0]
            return response
        except Exception as e:
            return f"(Error: {e})"

def get_agent(model_name: str = "gpt-oss-120b") -> ChatAgent:
    global _cached_agent
    try:
        _cached_agent
    except NameError:
        _cached_agent = None
    if _cached_agent is None:
        _cached_agent = ChatAgent(model_name=model_name)
    return _cached_agent
