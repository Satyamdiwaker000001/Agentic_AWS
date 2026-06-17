from rag.parser import extract_text
from rag.embeddings import chunk_text
from rag.vector_store import create_index, search

from llm.interviewer import (
    generate_question,
    evaluate
)

from speech.recorder import record_audio
from speech.stt import transcribe

resume = extract_text(
    "resumes/resume.pdf"
)

chunks = chunk_text(resume)

create_index(chunks)

while True:

    context = search(
        "project experience"
    )

    question = generate_question(
        "\n".join(context)
    )

    print(question)

    # TTS later

    record_audio(
        "audio/answer.wav",
        duration=20
    )

    answer = transcribe(
        "audio/answer.wav"
    )

    print(answer)

    result = evaluate(
        question,
        answer
    )

    print(result)