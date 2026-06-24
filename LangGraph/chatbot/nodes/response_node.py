def response_node(state):

    print("\n===== RESPONSE NODE =====")

    intent = state["intent"]

    if intent == "greeting":

        response = "Hello! Nice to meet you."

    else:

        response = (
            f"You asked about: {state['message']}"
        )

    print("Generated Response:", response)

    return {
        "response": response
    }