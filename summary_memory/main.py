from Agentic.summary_memory.loaders import load_file
from Agentic.summary_memory.summarizer import summarize_document
from Agentic.summary_memory.memory import SummaryMemory


memory = SummaryMemory()

file_path = "documents/cpp.pdf"

print("Loading file...")

document_text = load_file(
    file_path
)

print(
    f"Characters loaded: "
    f"{len(document_text)}"
)

print("Generating summary...")

summary = summarize_document(
    document_text
)

memory.save(summary)

print(
    "Summary saved "
    "to summary_memory.txt"
)