#!/usr/bin/env python3
"""
embed_and_select_context.py

Usage:
    python embed_and_select_context.py file1.txt file2.txt "your question here"

This script embeds two text files and a question, computes cosine similarity between the question and each file, and selects the more similar file as context for an LLM call.
"""
import os
import sys
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import hashlib

MODEL = "lbl/nomic-embed-text"

if len(sys.argv) != 4:
    print("Usage: python embed_and_select_context.py file1.txt file2.txt 'your question here'")
    sys.exit(1)

file1 = sys.argv[1]
file2 = sys.argv[2]
question = sys.argv[3]

with open(file1, "r", encoding="utf-8") as f:
    doc1 = f.read()
with open(file2, "r", encoding="utf-8") as f:
    doc2 = f.read()

openai.api_key = os.environ.get('CBORG_API_KEY')
openai.base_url = "https://api.cborg.lbl.gov"

# Try to load cached embeddings for docs
embeddings_cache = "embeddings_cache.pkl"
cache = {}
if os.path.exists(embeddings_cache):
    with open(embeddings_cache, "rb") as f:
        cache = pickle.load(f)

def get_embedding(text, key):
    if key in cache:
        return cache[key]
    response = openai.embeddings.create(
        model=MODEL,
        input=text
    )
    emb = response.data[0].embedding
    cache[key] = emb
    with open(embeddings_cache, "wb") as f:
        pickle.dump(cache, f)
    return emb

# Use file content hash as key for caching
def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

key1 = file_hash(file1)
key2 = file_hash(file2)

d1 = get_embedding(doc1, key1)
d2 = get_embedding(doc2, key2)

# Embed the question (no cache for questions)
response = openai.embeddings.create(
    model=MODEL,
    input=question
)
q = response.data[0].embedding

query_vec = np.array([q])
doc_vecs = np.array([d1, d2])
sims = cosine_similarity(query_vec, doc_vecs)[0]

print(f"Cosine similarity to {file1}: {sims[0]:.4f}")
print(f"Cosine similarity to {file2}: {sims[1]:.4f}")

# Select the more similar document as context
if sims[0] >= sims[1]:
    context = doc1
    context_file = file1
else:
    context = doc2
    context_file = file2

print(f"\nSelected context: {context_file}\n")

# Placeholder for LLM call using the selected context
print("# You can now use the selected context in an LLM prompt, e.g.:")
print(f"# LLM prompt: {question}\n\nContext:\n{context[:200]}...\n")
