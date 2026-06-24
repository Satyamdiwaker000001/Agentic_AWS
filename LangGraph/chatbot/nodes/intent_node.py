def intent_node(state):

    print("\n===== INTENT NODE =====")

    message = state["message"].lower()

    if "hello" in message or "hi" in message:
        intent = "greeting"

    else:
        intent = "question"

    print("Detected Intent:", intent)

    return {
        "intent": intent
    }