
from db import run_query, init_db
from sql_generator import generate_sql_from_nl, build_prompt
from pathlib import Path

SCHEMA_FILE = Path(__file__).parent / 'sample_data.sql'
def get_schema_text():
    return SCHEMA_FILE.read_text()

def handle_nl_request(nl_text, openai_api_key=None, model='gpt-4o', max_clarify=1, use_langchain=False):
    """Process a natural language request. Attempts generation and, if the model indicates ambiguity,
    returns a clarification prompt to the user (simple approach). Optionally, create a LangChain conversational agent
    for multi-turn clarifications if requested and available.
    """
    init_db(force=False)
    schema = get_schema_text()

    # If user requests langchain usage, try to create an agent
    if use_langchain:
        try:
            from .langchain_agent import create_conversational_agent, ask_agent, is_langchain_available  # type: ignore
        except Exception:
            # fallback to basic flow
            use_langchain = False

    # Attempt generation
    sql = generate_sql_from_nl(nl_text, schema, openai_api_key=openai_api_key, model=model)
    if sql == 'CANNOT_ANSWER':
        return {'sql': None, 'result': [], 'message': 'Cannot answer based on available schema.'}

    # Execute SQL and return results
    results = run_query(sql)
    # If results are empty, optionally try one clarification round
    if len(results) == 0 and max_clarify > 0:
        # Simple clarification strategy: ask the user if they meant a different timeframe or field
        clarification = 'The generated query returned no rows. Do you want to (A) broaden the filters, (B) check a different field, or (C) cancel?'
        return {'sql': sql, 'result': results, 'message': 'NO_RESULTS_CLARIFICATION', 'clarification': clarification}

    return {'sql': sql, 'result': results, 'message': 'OK'}
