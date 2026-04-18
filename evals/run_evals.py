import json
import sys
from pathlib import Path
from agents.expense_agent import run_agent
from evals.native_evaluator import evaluate_response


BASE_DIR = Path(__file__).resolve().parent   # evals/
PROJECT_ROOT = BASE_DIR.parent               # repo root


def extract_decision(text):
    if "approve" in text.lower():
        return "Approve"
    return "Reject"

with open(BASE_DIR / "test_cases.json", "r") as f:
    test_cases = json.load(f)

results = []
correct = 0

for case in test_cases:
    input_text = case["input"]
    expected = case["expected"]

    response = run_agent(input_text)
    actual = extract_decision(response)

    is_correct = actual == expected
    if is_correct:
        correct += 1

    judge = evaluate_response(input_text, response, expected)
        
    results.append({
        "input": input_text,
        "expected": expected,
        "actual": actual,
        "response": response,
        "status": "PASS" if is_correct else "FAIL",
        "judge": judge
    })

accuracy = round((correct / len(test_cases)) * 100, 2)

THRESHOLD = 80

if accuracy < THRESHOLD:
    print(f"Build failed: {accuracy}%")
    status_flag = 1
else:
    print(f"Build passed: {accuracy}%")
    status_flag = 0

# -----------------------------------------
# HTML Report Generation
# -----------------------------------------

html = f"<h1>Agent Eval Report</h1><h2>Accuracy: {accuracy}%</h2><table border='1'>"
html += "<tr><th>Input</th><th>Expected</th><th>Actual</th><th>Status</th><th>LLM Eval</th></tr>"

for r in results:
    color = "green" if r['status'] == "PASS" else "red"
    html += f"<tr><td>{r['input']}</td><td>{r['expected']}</td><td>{r['actual']}</td><td style='color:{color}'>{r['status']}</td><td>{r['judge']}</td></tr>"

html += "</table>"

with open(PROJECT_ROOT / "report.html", "w") as f:
    f.write(html)

sys.exit(status_flag)