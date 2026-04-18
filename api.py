# api.py
from fastapi import FastAPI
from agents.expense_agent import run_agent

app = FastAPI()

@app.post("/evaluate-expense")
def evaluate_expense(payload: dict):
    return run_agent(payload["text"])