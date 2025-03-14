# example_llm_text_generation.py
from transformers import pipeline

def generate_text(prompt):
    generator = pipeline('text-generation', model='gpt2')
    result = generator(prompt, max_length=50, num_return_sequences=1)
    return result[0]['generated_text']

if __name__ == "__main__":
    prompt = "In a futuristic world where AI and humans collaborate,"
    print("Generated text:")
    print(generate_text(prompt))
