import os

from pypdf import PdfReader

from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

# Load Model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Read JD
with open(
    "jd.txt",
    "r",
    encoding="utf-8"
) as f:

    jd_text = f.read()

jd_embedding = model.encode(
    jd_text
)

results = []

for file in os.listdir("resumes"):

    if not file.endswith(".pdf"):
        continue

    path = os.path.join(
        "resumes",
        file
    )

    reader = PdfReader(path)

    resume_text = ""

    for page in reader.pages:
        resume_text += (
            page.extract_text() or ""
        )

    resume_embedding = model.encode(
        resume_text
    )

    score = cosine_similarity(
        [jd_embedding],
        [resume_embedding]
    )[0][0]

    results.append(
        (
            file,
            round(score * 100, 2)
        )
    )

results.sort(
    key=lambda x: x[1],
    reverse=True
)

print("\nTOP CANDIDATES\n")

for rank, candidate in enumerate(
    results,
    start=1
):

    print(
        rank,
        candidate[0],
        f"{candidate[1]}%"
    )