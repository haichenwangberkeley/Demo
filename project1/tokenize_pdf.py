# Example: Tokenize a PDF file using pdfminer.six and tiktoken
from pdfminer.high_level import extract_text
import tiktoken

# Extract text from PDF
pdf_path = "paper.pdf"
text = extract_text(pdf_path)

# Optional: Clean text (remove excessive whitespace)
text = ' '.join(text.split())

# Tokenize using GPT-4 encoding
tokenizer = tiktoken.encoding_for_model("gpt-4")
tokens = tokenizer.encode(text)

# Save extracted text
with open("paper_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Save tokens as comma-separated integers
with open("paper_tokens.txt", "w", encoding="utf-8") as f:
    f.write(",".join(map(str, tokens)))

print(f"Number of tokens: {len(tokens)}")
