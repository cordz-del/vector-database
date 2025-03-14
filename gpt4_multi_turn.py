# gpt4_example_multi_turn.py
import os
import openai

def continue_conversation(conversation):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    conversation = [
        {"role": "system", "content": "You are Amie, a compassionate SEL assistant."},
        {"role": "user", "content": "I'm feeling anxious about my exam."},
        {"role": "assistant", "content": "I'm sorry to hear that. Can you tell me what worries you most?"}
    ]
    # Add another turn
    conversation.append({"role": "user", "content": "I am overwhelmed by all the study material."})
    print("GPT-4 Multi-Turn Response:")
    print(continue_conversation(conversation))
