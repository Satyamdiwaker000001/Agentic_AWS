from graph import graph

print("ChatBot Started")
print("Type 'exit' to quit\n")

while True:

    query = input("You: ")

    if query.lower() == "exit":
        break

    result = graph.invoke(
        {
            "message": query
        }
    )

    print("\nBot:")
    print(result["response"])
    print()