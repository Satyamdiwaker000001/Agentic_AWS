import time
import requests
import fitz # PyMuPDF
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def create_dummy_pdf(filepath: str):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "This is a test document about Agentic AI. The AI system uses embeddings to store memory.")
    page.insert_text((50, 100), "Another important concept is phishing detection, which helps secure networks from malicious attacks.")
    doc.save(filepath)
    doc.close()

def test_health():
    print("Testing /health...")
    resp = requests.get(f"{BASE_URL}/health")
    resp.raise_for_status()
    print("Health OK:", resp.json())

def test_upload(filepath: str):
    print(f"Testing POST /upload with {filepath}...")
    with open(filepath, "rb") as f:
        files = {"file": (filepath, f, "application/pdf")}
        resp = requests.post(f"{BASE_URL}/upload", files=files)
    resp.raise_for_status()
    print("Upload OK:", resp.json())

def test_search(query: str):
    print(f"Testing GET /search for '{query}'...")
    resp = requests.get(f"{BASE_URL}/search", params={"query": query, "n_results": 2})
    resp.raise_for_status()
    results = resp.json().get("results", [])
    print(f"Search found {len(results)} results:")
    for r in results:
        print(f" - [{r['score']:.4f}] {r['text']}")

if __name__ == "__main__":
    pdf_path = "test_document.pdf"
    create_dummy_pdf(pdf_path)
    
    # Give the server a moment if we just started it
    time.sleep(2)
    
    try:
        test_health()
        test_upload(pdf_path)
        test_search("What do you know about phishing detection?")
    finally:
        if Path(pdf_path).exists():
            Path(pdf_path).unlink()
