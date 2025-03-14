# chroma_index_example.py
import chromadb
from chromadb.config import Settings
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

def embed_text(texts, model, tokenizer):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.numpy()

def main():
    # Initialize Chroma client (using DuckDB+Parquet for persistence)
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
    collection = client.get_or_create_collection(name="documents")
    
    # Sample documents to index
    documents = [
        "Chroma is an innovative vector database that efficiently stores and retrieves embeddings.",
        "Advanced prompt engineering can significantly improve AI model outputs.",
        "Retrieval-Augmented Generation combines vector search with language models for enriched responses."
    ]
    
    # Load embedding model (MiniLM)
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    
    embeddings = embed_text(documents, model, tokenizer)
    
    # Add documents to the collection
    ids = [f"doc_{i}" for i in range(len(documents))]
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=[emb.tolist() for emb in embeddings],
        metadatas=[{"source": "example"} for _ in documents]
    )
    
    print("Documents have been indexed in Chroma.");
    
    # Example query
    query = "How does prompt engineering enhance AI responses?"
    query_embedding = embed_text([query], model, tokenizer)
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=2
    )
    
    print("Query Results:")
    print(results)

if __name__ == "__main__":
    main()
