from Agentic.window_memory.memory import WindowMemory

memory = WindowMemory()

print("WINDOW MEMORY BOT")

while True:

    user = input("\nYou: ")

    if user.lower() == "exit":
        break

    if user.lower() == "memory":

        print(
            "\nCurrent Window:\n"
        )

        print(
            memory.get_context()
        )

        continue

    memory.add_message(
        "User",
        user
    )

    response = (
        f"I received: {user}"
    )

    print(
        "Bot:",
        response
    )

    memory.add_message(
        "Bot",
        response
    )