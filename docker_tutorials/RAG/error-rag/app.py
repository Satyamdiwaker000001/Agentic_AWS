from rag import ErrorRAG
from utils import print_result


def main():
    print("=" * 60)
    print("      ERROR SOLUTION FINDER (RAG)")
    print("=" * 60)

    rag = ErrorRAG()

    while True:
        query = input("\nEnter an error (or type 'exit'): ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        docs, answer = rag.search(query)

        print_result(query, docs, answer)


if __name__ == "__main__":
    main()