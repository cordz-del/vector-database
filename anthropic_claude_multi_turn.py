# anthropic_claude_example_multi_turn.py
import os
import requests
import json

def continue_claude_conversation(conversation_prompt):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set.")
    
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    # Construct conversation prompt
    prompt = f"\n\nHuman: {conversation_prompt}\n\nAssistant:"
    data = {
        "prompt": prompt,
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
    conversation_prompt = "I'm really stressed about my upcoming presentation. What advice do you have?"
    print("Claude Multi-Turn Response:")
    print(continue_claude_conversation(conversation_prompt))
