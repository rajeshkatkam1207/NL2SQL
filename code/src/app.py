# code/src/app.py
import os
import signal
import streamlit as st
import pandas as pd

# --- Windows fix: provide SIGALRM fallback so libs that reference it don't crash
if not hasattr(signal, "SIGALRM"):
    signal.SIGALRM = getattr(signal, "SIGBREAK", 1)

st.set_page_config(page_title="NL2SQL Demo", layout="wide")
st.title("NL2SQL — Natural Language to SQL (SQLite)")
st.markdown("Enter a natural language question about the banking sample database and get a generated SQL + results.")

# ---------- UI (render first, no heavy work) ----------
api_key = st.text_input("🔑 OpenAI/Gemini API Key (or set env var):", type="password")
model = st.selectbox(
    "🤖 Model",
    ["gpt-4o", "gpt-4", "gpt-4o-mini", "gpt-3.5-turbo", "gemini-1.5-flash", "gemini-1.5-pro"],
    index=0,
)
nl = st.text_area("💬 Natural language query", height=120, value="")

left, right = st.columns([1,1])
with right:
    force_rebuild = st.checkbox("Force rebuild DB (use if locked)", value=False)

# Sidebar schema preview (best effort; don't fail page if unavailable)
schema_text = None
try:
    from nl2sql_agent import get_schema_text  # lightweight
    schema_text = get_schema_text()
except Exception as e:
    st.sidebar.warning(f"Schema preview unavailable: {e}")
else:
    st.sidebar.header("📂 Schema (for prompt)")
    st.sidebar.code(schema_text)

# Optional: reset DB now
if st.sidebar.button("🔄 Reset Database Now"):
    try:
        from db import init_db
        init_db(force=True)
        st.sidebar.success("Database reset successfully.")
    except Exception as e:
        st.sidebar.error(f"Reset failed: {e}")

# ---------- Action ----------
if st.button("🚀 Generate & Execute"):
    key_to_use = (api_key or "").strip() or os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key_to_use:
        st.error("❌ API key required (provide above or set OPENAI_API_KEY / GEMINI_API_KEY).")
    else:
        try:
            # Import here so early import errors don't blank the page
            from db import init_db
            from nl2sql_agent import handle_nl_request

            # Build DB only when needed; force if user asked (fixes WinError 32)
            init_db(force=force_rebuild)

            with st.spinner("⏳ Generating SQL..."):
                out = handle_nl_request(nl, api_key=key_to_use, model=model)

            if out.get("sql"):
                st.subheader("📜 Generated SQL")
                st.code(out["sql"])
                st.subheader("📊 Results")
                df = pd.DataFrame(out.get("result", []))
                st.dataframe(df) if not df.empty else st.info("Query executed but returned no rows.")
            else:
                st.warning(out.get("message", "No result"))
        except Exception as e:
            st.error(f"❌ Error: {e}")
