# anthropic_claude_example.py
import os
import requests
import json

def ask_claude(prompt):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set.")
    
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    data = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "model": "claude-v1",
        "max_tokens_to_sample": 150,
        "temperature": 0.7,
        "stop_sequences": ["\n\nHuman:"]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result.get("completion", "").strip()
    else:
        raise Exception(f"Claude API error: {response.status_code} {response.text}")

if __name__ == "__main__":
    prompt = "Explain how prompt engineering improves AI responses."
    print("Anthropic Claude Response:")
    print(ask_claude(prompt))
