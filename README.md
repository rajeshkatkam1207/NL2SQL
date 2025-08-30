# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)  

---

## 🎯 Introduction
NL2SQL is a solution that translates natural language queries into SQL statements and executes them on a sample banking database.
It solves the problem of non-technical users struggling to interact with databases, by enabling them to query data in plain English instead of writing SQL.

## 🎥 Demo
NL2SQL_full\artifacts\demo)

## 💡 Inspiration
Organizations store large amounts of data in relational databases, but not everyone knows SQL.
Our inspiration was to bridge this gap using LLMs (OpenAI / Gemini) so that business users, analysts, and managers can retrieve insights without technical knowledge.

## ⚙️ What It Does
Accepts natural language questions about the database.

✅ Generates valid SQL queries using OpenAI GPT or Google Gemini.

✅ Executes the query on a local SQLite banking database.

✅ Displays results in a clean Streamlit UI.

✅ Includes automated test framework (reads test cases from Excel, validates SQL + execution, and exports Markdown test reports).

## 🛠️ How We Built It
Streamlit → UI for entering natural language queries and showing results.

LangChain + LLMs (OpenAI / Gemini) → Converting NL queries to SQL.

SQLite → Lightweight database with banking schema & sample data.

Pandas → For tabular results and test reporting.

Excel-based Test Framework → Loads test cases, executes, and writes reports to Markdown.

## 🚧 Challenges We Faced
⚠️ Model differences → Gemini and GPT sometimes return SQL in different formats.

⚠️ Handling schema mismatches and missing fields.

⚠️ Database locking issues when multiple queries ran simultaneously.

⚠️ Streamlit re-runs causing DB initialization conflicts

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/rajeshkatkam1207/NL2SQL.git
   ```
2. Install dependencies  
   ```sh
   pip install -r requirements.txt

   ```
   export OPENAI_API_KEY=your_key_here   # for OpenAI
	export GEMINI_API_KEY=your_key_here   # for Gemini

3. Run the project  
   ```sh
   streamlit run src/app.py

   ```

## 🏗️ Tech Stack
- 🔹 Frontend: Streamlitr
- 🔹 Backend: Python (LangChain, Pandaso
- 🔹 Database: SQLite (Banking schema + sample data)
- 🔹 Other: OpenAI GPT, Google Gemini

## 👥 Team
- **K Rajesh** - rajeshkatkam1207 | rajesh katkam
- **Roshan Lohkare** - roshanlohkare| Roshan Lohkare