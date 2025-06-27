#!/usr/bin/env python3
"""
llm_instruction_with_file.py

Usage:
    python llm_instruction_with_file.py "Your instruction here" input_file.txt

Example:
    python llm_instruction_with_file.py "Summarize the following" somefile.txt
    python llm_instruction_with_file.py "Translate the following to French" somefile.txt
    python llm_instruction_with_file.py "Extract all equations from the following" somefile.txt

This script sends a user instruction and the contents of a text file to an LLM (e.g., OpenAI GPT-4) and prints the response.
"""

import sys
import os
import openai  # Make sure openai is installed and your API key is set

def main():
    if len(sys.argv) != 3:
        print("Usage: python llm_instruction_with_file.py \"<instruction>\" <input_file.txt>")
        sys.exit(1)

    instruction = sys.argv[1]
    input_file = sys.argv[2]

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file '{input_file}': {e}")
        sys.exit(1)

    prompt = f"{instruction}:\n\n{text}"

    try:
        client = openai.OpenAI(
            api_key=os.environ.get('CBORG_API_KEY'),
            base_url="https://api.cborg.lbl.gov"
        )
        response = client.chat.completions.create(
            model="google/gemini-flash",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.5,
        )
        result = response.choices[0].message.content
        print(result)
        # Print token usage breakdown if available
        if hasattr(response, 'usage') and response.usage:
            print("\n--- Token Usage ---")
            for k, v in response.usage.model_dump().items():
                print(f"{k}: {v}")
        elif hasattr(response, 'usage'):
            print(f"\nToken usage: {response.usage}")
        else:
            print("\nToken usage information not available.")
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
