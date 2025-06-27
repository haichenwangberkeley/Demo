# Project 1: LLM API Example (Paper Q&A)

This project demonstrates how to download a scientific paper, extract its text, tokenize it, and interact with it using an LLM API.

## Step 1: Download a Paper

Download a PDF from arXiv (or another source). Example:

```bash
wget https://arxiv.org/pdf/2412.10665 -O paper.pdf
```

## Step 2: Extract and Tokenize the PDF

Use the provided script to extract text and tokenize:

```bash
python tokenize_pdf.py
```

This will create two files:
- `paper_text.txt`: The extracted text from the PDF
- `paper_tokens.txt`: The tokenized representation (comma-separated integers)

**Note:**
The number of tokens is usually different from the number of words. This is because tokenization splits text into smaller units (tokens) that may be whole words, subwords, or even single characters, depending on the language model's tokenizer. For example, punctuation, special characters, and long or compound words may be split into multiple tokens, while common short words may be a single token. This is why the token count is often higher than the word count.

## Step 3: Ask Questions About the Paper

Use the LLM instruction script to ask questions or give instructions about the paper:

```bash
python llm_instruction_with_file.py "Your question or instruction here" paper_text.txt
```

**Examples:**
- Summarize the paper
- Extract all equations
- Translate the abstract to French
