# 📊 Proof-Carrying Data Analyst

**HNX26PSI08 — Agentic GenAI + Data Analytics + Verification**

A Streamlit app where every numerical answer must come with executable "proof" code. If the underlying data is unreliable, the agent refuses to guess rather than fabricate a number.

## What it does

- Loads three small in-memory datasets: **customers**, **orders**, **products**
- Runs an automatic **data quality check** (missing values, duplicate order rows, mixed currencies)
- Answers a small set of questions by generating Python "proof" code, executing it, and verifying the result before showing it
- **Refuses** questions the data can't reliably answer (e.g. total sales when both INR and USD are present with no exchange rate)

## Example questions

1. What are the sales in Chennai? → ₹10,000
2. What is the highest sale? → ₹7,000
3. How many customers are there? → 5
4. What are the total sales? → **Refused** (mixed INR/USD, no exchange rate)

## How it works

1. The user's question is matched against known, validated query patterns.
2. A block of proof code is generated for that pattern.
3. The code is executed against the real DataFrames.
4. The output is checked against the expected value. Only if it matches is the answer marked **VERIFIED**.
5. If no pattern matches, the agent returns **REFUSED** with a reason.

## Files

| File | Purpose |
|------|---------|
| `app.py` | The Streamlit application |
| `requirements.txt` | Dependencies (`streamlit`, `pandas`) |

## Run locally

```bash  
pip install -r requirements.txt  
streamlit run app.py  
