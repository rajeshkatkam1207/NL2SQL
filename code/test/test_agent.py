
from code.src.nl2sql_agent import handle_nl_request
def test_handle_nl_request_mock(monkeypatch):
    # Mock the SQL generator to return a fixed select, then run against DB
    def fake_generate(nl, schema, openai_api_key=None, model=None):
        return 'SELECT name FROM customers WHERE city = "Hyderabad";'
    import code.src.sql_generator as gen
    monkeypatch.setattr(gen, 'generate_sql_from_nl', fake_generate)
    out = handle_nl_request('who is in Hyderabad', openai_api_key='DUMMY')
    assert out['sql'] is not None
    assert isinstance(out['result'], list)
