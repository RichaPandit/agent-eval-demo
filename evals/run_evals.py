import json
import sys
from pathlib import Path

from agents.expense_agent import run_agent
from evals.native_evaluator import evaluate_response

from tools.policy_checker import evaluate_policy
from tools.formatter import format_response

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent        # evals/
PROJECT_ROOT = BASE_DIR.parent                   # repo root

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def extract_decision(text: str) -> str:
    return "Approve" if "approve" in text.lower() else "Reject"

# -------------------------------------------------
# Load test cases
# -------------------------------------------------
with open(BASE_DIR / "test_cases.json", "r") as f:
    test_cases = json.load(f)

results = []
correct = 0

# -------------------------------------------------
# Run evals
# -------------------------------------------------
for case in test_cases:
    input_text = case["input"]
    expected = case["expected"]

    # Optional structured fields
    amount = case.get("amount")
    expense_type = case.get("expense_type")

    # 1️. Run agent
    agent_response = run_agent(input_text)
    
    actual_decision = agent_response["decision"]
    raw_reason = agent_response["reason"]

    # 2️. Extract decision
    actual_decision = extract_decision(agent_response)

    # 3️. FORMAT RESPONSE for evaluation
    formatted_response = format_response(actual_decision, raw_reason)

    # 4️. Policy evaluation (deterministic)
    policy_decision, policy_reason = evaluate_policy(amount, expense_type)

    # 5️. Ground truth check
    is_correct = actual_decision == expected
    if is_correct:
        correct += 1

    # 6️. LLM semantic evaluation (structured)
    judge = evaluate_response(
        input_text=input_text,
        response=formatted_response,
        expected=expected
    )

    # 7️. Failure classification
    if is_correct:
        failure_type = "None"
    elif actual_decision != policy_decision:
        failure_type = "Policy violation"
    elif judge["correct"]:
        failure_type = "Extraction / formatting issue"
    else:
        failure_type = "Reasoning error"

    results.append({
        "input": input_text,
        "expected": expected,
        "actual": actual_decision,
        "formatted_response": formatted_response,
        "policy_decision": policy_decision,
        "policy_reason": policy_reason,
        "judge": judge,
        "status": "PASS" if is_correct else "FAIL",
        "failure_type": failure_type
    })

# -------------------------------------------------
# Aggregate metrics
# -------------------------------------------------
accuracy = round((correct / len(test_cases)) * 100, 2)
THRESHOLD = 80

print(f"Accuracy: {accuracy}%")

status_flag = 1 if accuracy < THRESHOLD else 0

# -------------------------------------------------
# HTML Report
# -------------------------------------------------
html = f"""
<h1>Agent Evaluation Report</h1>
<h2>Accuracy: {accuracy}%</h2>
<table border="1" cellpadding="6">
<tr>
  <th>Input</th>
  <th>Expected</th>
  <th>Actual</th>
  <th>Status</th>
  <th>Policy Decision</th>
  <th>LLM Correct</th>
  <th>Reasoning Score</th>
  <th>Failure Type</th>
  <th>LLM Rationale</th>
</tr>
"""

for r in results:
    color = "green" if r["status"] == "PASS" else "red"
    html += f"""
    <tr>
      <td>{r['input']}</td>
      <td>{r['expected']}</td>
      <td>{r['actual']}</td>
      <td style="color:{color}">{r['status']}</td>
      <td>{r['policy_decision']}</td>
      <td>{r['judge']['correct']}</td>
      <td>{r['judge']['reasoning_score']}</td>
      <td>{r['failure_type']}</td>
      <td>{r['judge']['rationale']}</td>
    </tr>
    """

html += "</table>"

with open(PROJECT_ROOT / "report.html", "w") as f:
    f.write(html)

# -------------------------------------------------
# CI exit
# -------------------------------------------------
if status_flag:
    print(f"❌ Build failed: accuracy {accuracy}% < {THRESHOLD}%")
else:
    print("✅ Build passed")

sys.exit(status_flag)