# faiss_indexing_example.py
# This example shows how to index documents using FAISS for retrieval.

import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

def embed_text(texts, model, tokenizer):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.numpy()

def main():
    # Example documents
    documents = [
        "Amie is a compassionate SEL assistant.",
        "Prompt engineering improves AI performance.",
        "Vector databases help retrieve relevant data efficiently."
    ]
    
    # Load a small transformer model for embeddings
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    
    # Get embeddings for each document
    embeddings = embed_text(documents, model, tokenizer)
    
    # Create a FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print("Indexed documents:", index.ntotal)
    
    # Example query
    query = "How can prompt engineering boost performance?"
    query_embedding = embed_text([query], model, tokenizer)
    
    # Retrieve top 2 nearest documents
    distances, indices = index.search(query_embedding, k=2)
    print("Query:", query)
    print("Nearest documents:")
    for idx in indices[0]:
        print(documents[idx])

if __name__ == "__main__":
    main()
