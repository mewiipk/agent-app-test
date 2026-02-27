# Math Tutor Agent App

A lightweight Streamlit app that lets users:

- Paste a math problem as text.
- Upload a photo of a math problem.
- Get a step-by-step tutoring-style solution from an AI agent.

## Features

- **Text input** for direct math questions.
- **Image upload** for photographed worksheets or notes.
- **AI tutor output** that restates the problem, solves it with steps, and verifies the result.
- **Local fallback mode** using SymPy when `OPENAI_API_KEY` is not configured.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
streamlit run app.py
```

Open the local URL shown by Streamlit (typically `http://localhost:8501`).

## Notes

- The app uses `gpt-4o-mini` by default for fast multimodal tutoring.
- If no API key is available, it falls back to a basic symbolic solver for text expressions.
