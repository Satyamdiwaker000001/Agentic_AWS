from transformers import Text2TextGenerationPipeline, pipeline

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


VECTOR_DB_PATH = "vector_db"


class ErrorRAG:

    def __init__(self):

        print("Loading Embedding Model...")

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Loading Vector Database...")

        self.vector_db = FAISS.load_local(
            VECTOR_DB_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        print("Loading LLM...")

        self.llm: Text2TextGenerationPipeline = pipeline(
        task="text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=200
    )
        print("Ready!\n")

    def search(self, query, k=3):

        docs = self.vector_db.similarity_search(query, k=k)

        context = ""

        for doc in docs:
            context += (
                f"Error: {doc.page_content}\n"
                f"Solution: {doc.metadata['solution']}\n\n"
            )

        prompt = f"""
You are an expert software debugging assistant.

Below are similar programming errors and their solutions.

{context}

Current Error:
{query}

Give:
1. Most likely cause
2. Best solution
3. Short explanation
"""

        response = self.llm(prompt)[0]["generated_text"]

        return docs, response