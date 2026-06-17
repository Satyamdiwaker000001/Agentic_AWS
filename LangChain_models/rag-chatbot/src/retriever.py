def retrieve_context(
    vectorstore,
    question,
    k=1
):

    results = vectorstore.similarity_search(
        question,
        k=k
    )

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    return context