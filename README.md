# Scientific Multi-Agent Literature Search System

A **Multi-Agent Scientific Literature Search System** built with **LangGraph**, **LangChain**, **Groq LLM**, **OpenAlex**, **Crossref**, **arXiv**, and **Streamlit**.

The goal of this project is to demonstrate how multiple specialized AI agents can collaboratively solve a complex research task. Instead of relying on a single LLM prompt, the system decomposes the workflow into multiple intelligent agents that each perform one well-defined task.

The project is intended for research and educational purposes and demonstrates the use of **LangGraph** for orchestrating multi-agent workflows.

---

# Features

- Scientific relevance classification
- Automatic generation of academic search queries
- Literature search across multiple scientific databases
- Paper ranking using LLM reasoning
- Automatic paper selection
- Scientific answer generation
- Automatic answer evaluation
- Interactive Streamlit dashboard
- Paper scoring and ranking
- Open paper links
- Modular multi-agent architecture

---

# System Architecture

```
                        User Question
                              │
                              ▼
                Scientific Relevance Agent
                              │
             Scientific? ─────┴────── No
                  │                    │
                 Yes                   ▼
                  │             Reject Question
                  ▼
               Search Query Agent
                  │
                  ▼
            Literature Search Agent
                  │
      ┌────────────┬────────────┬
      │            │            │
      ▼            ▼            ▼
   OpenAlex     Crossref      arXiv
      │            │            │
      └────────────┴────────────┘
                  │
                  ▼
          Deduplication
                  │
                  ▼
            Ranking Agent
                  │
                  ▼
        Paper Selection Agent
                  │
                  ▼
      Answer Generation Agent
                  │
                  ▼
      Answer Evaluation Agent
                  │
      ┌───────────┴───────────┐
      │                       │
   Passed                  Failed
      │                       │
      ▼                       ▼
 Final Answer         Revision Agent
      │                       │
      └───────────────┬───────┘
                      ▼
                 Streamlit UI
```

---

# Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Programming language |
| LangGraph | Multi-agent workflow orchestration |
| LangChain | LLM abstraction |
| Groq API | Large Language Model |
| Llama 3.3 70B | Reasoning model |
| Streamlit | User interface |
| OpenAlex API | Scientific literature search |
| Crossref API | Publication metadata |
| arXiv API | Scientific preprints and full abstracts |
| Pydantic | Structured outputs |
| Requests | API communication |

---

# Large Language Model

The project uses **Groq** as the inference provider.

Default model:

```
llama-3.3-70b-versatile
```

The model is used for:

- relevance classification
- query generation
- paper ranking
- paper selection
- answer generation
- answer evaluation
- answer revision

---

# LangGraph Workflow

The workflow is implemented as a directed state graph.

Each node represents one autonomous agent.

```
Relevance
      │
      ▼
Search Query
      │
      ▼
Search
      │
      ▼
Ranking
      │
      ▼
Paper Selection
      │
      ▼
Answer Generation
      │
      ▼
Answer Evaluation
      │
 Passed? ────────► END
      │
      ▼
Revision
      │
      ▼
END
```

The graph uses conditional routing.

If the question is not scientific, the workflow terminates immediately.

If the generated answer does not satisfy the evaluation agent, a revision step is executed.

---

# Agents

## 1. Scientific Relevance Agent

### Purpose

Determines whether the user's question is explicitly scientific.

### Responsibilities

- Reject weather questions
- Reject recipes
- Reject shopping requests
- Reject entertainment requests
- Accept academic research questions
- Identify the research domain

### Output

```python
{
    "is_scientific": True,
    "research_domain": "Computer Science"
}
```

---

## 2. Search Query Agent

### Purpose

Transforms the user question into multiple academic search queries.

### Responsibilities

- Generate Boolean search expressions
- Use academic terminology
- Translate concepts into English when appropriate
- Generate multiple search strategies

Example:

```
("Large Language Models" OR LLM)
AND
("Scientific Literature Search")
```

---

## 3. Literature Search Agent

### Purpose

Retrieves publications from scientific databases.

Currently supported:

- OpenAlex
- Crossref
- arXiv

Responsibilities:

- execute every search query
- collect publications
- merge results
- remove duplicates

---

## 4. Ranking Agent

### Purpose

Ranks every publication.

Each paper receives four scores.

### Relevance Score

How well the paper answers the question.

Range:

```
0–100
```

### Quality Score

Estimated publication quality based on:

- journal
- conference
- metadata
- completeness
- publication type

Range:

```
0–100
```

### Recency Score

Higher scores are assigned to more recent publications when appropriate.

Range:

```
0–100
```

### Final Score

Weighted score

```
60% Relevance
25% Quality
15% Recency
```

Papers are sorted descending by Final Score.

---

## 5. Paper Selection Agent

Uses the ranking results to determine which papers should be included.

Selection criteria include:

- high relevance
- sufficient metadata
- scientific usefulness

Only the strongest papers are forwarded.

---

## 6. Answer Generation Agent

Creates the final scientific answer.

The answer includes:

- summary
- literature overview
- important findings
- research gaps
- recommendations

Only selected papers are used.

---

## 7. Answer Evaluation Agent

Checks whether the generated answer satisfies the original question.

Evaluation criteria include:

- correctness
- completeness
- relevance
- scientific quality
- evidence usage

---

## 8. Revision Agent

If evaluation fails:

- improve the answer
- correct weaknesses
- generate a revised response

---

# Scientific Search Tools

## OpenAlex

Used for:

- publication search
- abstracts
- DOI
- publication year
- citation count

API:

https://api.openalex.org

---

## Crossref

Used for:

- publication metadata
- DOI
- journal information
- publication year

API:

https://api.crossref.org

---

## arXiv

Used for:

- scientific preprints
- full abstracts
- author information
- publication date
- PDF links
- research categories

arXiv is especially useful for rapidly evolving research areas such as:

- Artificial Intelligence
- Large Language Models
- Machine Learning
- Natural Language Processing
- Computer Science

API:

https://export.arxiv.org/api/query

---

# Project Structure

```
scientific-agent/

│
├── agents/
│
├── graph/
│
├── prompts/
│
├── models/
│
├── tools/
│
├── frontend/
│
├── app.py
│
├── streamlit_app.py
│
├── config.py
│
├── requirements.txt
│
└── .env.example
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/TutaevaIrina/AI-Agent-LangGraph.git

cd scientific-agent
```

---

## 2. Create a virtual environment

Windows

```powershell
python -m venv .venv
```

Activate

```powershell
.venv\Scripts\Activate.ps1
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a file called

```
.env
```

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

You can obtain a Groq API key at:

https://console.groq.com

---

# Running the Project

## Streamlit (recommended)

```bash
streamlit run streamlit_app.py
```

or

```bash
python -m streamlit run streamlit_app.py
```

---

## Command Line Interface

```bash
python app.py
```

---

# Example Questions

Accepted

```
How can Large Language Models improve scientific literature search?
```

```
Which theories explain consumer trust in fake online reviews?
```

```
What methods are suitable for evaluating a multi-agent research assistant?
```

Rejected

```
What will the weather be tomorrow?
```

```
Give me a cake recipe.
```

```
Recommend a movie.
```

---


# Visualizing the LangGraph Workflow

This project includes a utility script that generates a visualization of the LangGraph workflow.

The script builds the graph defined in `graph/builder.py` and exports it as a Mermaid diagram and/or PNG image.

## Generate the workflow diagram

Run:

```bash
python visualize_graph.py
```

After execution, the generated files are stored in the `images/` directory.

---
