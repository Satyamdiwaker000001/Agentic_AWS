# ============================================================
# IMPORTS
# ============================================================

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)

from rag_engine import retrieve_documents


# ============================================================
# CONFIG
# ============================================================

MODEL_NAME = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

_llm = None


# ============================================================
# FEATURE 07 : SMOLLM2 LOADER
# ============================================================

def load_llm():
    """
    Load SmolLM2 model only once.
    """

    global _llm

    if _llm is not None:
        return _llm

    print("[INFO] Loading SmolLM2...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )

    _llm = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.3
    )

    print("[SUCCESS] SmolLM2 Loaded")

    return _llm


# ============================================================
# FEATURE 08 : TRAVEL QUESTION ANSWERING
# ============================================================

def ask_travel_ai(query):
    """
    RAG Question Answering
    """

    llm = load_llm()

    documents = retrieve_documents(
        query=query,
        k=5
    )

    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    prompt = f"""
You are a professional travel assistant.

Use ONLY the provided context.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    result = llm(prompt)

    answer = result[0]["generated_text"]

    return answer


# ============================================================
# FEATURE 09 : SIMILAR TRIP RECOMMENDATION
# ============================================================

def recommend_trip(
    budget,
    duration,
    male_count,
    female_count
):
    """
    Generate recommendation using RAG context.
    """

    query = f"""
Suggest a trip.

Budget: {budget}

Duration: {duration} days

Male Travelers: {male_count}

Female Travelers: {female_count}
"""

    return ask_travel_ai(query)


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\nTesting Travel AI...\n")

    response = ask_travel_ai(
        "Which destination is cheapest?"
    )

    print(response)

    print("\n" + "=" * 60 + "\n")

    recommendation = recommend_trip(
        budget=80000,
        duration=5,
        male_count=2,
        female_count=1
    )

    print(recommendation)