import os
import pandas as pd
from pathlib import Path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from nl2sql_agent import handle_nl_request

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = PROJECT_ROOT.parent  # go one level up → .../NL2SQL_full
XLS_FILE = Path("TestCases.xlsx")   # Your Excel file with 2 columns: id, nl_query
REPORT_FILE = PROJECT_ROOT / "artifacts" / "arch" / "testreport.md"
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

def run_tests():
    # Load Excel
    df = pd.read_excel(XLS_FILE)
    results = []

    api_key = "AIzaSyAXckDDt5tjw0cMoXYUB8WkZpU8YDSFkqk"
    if not api_key:
        raise ValueError("No API key found. Please set OPENAI_API_KEY or GEMINI_API_KEY in environment.")

    for _, row in df.iterrows():
        case_id = row["Test Case ID"]
        nl = row["Natural Language Query"]

        try:
            # Pick model depending on API key type
            if api_key.startswith("AIza"):  
                model = "gemini-1.5-flash"   # Gemini
            else:
             model = "gpt-4o"             # OpenAI
            out = handle_nl_request(nl, api_key=api_key, model=model)
            sql = out.get("sql", "")
            res = out.get("result", [])
            message = out.get("message", "")

            # 🚨 Cleanup Gemini/OpenAI output if it contains code fences
            if sql.startswith("```"):
                sql = sql.strip("`").replace("sql", "", 1).strip()

            results.append((case_id, nl, sql, len(res), message, "PASS"))

        except Exception as e:
            results.append((case_id, nl, str(e), 0, "Exception", "FAIL"))

    # Write report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# NL2SQL Test Report\n\n")
        f.write("| ID | Query | Generated SQL | Rows Returned | Message | Status |\n")
        f.write("|----|-------|---------------|---------------|---------|--------|\n")
        for r in results:
            f.write(f"| {r[0]} | {r[1]} | `{r[2]}` | {r[3]} | {r[4]} | {r[5]} |\n")

if __name__ == "__main__":
    run_tests()
    print(f"✅ Test report written to {REPORT_FILE}")
