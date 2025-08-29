from db import run_query, init_db
from sql_generator import generate_sql_from_nl, build_prompt
from pathlib import Path

SCHEMA_FILE = Path(__file__).parent / "sample_data.sql"

def get_schema_text():
    return SCHEMA_FILE.read_text()

def handle_nl_request(nl_text, openai_api_key=None, model="gpt-4o", use_langchain=False):
    init_db(force=False)
    schema = get_schema_text()

    # Case 1: no API key → use mock
    if not openai_api_key:
        return mock_fallback(nl_text)

    try:
        sql = generate_sql_from_nl(nl_text, schema, openai_api_key=openai_api_key, model=model)
    except Exception as e:
        # Case 2: API key invalid or quota exceeded → use mock
        return mock_fallback(nl_text)

    if sql == "CANNOT_ANSWER":
        return {"sql": None, "result": [], "message": "Cannot answer based on available schema."}

    results = run_query(sql)
    return {"sql": sql, "result": results, "message": "OK"}


def mock_fallback(nl_text: str):
    """Return mock SQL + dummy results based on simple keyword rules."""
    nl_lower = nl_text.lower()

    if "transaction" in nl_lower or "transactions" in nl_lower:
        return {
            "sql": "SELECT tx_id, account_id, amount, tx_date, description FROM transactions WHERE account_id = 1;",
            "result": [
                {"tx_id": 101, "account_id": 1, "amount": 5000, "tx_date": "2025-08-01", "description": "Salary credit"},
                {"tx_id": 102, "account_id": 1, "amount": -1500, "tx_date": "2025-08-05", "description": "ATM withdrawal"},
            ],
            "message": "⚠️ Mock mode: showing fake transactions (quota exceeded or no key)."
        }

    elif "balance" in nl_lower:
        return {
            "sql": "SELECT account_id, balance FROM accounts WHERE customer_id = 1;",
            "result": [
                {"account_id": 1, "balance": 12000.50},
            ],
            "message": "⚠️ Mock mode: showing fake balances."
        }

    else:
        return {
            "sql": "SELECT customer_id, name, city FROM customers;",
            "result": [
                {"customer_id": 1, "name": "Alice Gupta", "city": "Hyderabad"},
                {"customer_id": 2, "name": "Ramesh Kumar", "city": "Mumbai"},
            ],
            "message": "⚠️ Mock mode: showing fake customers."
        }
