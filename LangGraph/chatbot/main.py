from graph import graph

while True:

    user_message = input("\nYou: ")

    if user_message.lower() == "exit":
        break

    result = graph.invoke(
        {
            "message": user_message
        }
    )

    print("\nBot:", result["response"])