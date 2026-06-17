from pypdf import PdfReader


def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)

    all_text = []

    for page_num, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            all_text.append(
                f"\n\n===== PAGE {page_num} =====\n"
            )
            all_text.append(text)

    return "\n".join(all_text)