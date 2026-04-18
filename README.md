# Agent Evaluation Demo (AgentOps)

This project demonstrates a pro-code approach to building and evaluating AI agents using AI Foundry.

## Features
- Modulear agent architecture (agents + tools)
- Azure AI Foundry integration
- Automated evaluation pipeline
- LLM-based evaluator (reasoning + policy check)
- CI/CD with GitHub Actions
- HTML evaluation report

## How it works

1. Agent processes input using tools
2. Evaluation script runs test cases
3. Calls LLM evaluator for reasoning checks
4. Generates reports + pass/fail outcome

## Run locally

```bash
pip install -r requirements.txt
export FOUNDRY_ENDPOINT=your_enpoint
export FOUNDRY_API=your_key

cd evals
python run_evals.py