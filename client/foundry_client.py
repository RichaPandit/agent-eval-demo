import requests
import os

ENDPOINT = os.getenv("FOUNDRY_ENDPOINT")
API_KEY = os.getenv("FOUNDRY_API_KEY")

if not ENDPOINT:
    raise ValueError("FOUNDRY_ENDPOINT is not set or not loaded")
if not API_KEY:
    raise ValueError("FOUNDRY_API_KEY is not set or not loaded")


def call_llm(messages, temperature=0):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY  }
    
    payload = {
        "messages": messages,
        "temperature": temperature
    }
    
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]