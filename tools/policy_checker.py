def evaluate_policy(amount, expense_type):
    if expense_type.lower() == "luxury":
        return "Reject", "Luxury expenses are not allowed"
    if amount > 10000:
        return "Reject", "Amount exceeds limit"
    else:
        return "Approve", "Within allowed limit"