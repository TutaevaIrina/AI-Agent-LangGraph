# AI Research Assistant using LangGraph

## Overview

This project implements an AI-powered research assistant using **LangGraph**. The agent helps researchers find relevant scientific papers, evaluate their credibility, rank the results, and generate a structured research report.

The system uses:

- **LangGraph** for workflow orchestration
- **Google Gemini** as the Large Language Model (LLM)
- **arXiv API** for scientific paper retrieval
- **Crossref API** for DOI and publication metadata verification

---

## Workflow

The agent follows the workflow below:

```text
User Question
      │
      ▼
Planner
      │
      ├── Research / General Knowledge
      │          │
      │          ▼
      │     arXiv Search
      │          ▼
      │  Source Evaluation
      │          ▼
      │      Ranking
      │          ▼
      │  Report Generation
      │
      └── Out of Scope
             ▼
      Friendly Response
```

---

## Features

- Searches academic literature using the **arXiv API**
- Evaluates the credibility of scientific sources
- Verifies DOI and publication metadata using **Crossref**
- Ranks papers based on relevance and credibility
- Generates structured research reports using Google Gemini
- Handles non-research questions gracefully
- Provides a fallback report if the LLM is unavailable

---

## Installation

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment (Windows PowerShell)

```bash
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root and add your Google API key:

```text
GOOGLE_API_KEY="your_api_key"
```

---

## Run the project

```bash
python app.py
```

---

## Example Query

```text
How can AI agents support literature review in academic research?
```