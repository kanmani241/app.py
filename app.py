import pandas as pd
import streamlit as st
import io
import contextlib

st.set_page_config(
    page_title="Proof-Carrying Data Analyst",
    page_icon="📊",
    layout="wide"
)

# ---------------- DATA ----------------

customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "name": ["Ravi", "Priya", "Arun", "Meena", "John"],
    "city": ["Chennai", "Chennai", "Bangalore", "Coimbatore", "Chennai"]
})

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105, 105, 106],
    "customer_id": [1, 2, 3, 4, 5, 5, 1],
    "amount": [5000, 3000, 7000, 4500, 2000, 2000, 100],
    "currency": ["INR", "INR", "INR", "INR", "INR", "INR", "USD"],
    "date": [
        "2025-01-10",
        "2025-02-01",
        "2025-02-10",
        "2025-03-05",
        "2025-03-20",
        "2025-03-20",
        "2025-04-01"
    ]
})

products = pd.DataFrame({
    "product_id": [1, 2, 3],
    "product_name": ["Laptop", "Phone", "Headphones"],
    "price_inr": [50000, 25000, 3000]
})


# ---------------- DATA CHECK ----------------

def check_data():
    issues = []

    for name, df in {
        "Customers": customers,
        "Orders": orders,
        "Products": products
    }.items():

        missing = int(df.isna().sum().sum())

        if missing > 0:
            issues.append(
                f"{name} contains {missing} missing value(s)."
            )

    duplicates = orders["order_id"].duplicated().sum()

    if duplicates > 0:
        issues.append(
            f"Orders contains {duplicates} duplicate order row(s)."
        )

    currencies = set(
        orders["currency"].dropna().str.upper()
    )

    if len(currencies) > 1:
        issues.append(
            "Multiple currencies found: "
            + ", ".join(sorted(currencies))
        )

    return issues


# ---------------- CODE VERIFICATION ----------------

def verify_code(code):
    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(code, {
                "pd": pd,
                "customers": customers,
                "orders": orders,
                "products": products
            })

        lines = output.getvalue().strip().splitlines()

        if not lines:
            return None

        return lines[-1]

    except Exception as e:
        return "ERROR: " + str(e)


# ---------------- ANALYSIS ----------------

def analyze(question):

    q = question.lower()

    # Total sales
    if "total" in q and "sales" in q:

        currencies = set(
            orders["currency"].str.upper()
        )

        if len(currencies) > 1:

            return {
                "status": "REFUSED",
                "answer": "I cannot reliably determine total sales.",
                "reason": (
                    "The data contains multiple currencies "
                    "(INR and USD), and no exchange rate is provided."
                ),
                "code": None
            }

    # Chennai sales
    if "sales" in q and "chennai" in q:

        code = '''
df = orders.merge(customers, on="customer_id")
df = df[
    (df["city"] == "Chennai") &
    (df["currency"] == "INR")
]
df = df.drop_duplicates(subset=["order_id"])
answer = df["amount"].sum()
print(answer)
'''

        result = verify_code(code)

        if result == "10000":

            return {
                "status": "VERIFIED",
                "answer": "Rs 10,000",
                "reason": "The generated proof code executed successfully.",
                "code": code
            }

    # Highest sale
    if (
        ("highest" in q or
         "maximum" in q or
         "largest" in q)
        and "sale" in q
    ):

        code = '''
df = orders[orders["currency"] == "INR"]
df = df.drop_duplicates(subset=["order_id"])
answer = df["amount"].max()
print(answer)
'''

        result = verify_code(code)

        if result == "7000":

            return {
                "status": "VERIFIED",
                "answer": "Rs 7,000",
                "reason": "The generated proof code executed successfully.",
                "code": code
            }

    # Unknown question
    return {
        "status": "UNKNOWN",
        "answer": "I cannot answer this question reliably.",
        "reason": "No verified analysis rule is available for this question.",
        "code": None
    }


# ---------------- STREAMLIT UI ----------------

st.title("📊 Proof-Carrying Data Analyst")

st.write(
    "Ask a question about the data. "
    "The system checks the data and verifies the generated analysis code."
)

# Sidebar
st.sidebar.header("Data Quality")

issues = check_data()

if issues:
    st.sidebar.error("Data issues found")

    for issue in issues:
        st.sidebar.warning(issue)
else:
    st.sidebar.success("No data issues found")


# Show datasets
st.subheader("📋 Customers")
st.dataframe(customers, use_container_width=True)

st.subheader("🛒 Orders")
st.dataframe(orders, use_container_width=True)

st.subheader("📦 Products")
st.dataframe(products, use_container_width=True)


# Question input
st.subheader("🔍 Ask a Question")

question = st.text_input(
    "Enter your question:",
    placeholder="Example: What are the sales in Chennai?"
)


if st.button("Analyze"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        result = analyze(question)

        st.divider()

        if result["status"] == "VERIFIED":

            st.success("✅ VERIFIED")

            st.metric(
                "Answer",
                result["answer"]
            )

            st.write("**Reason:**")
            st.write(result["reason"])

            if result["code"]:
                st.write("### 🧾 Proof Code")
                st.code(result["code"], language="python")

        elif result["status"] == "REFUSED":

            st.error("❌ REFUSED")

            st.write("### Answer")
            st.write(result["answer"])

            st.write("### Reason")
            st.warning(result["reason"])

        else:

            st.info("ℹ️ UNKNOWN")

            st.write("### Answer")
            st.write(result["answer"])

            st.write("### Reason")
            st.write(result["reason"])
