
# NL2SQL Test Report

## Unit Tests
- `test_sql_generator.py`: tests that sql_generator returns SELECT queries using a monkeypatched OpenAI response.
- `test_agent.py`: tests agent flow with a mocked generator to ensure DB integration and results format.

## Coverage Notes
- Aim: >60% coverage; current tests are minimal and intended to be extended.

## How to run tests
```bash
pip install -r code/src/requirements.txt
pytest code/test -q
```

## Test Results (example)
- test_sql_generator.py — PASS
- test_agent.py — PASS

