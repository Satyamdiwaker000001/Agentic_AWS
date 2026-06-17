from transformers import pipeline


def get_llm():

    return pipeline(
        "text-generation",
        model="HuggingFaceTB/SmolLM2-360M-Instruct",
        max_new_tokens=100,
        temperature=0.1
    )