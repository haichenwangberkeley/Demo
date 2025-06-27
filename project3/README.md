# Project 3: ROOT File Analysis with LLM Assistance

This project demonstrates how to analyze ROOT files containing physics data, use LLMs to interpret variable names, and extract photon four-vectors.

## Step 1: Download Example ROOT Files

Download the two example ROOT files:

```bash
wget https://portal.nersc.gov/project/atlas/haichen/DOEschool/v1.root
wget https://portal.nersc.gov/project/atlas/haichen/DOEschool/v2.root
```

- `v1.root` contains photon four-vectors saved as vectors.
- `v2.root` contains photon variables saved as scalars.

## Step 2: Analyze Each File

For each file, run the following sequence:

```bash
python list_root_branches_with_types.py v1.root
python interpret_branches_with_llm.py branches_with_types.txt
python print_photon_fourvectors.py mapping.txt v1.root

python list_root_branches_with_types.py v2.root
python interpret_branches_with_llm.py branches_with_types.txt
python print_photon_fourvectors.py mapping.txt v2.root
```

Each step will overwrite `branches_with_types.txt` and `mapping.txt`, so run them in order for each file.
