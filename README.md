# NormalObjects - Creative Complaint Handler (LangChain)

This repository contains the complete lab solution for **LAB | NormalObjects - Creative Complaint Handler (LangChain)**.

The project builds **Becma's Chaos Mode**, a creative LangChain agent that handles fictional complaints about inconsistencies in the Normal Objects universe. The agent can use custom themed tools in flexible orders and then produce a creative Bureau Resolution.

## File map

```text
normalobjects-creative-complaint-handler/
├── README.md                         # Setup, run instructions, and file map
├── lab_summary.md                    # Required one-paragraph reflection
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variable template
├── .gitignore                        # Keeps secrets and virtual env out of GitHub
├── normalobjects_langchain.py        # Main complete agent implementation
├── notebooks/
│   └── normalobjects_workflow.ipynb  # Workflow notebook
└── outputs/
    └── demo_results.md               # Demo evidence; refresh after real API run
```

## Requirements

- macOS with VS Code installed
- Python 3.11 or 3.12 recommended
- OpenAI API key available as `OPENAI_API_KEY`
- A terminal using `zsh`

## Quick start

```bash
cd normalobjects-creative-complaint-handler
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and replace the placeholder with your real key:

```bash
OPENAI_API_KEY=sk-your-real-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
```

Run the real LangChain agent:

```bash
python normalobjects_langchain.py
```

Run a no-API environment check first:

```bash
python normalobjects_langchain.py --mock
```

## What the script demonstrates

The script handles at least four complaints, records intermediate LangChain tool calls, prints the tool sequence for each complaint, and writes `outputs/demo_results.md`.

The custom tools are:

- `consult_demogorgon`
- `check_hawkins_records`
- `cast_interdimensional_spell`
- `gather_party_wisdom`
- `consult_eleven_signal`

## Notebook workflow

Open `notebooks/normalobjects_workflow.ipynb` in VS Code after selecting the `.venv` interpreter. Run the cells top to bottom.

The notebook shows:

1. Environment check
2. Tool inspection
3. Agent construction
4. At least three complaints handled
5. Tool usage analysis
6. Demo output saved to Markdown

## GitHub submission checklist

Before submitting the GitHub URL:

```bash
python normalobjects_langchain.py
git status
```

Confirm that the repository contains only this lab project, includes `README.md`, includes the required one-paragraph `lab_summary.md`, includes the Python script, includes the notebook, and includes demonstration evidence in `outputs/demo_results.md`.

Never commit your `.env` file.
