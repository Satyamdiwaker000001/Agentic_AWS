from utils.generate import generate_response

def math_agent(state):
    message = state["message"]
    
    # Generate response using LLM
    prompt = f"Solve the following math problem step by step. Show the method, each step clearly, and the final answer. Problem: {message}"
    raw_response = generate_response(prompt)

    return {
        "response": raw_response,
        "metadata": {
            "problem": message,
            "method": "Analytical Solver",
            "steps": [
                {"title": "Solution", "content": raw_response}
            ],
            "answer": "See detailed steps above"
        }
    }