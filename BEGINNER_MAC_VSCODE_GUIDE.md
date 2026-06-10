# Beginner Setup Guide - VS Code on Apple Silicon Mac

This guide assumes VS Code is installed and you have an OpenAI API key that can be used as `OPENAI_API_KEY`.

## 1. Create the project folder

Open Terminal and run:

```bash
cd ~/Desktop
mkdir normalobjects-creative-complaint-handler
cd normalobjects-creative-complaint-handler
```

If you downloaded the provided ZIP, unzip it and `cd` into the unzipped folder instead.

## 2. Open in VS Code

```bash
code .
```

If `code` is not found, open VS Code, press `Command + Shift + P`, search `Shell Command: Install 'code' command in PATH`, then retry.

## 3. Check Python

```bash
python3 --version
which python3
```

Use Python 3.11 or 3.12 if available.

## 4. Create and activate the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your terminal prompt should show `(.venv)`.

Check the active Python:

```bash
which python
python --version
```

Expected path should end with:

```text
normalobjects-creative-complaint-handler/.venv/bin/python
```

## 5. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Add API key

```bash
cp .env.example .env
```

Open `.env` in VS Code and replace:

```text
OPENAI_API_KEY=sk-your-real-key-here
```

with your real key.

## 7. Select Python interpreter in VS Code

1. Press `Command + Shift + P`
2. Search `Python: Select Interpreter`
3. Choose the interpreter inside `.venv`
4. It should look like `.venv/bin/python`

## 8. Run the script

First run a safe no-API check:

```bash
python normalobjects_langchain.py --mock
```

Then run the real agent:

```bash
python normalobjects_langchain.py
```

The real run writes:

```text
outputs/demo_results.md
```

## 9. Run the notebook

In VS Code:

1. Open `notebooks/normalobjects_workflow.ipynb`
2. Click `Select Kernel`
3. Choose the `.venv` Python environment
4. Run cells from top to bottom

## 10. GitHub submission

```bash
git init
git add README.md lab_summary.md requirements.txt .gitignore .env.example normalobjects_langchain.py notebooks outputs
git commit -m "Complete NormalObjects LangChain lab"
```

Create a GitHub repository, push it, and submit the repository URL.

Do not commit `.env`.
