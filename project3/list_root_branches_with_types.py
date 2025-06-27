#!/usr/bin/env python3
"""
list_root_branches_with_types.py

Usage:
    python list_root_branches_with_types.py input.root [tree_name]

Prints and saves all branch names and their types in the specified ROOT file (and tree) to 'branches_with_types.txt'.
If tree_name is not provided, the first tree in the file is used.
"""
import sys
import uproot

def main():
    if len(sys.argv) < 2:
        print("Usage: python list_root_branches_with_types.py input.root [tree_name]")
        sys.exit(1)
    rootfile = sys.argv[1]
    tree_name = sys.argv[2] if len(sys.argv) > 2 else None

    file = uproot.open(rootfile)
    if tree_name is None:
        # Pick the first TTree in the file
        tree_name = next((k for k in file.keys() if file[k].classname.startswith("TTree")), None)
        if tree_name is None:
            print("No TTree found in file.")
            sys.exit(1)
    tree = file[tree_name]
    print(f"Branches and types in {tree_name}:")
    with open("branches_with_types.txt", "w") as f:
        for b in tree.keys():
            try:
                dtype = tree[b].interpretation
                print(f"{b}: {dtype}")
                f.write(f"{b}: {dtype}\n")
            except Exception as e:
                print(f"{b}: [type unavailable] ({e})")
                f.write(f"{b}: [type unavailable]\n")
    print(f"Branch list with types saved to branches_with_types.txt")

if __name__ == "__main__":
    main()
