#!/usr/bin/env python3
"""
interpret_branches_with_llm.py

Usage:
    python interpret_branches_with_llm.py "Your instruction" branches.txt

Example:
    python interpret_branches_with_llm.py "Identify the four-vector variables for photons" branches.txt

This script sends a user instruction and the list of ROOT branches to an LLM and prints the response.
"""
import sys
import os
import openai


DEFAULT_INSTRUCTION = (
    "You are given a list of ROOT TTree branches. Identify the branches that correspond to the four-vector "
    "components (pt, eta, phi, energy or mass) of two photons. The naming convention may vary between datasets. "
    "Photon variables may be stored as scalar values (e.g., ph1_pt) or as arrays (e.g., ph_pt[0], ph_pt[1]).\n\n"
    "Output must follow this strict format:\n"
    "  photon 1 pt: <branch name>\n"
    "  photon 1 eta: <branch name>\n"
    "  photon 1 phi: <branch name>\n"
    "  photon 1 energy: <branch name>\n"
    "  photon 2 pt: <branch name>\n"
    "  photon 2 eta: <branch name>\n"
    "  photon 2 phi: <branch name>\n"
    "  photon 2 energy: <branch name>\n\n"
    "The value after the colon must be the exact branch name as listed in the TTree. "
    "If a component cannot be found, say 'not found'.\n\n"
    "Do not provide any other information. Output only the entries in this exact format.\n\n"
    "Example:\n"
    "  photon 1 pt: gam_pt[0]\n"
    "  photon 1 eta: gam_eta[0]\n"
    "  photon 1 phi: gam_phi[0]\n"
    "  photon 1 energy: gam_E[0]\n"
    "  photon 2 pt: gam_pt[1]\n"
    "  photon 2 eta: gam_eta[1]\n"
    "  photon 2 phi: gam_phi[1]\n"
    "  photon 2 energy: gam_E[1]"
)

# DEFAULT_INSTRUCTION = (
#     "You are given a list of ROOT TTree branches. Identify the branches that correspond to the four-vector "
#     "components (pt, eta, phi, energy or mass) of two photons. The naming convention may vary between datasets. "
#     "Photon variables may be stored as scalar values (e.g., ph1_pt) or as arrays or vectors (e.g., ph_pt[0], ph_pt[1]).\n\n"
#     "Output must follow this strict format:\n"
#     "  photon 1 pt: <branch name>\n"
#     "  photon 1 eta: <branch name>\n"
#     "  photon 1 phi: <branch name>\n"
#     "  photon 1 energy: <branch name>\n"
#     "  photon 2 pt: <branch name>\n"
#     "  photon 2 eta: <branch name>\n"
#     "  photon 2 phi: <branch name>\n"
#     "  photon 2 energy: <branch name>\n\n""
#     "The value after the colon must be the exact branch name as listed in the TTree. "
#     "If a component cannot be found, say 'not found'.\n\n"
#     "Do not provide any other information. Output only the entries in this exact format."
# )


# DEFAULT_INSTRUCTION = (
#     "Identify photon four vector branches. There are always two photons. Their names may vary a bit."
#     "They could be scalars or vectors. Strict output format: name:varialbe. "
#     "e.g., photon 1 pt: ph_pt[0], etc."
#     "photon 2 pt: ph_pt[1], etc." \
#     "the entry after : must be variable name in the TTree branch list."  # Clarify that the entry after : must be a variable name in the TTree branch list
# )

def main():
    # Use default instruction if not provided
    if len(sys.argv) == 2:
        instruction = DEFAULT_INSTRUCTION
        input_file = sys.argv[1]
    elif len(sys.argv) == 3:
        instruction = sys.argv[1]
        input_file = sys.argv[2]
    else:
        print("Usage: python interpret_branches_with_llm.py [<instruction>] <branches.txt>")
        sys.exit(1)
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
            #model="google/gemini-flash",
            model="lbl/cborg-chat:latest",  # Use the latest model for cutflow generation
            # model="lbl/cborg-coder:latest",  # Use the latest model for
            # model="lbl/cborg-deepthought:latest",  # Use the latest model for cutflow generation
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.1,
        )
        result = response.choices[0].message.content
        print(result)
        # Save result to mapping.txt
        with open("mapping.txt", "w", encoding="utf-8") as mf:
            mf.write(result.strip() + "\n")
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
