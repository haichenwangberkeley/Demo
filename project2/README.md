# Project 2: Retrieval-Augmented Generation (RAG) Demo

This project demonstrates how to use embeddings and cosine similarity to select the most relevant context for a question, a key step in RAG workflows.

## Step 1: Prepare Input Files

You need two text files to compare. For example:
- `paper_text.txt` (from Project 1)
- `declaration_of_independence.txt` (download or create this file)

## Step 2: Run the Embedding and Context Selection Script

Use the script to embed both files and your question, then select the most relevant context:

```bash
python embed_and_select_context.py paper_text.txt declaration_of_independence.txt "Did Thomas Jefferson sign the declaration of independence?"
```

The script will:
- Compute cosine similarity between your question and each file
- Print the similarity scores
- Select and display the file with the highest similarity as the context
- Show a snippet of the selected context

**Check if the selection is correct:**
- If you ask a question about physics, the script should select `paper_text.txt`
- If you ask about American history, it should select `declaration_of_independence.txt`
