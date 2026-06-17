def summarize_text(text, max_chars=1000):

    text = text.replace("\n", " ")

    return text[:max_chars]