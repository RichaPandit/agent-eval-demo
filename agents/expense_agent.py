import re
from tools.policy_checker import evaluate_policy
from tools.formatter import format_response

def extract_details(user_input):
    amount_match = re.search(r"\d+", user_input)
    amount = int(amount_match.group()) if amount_match else 0

    if "luxury" in user_input.lower():
        expense_type = "luxury"
    elif "travel" in user_input.lower():
        expense_type = "travel"
    else:
        expense_type = "general"

    return amount, expense_type

def run_agent(user_input):
    amount, expense_type = extract_details(user_input)
    decision, reason = evaluate_policy(amount, expense_type)
    return {
        "decision": decision,
        "reason": reason,
        "amount": amount,
        "expense_type": expense_type
    }
