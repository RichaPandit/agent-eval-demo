import json
from client.foundry_client import call_llm

def evaluate_response(input_text, response, expected):
    prompt = f"""
You are an evaluator for an expense approval agent.

Input: {input_text}
Expected Decision: {expected}
Agent Response: {response}

Return STRICT JSON in this exact schema:

{{
  "correct": true | false,
  "reasoning_score": 1 | 2 | 3 | 4 | 5,
  "policy_aligned": true | false,
  "rationale": "short explanation"
}}

Do not add extra text. JSON only.
    """

    messages = [{"role": "user", "content": prompt}]
    raw = call_llm(messages, temperature=0)

    try:
        return json.loads(raw)
    except Exception:
        # Fallback if model misbehaves
        return {
            "correct": False,
            "reasoning_score": 1,
            "policy_aligned": False,
            "rationale": "Invalid JSON from evaluator"
        }