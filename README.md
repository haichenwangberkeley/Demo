# Demo Project Setup

These tutorials are developed for the 2025 DOE Computational High Energy Physics Traineeship Summer School. For more information and the full schedule, see the [Indico event page](https://indico.cern.ch/event/1531818/timetable/?view=standard).

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

## Setting Up the CBORG API Key

To use the LLM API, you need to set your CBORG API key as an environment variable. **Never hard-code your API key in scripts or commit it to git.**

Example (add this to your terminal or your shell profile):

```bash
export CBORG_API_KEY="sk-demo1234567890abcdef"
# The above key value is a dummy, just for demo purpose
```

Replace the value with your actual API key. This ensures your credentials remain secure and are not exposed in code or version control.
