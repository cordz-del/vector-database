# chroma_rest_api_example.py
from flask import Flask, request, jsonify
import chromadb
from chromadb.config import Settings
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

app = Flask(__name__)

# Initialize Chroma client
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
collection = client.get_or_create_collection(name="documents")

# Load embedding model (MiniLM)
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(texts, model, tokenizer):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.numpy()

@app.route('/api/add_document', methods=['POST'])
def add_document():
    data = request.get_json()
    document = data.get("document")
    if not document:
        return jsonify({"error": "Document is required"}), 400
    
    embedding = embed_text([document], model, tokenizer)
    doc_id = f"doc_{len(collection.get()['ids']) + 1}"
    collection.add(
        ids=[doc_id],
        documents=[document],
        embeddings=[embedding[0].tolist()],
        metadatas=[{"source": "api"}]
    )
    return jsonify({"message": "Document added", "id": doc_id}), 201

@app.route('/api/query', methods=['POST'])
def query_documents():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400
    query_embedding = embed_text([query], model, tokenizer)
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3
    )
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
