from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "models/qwen-0.5b"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype="auto",
    device_map="auto"
)

print("Model Loaded Successfully!")

prompt = "What is React?"

messages = [
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer(
    text,
    return_tensors="pt"
).to(model.device)

print("Generating...")

outputs = model.generate(
    **inputs,
    max_new_tokens=30
)

response = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

print("\nResponse:\n")
print(response)