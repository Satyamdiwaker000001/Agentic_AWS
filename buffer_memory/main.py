from Agentic.buffer_memory.memory import BufferMemory

memory = BufferMemory()

print("=" * 50)
print("AGENTIC AI CHAT")
print("Type 'memory' to see memory")
print("Type 'clear' to clear memory")
print("Type 'exit' to quit")
print("=" * 50)

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Goodbye")
        break

    elif user_input.lower() == "memory":
        print("\n----- MEMORY -----")
        print(memory.get_memory())
        print("------------------")
        continue

    elif user_input.lower() == "clear":
        memory.clear_memory()
        print("Memory Cleared")
        continue

    # Save user message
    memory.save_message("User", user_input)

    # Dummy Agent Response
    response = f"I received your message: {user_input}"

    print(f"Agent: {response}")

    # Save agent response
    memory.save_message("Agent", response)