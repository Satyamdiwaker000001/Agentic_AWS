from Agentic.pdf_summary.pdf_reader import extract_pdf_text
from Agentic.pdf_summary.memory import SummaryMemory

memory = SummaryMemory()

pdf_path = "pdfs/cpp.pdf"

print("Reading PDF...")

pdf_text = extract_pdf_text(pdf_path)

memory.save(pdf_text)

print("Complete PDF saved into summary_memory.txt")