
import streamlit as st
from nl2sql_agent import handle_nl_request, get_schema_text
import os

st.set_page_config(page_title="NL2SQL Demo", layout="wide")
st.title("NL2SQL — Natural Language to SQL (SQLite)")
st.markdown("Enter a natural language question about the banking sample database and get a generated SQL + results.")

api_key = st.text_input("OpenAI API Key (or set OPENAI_API_KEY env var):", type="password")
model = st.selectbox("Model", options=["gpt-4o","gpt-4","gpt-4o-mini","gpt-3.5-turbo"], index=0)
nl = st.text_area("Natural language query", height=120, value="Show me all transactions for Alice Gupta")
run = st.button("Generate & Execute")

if run:
    key_to_use = api_key if api_key.strip() else os.getenv('OPENAI_API_KEY')
    if not key_to_use:
        st.error("OpenAI API key required (provide it above or set OPENAI_API_KEY).")
    else:
        with st.spinner("Generating SQL..."):
            try:
                out = handle_nl_request(nl, openai_api_key=key_to_use, model=model)
                if out['sql']:
                    st.subheader("Generated SQL")
                    st.code(out['sql'])
                    st.subheader("Results")
                    import pandas as pd
                    df = pd.DataFrame(out['result'])
                    st.dataframe(df)
                else:
                    st.warning(out['message'])
            except Exception as e:
                st.exception(e)
st.sidebar.header("Schema (for prompt)")
st.sidebar.code(get_schema_text())
