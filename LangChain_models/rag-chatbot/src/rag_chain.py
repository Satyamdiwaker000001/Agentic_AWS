from src.retriever import (
    retrieve_context
)

from src.prompt_builder import (
    build_prompt
)


def ask_rag(
    question,
    vectorstore,
    llm
):

    context = retrieve_context(
        vectorstore,
        question
    )

    prompt = build_prompt(
        context,
        question
    )

    response = llm(prompt)

    generated = response[0][
        "generated_text"
    ]

    if "Answer:" in generated:

        generated = generated.split(
            "Answer:"
        )[-1]

    generated = generated.strip()

    if not generated:

        return (
            "I could not find this "
            "information in the document."
        )

    return generated