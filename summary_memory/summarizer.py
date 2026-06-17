def summarize_document(text):

    summaries = []

    chunks = chunk_text(text)

    for chunk in chunks:

        if not chunk.strip():
            continue

        result = summarizer(
            chunk,
            max_length=MAX_SUMMARY_LENGTH,
            min_length=MIN_SUMMARY_LENGTH,
            do_sample=False
        )

        summaries.append(
            result[0]["summary_text"]
        )

    return "\n\n".join(summaries)