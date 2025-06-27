# Demo Project Setup

This guide will help you set up a Python environment and install the required packages for this workspace.

## 1. Create a Python Virtual Environment

It is recommended to use a virtual environment to manage dependencies. You can use `venv` (built-in) or `conda` (if you prefer Anaconda/Miniconda).

### Using `venv` (Standard Python)

```bash
python3 -m venv venv
source venv/bin/activate
```

### Using `conda` (Optional)

```bash
conda create -n demo-env python=3.10
conda activate demo-env
```

## 2. Install Required Packages

With your environment activated, install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## 3. Verify Installation

You can check that the packages are installed by running:

```bash
pip list
```

## 4. Project Usage

See the README in each project directory for instructions on running the individual projects.
