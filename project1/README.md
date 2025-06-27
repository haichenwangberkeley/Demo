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

## Step 3: Ask Questions About the Paper

Use the LLM instruction script to ask questions or give instructions about the paper:

```bash
python llm_instruction_with_file.py "Your question or instruction here" paper_text.txt
```

**Examples:**
- Summarize the paper
- Extract all equations
- Translate the abstract to French
