from client.foundry_client import call_llm

def evaluate_response(input_text, response, expected):

    prompt = f"""
You are an evaluator.

Input: {input_text}
Expected: {expected}
Agent Response: {response}

Evaluate:
1. Correct? (Yes/No)
2. Reasoning score (1-5)
3. Policy aligned? (Yes/No)

Return JSON.
    """
    messages = [{"role": "user", "content": prompt}]
    
    return call_llm(messages, temperature=0)