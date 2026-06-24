import torch
from models.qwen_model import model, tokenizer


def generate_response(prompt, max_tokens=1500):
    """
    Generate a response using the preloaded Qwen model.
    Optimized for maximum CPU speed:
    - torch.inference_mode (faster than no_grad)
    - Greedy decoding (no sampling overhead)
    - Reduced token count (50 tokens = ~5s on CPU)
    """

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    # inference_mode is stricter and faster than no_grad
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=False,                       # greedy = fastest
            repetition_penalty=1.1,                # avoid loops
            pad_token_id=tokenizer.eos_token_id,   # suppress warnings
            use_cache=True,                        # KV cache for faster autoregressive
        )

    input_length = inputs.input_ids.shape[1]
    generated_tokens = outputs[0][input_length:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return response