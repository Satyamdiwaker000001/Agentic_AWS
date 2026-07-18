from langchain_core.documents import Document


def load_data(errors_file, solutions_file):
    """
    Load errors and solutions from text files.
    Each line in errors.txt corresponds to the same line in solutions.txt.
    """

    with open(errors_file, "r", encoding="utf-8") as f:
        errors = [line.strip() for line in f if line.strip()]

    with open(solutions_file, "r", encoding="utf-8") as f:
        solutions = [line.strip() for line in f if line.strip()]

    if len(errors) != len(solutions):
        raise ValueError(
            "errors.txt and solutions.txt must have the same number of lines."
        )

    documents = []

    for error, solution in zip(errors, solutions):
        doc = Document(
            page_content=error,
            metadata={
                "solution": solution
            }
        )
        documents.append(doc)

    return documents


def print_result(query, retrieved_docs, answer):
    """
    Display the RAG output in a readable format.
    """

    print("\n" + "=" * 60)
    print("ERROR SEARCH RESULT")
    print("=" * 60)

    print(f"\nQuery:\n{query}")

    print("\nMost Similar Errors:\n")

    for i, doc in enumerate(retrieved_docs, start=1):
        print(f"{i}. {doc.page_content}")
        print(f"   Solution: {doc.metadata['solution']}\n")

    print("-" * 60)
    print("AI GENERATED ANSWER\n")
    print(answer)
    print("=" * 60)