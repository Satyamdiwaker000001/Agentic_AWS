from utils.generate import generate_response

def physics_agent(state):
    message = state['message']

    # Generate response using LLM
    prompt = f'Solve the following physics problem. Show given values, formula, calculation, and final answer clearly. Problem: {message}'
    raw_response = generate_response(prompt)

    return {
        'response': raw_response,
        'metadata': {
            'given': {'Query Problem': message},
            'formula': 'Applied physics principles',
            'substitution': 'See detailed response',
            'calculation': 'Step-by-step in response',
            'answer': 'See response above'
        }
    }

