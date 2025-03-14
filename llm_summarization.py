# example_llm_summarization.py
from transformers import pipeline

def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    text = ("Artificial intelligence is transforming every industry. "
            "Advances in deep learning and natural language processing are driving innovative solutions "
            "across various fields.")
    print("Summary:")
    print(summarize_text(text))
