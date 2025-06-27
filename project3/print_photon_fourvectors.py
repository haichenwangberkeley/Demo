#!/usr/bin/env python3
"""
print_photon_fourvectors.py

Usage:
    python print_photon_fourvectors.py photon_mapping.txt input.root [tree_name] [n_events]

Reads photon four-vector mapping from photon_mapping.txt, retrieves the corresponding variables from the TTree in the ROOT file, and prints their values for the first n_events (default: 5).

photon_mapping.txt example:
photon 1, pt:photon_pt[0]
photon 1, eta:photon_eta[0]
photon 1, phi:photon_phi[0]
photon 1, E:photon_E[0]
photon 2, pt:photon_pt[1]
...
"""
import sys
import os
import uproot
import openai

def main():
    if len(sys.argv) < 3:
        print("Usage: python print_photon_fourvectors.py photon_mapping.txt input.root [tree_name] [n_events]")
        sys.exit(1)
    mapping_file = sys.argv[1]
    rootfile = sys.argv[2]
    tree_name = sys.argv[3] if len(sys.argv) > 3 else None
    n_events = int(sys.argv[4]) if len(sys.argv) > 4 else 5

    # Use LLM to extract only pt, eta, phi, E for photon 1 and 2 from mapping file
    with open(mapping_file, "r") as f:
        mapping_text = f.read()
    llm_prompt = (
        "From the following mapping, identify which variables correspond to photon 1 and photon 2's pt, eta, phi, and E. Some variables be named slightly differently"
        "Output in the format: photon 1 pt: ..., photon 1 eta: ..., photon 1 phi: ..., photon 1 E: ..., photon 2 pt: ..., etc.\n\n" + mapping_text
    )
    try:
        client = openai.OpenAI(
            api_key=os.environ.get('CBORG_API_KEY'),
            base_url="https://api.cborg.lbl.gov"
        )
        response = client.chat.completions.create(
            model="google/gemini-flash",
            messages=[{"role": "user", "content": llm_prompt}],
            max_tokens=512,
            temperature=0.0,
        )
        llm_result = response.choices[0].message.content
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        sys.exit(1)

    # Parse LLM result for mapping
    mapping = []
    for line in llm_result.splitlines():
        if ":" in line:
            label, var = line.strip().split(":", 1)
            var = var.strip()
            # Only keep the variable name (strip label and any trailing commas)
            if "," in var:
                var = var.split(",")[0].strip()
            mapping.append((label.strip(), var))

    # Open ROOT file and tree
    file = uproot.open(rootfile)
    if tree_name is None:
        tree_name = next((k for k in file.keys() if file[k].classname.startswith("TTree")), None)
        if tree_name is None:
            print("No TTree found in file.")
            sys.exit(1)
    tree = file[tree_name]

    # --- Prepare branch names for uproot ---
    branch_names = set(var.split("[")[0] for _, var in mapping)
    # Remove any empty or invalid branch names (e.g., if LLM output is malformed)
    branch_names = {b for b in branch_names if b and ":" not in b and "," not in b}

    # --- Read arrays for all needed branches from the TTree ---
    arrays = tree.arrays(list(branch_names), entry_stop=n_events, library="np")

    print(f"Printing photon four-vectors for first {n_events} events from {tree_name} in {rootfile}:")
    for i in range(n_events):
        print(f"\nEvent {i}:")
        for label, var in mapping:
            base = var.split("[")[0]
            # --- Bifurcation: Handle vector (with index) vs scalar variable ---
            if "[" in var and "]" in var:
                # Vector case: extract index and access the element
                try:
                    idx = int(var[var.find("[")+1:var.find("]")])
                    arr = arrays[base][i]
                    # Check if arr is a vector and idx is valid
                    if hasattr(arr, "__len__") and len(arr) > idx:
                        value = arr[idx]
                    else:
                        value = "N/A"
                except Exception:
                    value = "N/A"
            else:
                # Scalar case: access the value directly
                try:
                    arr = arrays[base][i]
                    # If arr is a length-1 vector, print the value; else print as is
                    if hasattr(arr, "__len__") and not isinstance(arr, (str, bytes)) and len(arr) == 1:
                        value = arr[0]
                    else:
                        value = arr
                except Exception:
                    value = "N/A"
            print(f"  {label}: {value}")

if __name__ == "__main__":
    main()
