def chunk_text(text, size=500):

    chunks = []

    current = ""

    for line in text.split("\n"):

        current += line + "\n"

        if len(current) > size:
            chunks.append(current)
            current = ""

    if current:
        chunks.append(current)

    return chunks