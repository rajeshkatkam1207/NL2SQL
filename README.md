
# NL2SQL - Natural Language to SQL

## Overview
NL2SQL is a minimal working reference implementation that converts natural language questions into executable SQL queries against a local SQLite database using the OpenAI API.

## Requirements
- Python 3.10+
- An OpenAI API key (set via the Streamlit UI or environment variable `OPENAI_API_KEY`)

## How to run
1. Extract the archive.
2. Install dependencies: `pip install -r code/src/requirements.txt`
3. Initialize the database (automatically done on first run) or run `python code/src/db.py`
4. Run the Streamlit app: `streamlit run code/src/app.py`

## Files
- `code/src/app.py` — Streamlit UI
- `code/src/db.py` — SQLite database init + helper
- `code/src/sql_generator.py` — OpenAI-integrated SQL generation + validation
- `code/src/nl2sql_agent.py` — Lightweight agent wrapping generator + execution
- `code/src/sample_data.sql` — SQL schema + sample inserts
- `code/test/` — pytest test cases


## Step B additions
- Improved prompt + few-shot examples in `code/src/sql_generator.py`
- LangChain agent scaffold `code/src/langchain_agent.py`
- Clarification loop in `code/src/nl2sql_agent.py`
- Filled architecture and test report (in `artifacts/arch/` as markdown)
- Demo storyboard and placeholder demo video in `artifacts/demo/`
