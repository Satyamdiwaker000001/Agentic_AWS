def build_prompt(
    context,
    question
):

    return f"""
You are a document assistant.

Answer only from the context.

If answer is not available say:

I could not find this information in the uploaded document.

Context:
{context}

Question:
{question}

Answer:
"""