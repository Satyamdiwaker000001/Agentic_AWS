from Agentic.summary_memory_bot.memory import SummaryMemory
from Agentic.summary_memory_bot.summarizer import update_summary

memory = SummaryMemory()

print("SUMMARY MEMORY BOT")

while True:

    user = input("\nYou: ")

    if user.lower() == "exit":
        break

    if user.lower() == "memory":

        print("\nSummary Memory:")
        print(memory.load_summary())
        continue

    old_summary = memory.load_summary()

    new_summary = update_summary(
        old_summary,
        user
    )

    memory.save_summary(new_summary)

    response = (
        "I have updated my summary memory."
    )

    print("Bot:", response)