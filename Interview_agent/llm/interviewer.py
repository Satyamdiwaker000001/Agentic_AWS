from llama_cpp import Llama

llm = Llama(
    model_path="models/qwen.gguf",
    n_ctx=4096,
    verbose=False
)


def generate_question(context):

    prompt = f"""
You are a technical interviewer.

Resume Context:
{context}

Ask exactly one interview question.

Return only the question.
"""

    response = llm(
        prompt,
        max_tokens=100
    )

    return response["choices"][0]["text"].strip()


def evaluate(question, answer):

    prompt = f"""
Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Give:
Score: X/10

Feedback:
2-3 lines
"""

    response = llm(
        prompt,
        max_tokens=200
    )

    return response["choices"][0]["text"].strip()