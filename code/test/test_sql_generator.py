
import os
import pytest
from code.src.sql_generator import generate_sql_from_nl

class DummyResp:
    def __init__(self, content):
        self.choices = [{'message': {'content': content}}]

def dummy_create(*args, **kwargs):
    return {'choices':[{'message':{'content': 'SELECT name FROM customers WHERE city = "Hyderabad";'}}]}

def test_generate_sql_select(monkeypatch):
    # monkeypatch openai.ChatCompletion.create to return a predictable SQL
    import openai
    monkeypatch.setattr(openai.ChatCompletion, 'create', lambda *a, **k: dummy_create())
    sql = generate_sql_from_nl('customers in Hyderabad', 'schema text', openai_api_key='DUMMY')
    assert sql.strip().upper().startswith('SELECT')
