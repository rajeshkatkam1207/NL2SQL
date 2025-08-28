
# NL2SQL Architecture Document

## Overview
NL2SQL translates natural language questions into SQL queries for a local SQLite banking sample database.

## Components
- **Streamlit UI (app.py):** collects user input and displays generated SQL and results.
- **SQL Generator (sql_generator.py):** builds schema-aware prompts and calls OpenAI to create SQL (SELECT only).
- **Agent (nl2sql_agent.py / langchain_agent.py):** orchestrates generation, clarification, and execution.
- **Database (db.py):** initializes and queries a local SQLite database using `sample_data.sql`.

## Prompting Strategy
- Schema-aware prompts: the SQL generator includes the schema in the prompt, plus few-shot examples to improve accuracy.
- Safety rules: the model is restricted to return only a single SELECT statement or `CANNOT_ANSWER`.

## Clarification & Multi-turn
- A simple clarification loop is implemented: if a generated query returns no rows, the system requests clarification options.
- Optional LangChain-based conversational agent scaffold included (requires langchain installation).

## Limitations & Future Work
- The current few-shot examples are small; add more representative examples to improve edge cases.
- Implement syntactic parsing of schema for stronger validation (e.g., explicit allowed column lists).
- Add parameterized queries to further protect against unexpected inputs.
