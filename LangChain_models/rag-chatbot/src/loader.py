from pathlib import Path
from pypdf import PdfReader
import docx2txt


def load_document(file_path):

    file_path = Path(file_path)

    if file_path.suffix.lower() == ".pdf":

        text = ""

        reader = PdfReader(str(file_path))

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif file_path.suffix.lower() == ".docx":

        return docx2txt.process(str(file_path))

    elif file_path.suffix.lower() == ".txt":

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    raise ValueError("Unsupported file")