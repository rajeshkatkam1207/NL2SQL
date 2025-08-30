import os
from pathlib import Path
from db import run_query, init_db
from sql_generator import generate_sql_from_nl

# OpenAI + Gemini SDK
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import google.generativeai as genai

SCHEMA_FILE = Path(__file__).parent / "data" / "banking_schema_sqlite.sql"


def get_schema_text() -> str:
    with open(SCHEMA_FILE) as f:
        return f.read()


def generate_sql_with_llm(
    nl_text: str,
    schema_text: str,
    api_key: str,
    provider: str = "openai",
    model: str = None
) -> str:
    """Generate SQL using either OpenAI (via LangChain) or Gemini (native SDK)."""

    if provider == "openai":
        llm = ChatOpenAI(openai_api_key=api_key, model=model or "gpt-4o", temperature=0)
        prompt_template = ChatPromptTemplate.from_template("""
        You are a SQL generation assistant.
        Schema:
        {schema}

        User request:
        {nl}

        Return only ONE SQL SELECT statement (with semicolon) or CANNOT_ANSWER.
        """)
        chain = prompt_template | llm
        resp = chain.invoke({"schema": schema_text, "nl": nl_text})
        return resp.content.strip()

    elif provider == "gemini":
        genai.configure(api_key=api_key)
        llm = genai.GenerativeModel(model or "gemini-1.5-flash")
        prompt = f"""
        You are a SQL generation assistant.
        Schema:
        {schema_text}

        User request:
        {nl_text}

        Return only ONE SQL SELECT statement ending with semicolon.
        Do NOT include explanations or markdown formatting. Just the SQL.
        """
        resp = llm.generate_content(prompt)
        sql_text = resp.text.strip()
        # 🚨 Cleanup: strip markdown fences if present
        if sql_text.startswith("```"):
            sql_text = sql_text.strip("`")       # remove backticks
            sql_text = sql_text.replace("sql", "", 1).strip()  # remove optional "sql" tag

        return sql_text

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def handle_nl_request(
    nl_text,
    api_key=None,
    model="gpt-4o",
    use_langchain=False,
    provider=None
):
    """
    Main entry for NL → SQL.
    - Auto-detects provider from API key (sk-... = OpenAI, AIza... = Gemini).
    - If use_langchain=False → Gemini uses native SDK, OpenAI uses LangChain.
    """

    init_db(force=False)
    schema = get_schema_text()

    # 🔑 Auto-detect provider
    if not provider:
        if api_key and api_key.startswith("sk-"):
            provider = "openai"
        elif api_key and api_key.startswith("AIza"):
            provider = "gemini"
        elif model.startswith("gemini"):
            provider = "gemini"
        elif model.startswith("gpt"):
            provider = "openai"
        else:
            provider = "gemini"  # default

    if not api_key:
        raise ValueError("No API key provided. Please set OPENAI_API_KEY or GEMINI_API_KEY.")

    # Run with selected method
    sql = generate_sql_with_llm(nl_text, schema, api_key=api_key, provider=provider, model=model)

    # Handle cannot answer
    if sql == "CANNOT_ANSWER":
        return {"sql": None, "result": [], "message": "Cannot answer based on available schema."}

    # Execute query
    results = run_query(sql)
    return {"sql": sql, "result": results, "message": "OK"}
