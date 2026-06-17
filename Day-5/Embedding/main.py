from agent import Agent

agent = Agent()

while True:

    print("\n1. Save Memory")
    print("2. Search Memory")
    print("3. Exit")

    choice = input("\nChoice: ")

    if choice == "1":

        text = input(
            "Enter memory: "
        )

        agent.save(text)

        print(
            "Memory Saved"
        )

    elif choice == "2":

        query = input(
            "Ask: "
        )

        result = agent.recall(
            query
        )

        print(
            "\nRelevant Memory:"
        )

        print(result)

    elif choice == "3":

        break