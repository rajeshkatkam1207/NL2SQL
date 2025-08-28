import os
import re
from typing import List
from openai import OpenAI

FEW_SHOT_EXAMPLES: List[dict] = [
    {
        "nl": "List all customers in Hyderabad",
        "sql": "SELECT customer_id, name, city FROM customers WHERE city = 'Hyderabad';"
    },
    {
        "nl": "Show account balances for customer Alice Gupta",
        "sql": "SELECT a.account_id, a.account_type, a.balance FROM accounts a JOIN customers c ON a.customer_id = c.customer_id WHERE c.name = 'Alice Gupta';"
    },
    {
        "nl": "Get all transactions greater than 1000",
        "sql": "SELECT tx_id, account_id, amount, tx_date, description FROM transactions WHERE amount > 1000;"
    }
]

def build_prompt(nl_query: str, schema_text: str, examples: List[dict]=FEW_SHOT_EXAMPLES) -> str:
    examples_text = ""
    for ex in examples:
        examples_text += f"\nNL: {ex['nl']}\nSQL: {ex['sql']}\n---\n"
    prompt = f"""
You are a SQL generation assistant for a SQLite banking database.
Only output a single SAFE SQL SELECT statement (ending with a semicolon) or the single word CANNOT_ANSWER.
Use the schema below to determine table/column names. Do not invent columns or tables.

Schema:
{schema_text}

Examples (do not re-explain):{examples_text}

Natural language request:
{nl_query}

Rules:
- Return only a single SELECT statement with a trailing semicolon, or CANNOT_ANSWER.
- Do NOT return INSERT/UPDATE/DELETE/PRAGMA or multiple statements.
- If the request cannot be answered with the provided schema, return CANNOT_ANSWER.
"""
    return prompt.strip()

def sanitize_sql_text(text: str) -> str:
    text = re.sub(r"```(?:sql)?", "", text, flags=re.IGNORECASE).strip()
    if ";" in text:
        text = text.split(";")[0].strip() + ";"
    return text

def generate_sql_from_nl(nl_query: str, schema_text: str, openai_api_key: str=None, model: str="gpt-4o") -> str:
    client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY or pass key.")

    prompt = build_prompt(nl_query, schema_text)

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You convert natural language to SQL. Be precise, safe and concise."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.0,
    )

    text = resp.choices[0].message.content.strip()
    text = sanitize_sql_text(text)

    if not re.match(r"^\s*SELECT\b", text, flags=re.IGNORECASE):
        if text.strip().upper().startswith("CANNOT_ANSWER"):
            return "CANNOT_ANSWER"
        raise ValueError("Generated SQL is not a SELECT statement. Generated: " + text[:200])

    return text
