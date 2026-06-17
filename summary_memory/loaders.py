from pathlib import Path
from pypdf import PdfReader
from docx import Document
import pandas as pd


def load_file(file_path):

    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return load_pdf(file_path)

    elif suffix == ".txt":
        return load_txt(file_path)

    elif suffix == ".docx":
        return load_docx(file_path)

    elif suffix == ".csv":
        return load_csv(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {suffix}"
        )


def load_pdf(path):

    reader = PdfReader(path)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def load_txt(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def load_docx(path):

    doc = Document(path)

    return "\n".join(
        para.text
        for para in doc.paragraphs
    )


def load_csv(path):

    df = pd.read_csv(path)

    return df.to_string()