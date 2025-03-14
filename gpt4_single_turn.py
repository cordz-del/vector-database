# gpt4_example_single_turn.py
import os
import openai

def ask_gpt4(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful and compassionate assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    prompt = "Explain why prompt engineering is important for AI systems."
    print("GPT-4 Response:")
    print(ask_gpt4(prompt))
