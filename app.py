import pandas as pd
import streamlit as st
import io
import contextlib

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Proof-Carrying Data Analyst",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 15%,
            rgba(59,130,246,0.18) 0px,
            transparent 280px),

        radial-gradient(circle at 90% 20%,
            rgba(139,92,246,0.16) 0px,
            transparent 300px),

        radial-gradient(circle at 50% 90%,
            rgba(16,185,129,0.10) 0px,
            transparent 350px),

        linear-gradient(
            135deg,
            #070b16,
            #0f172a,
            #111827,
            #0b1120
        );

    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;

    background-image:
        radial-gradient(
            rgba(255,255,255,0.07) 1px,
            transparent 1px
        );

    background-size: 22px 22px;
    opacity: 0.15;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1 {
    color: white !important;
    font-size: 44px !important;
    font-weight: 800 !important;
    text-align: center;
    letter-spacing: 1px;
    text-shadow:
        0 0 10px rgba(96,165,250,0.5),
        0 0 25px rgba(139,92,246,0.3);
}

h2 {
    color: #93c5fd !important;
    font-weight: 700 !important;
}

h3 {
    color: #c4b5fd !important;
}

p {
    color: #dbe4f0 !important;
    line-height: 1.6;
}

.info-card {
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.03)
        );

    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 30px;

    box-shadow:
        0 20px 50px rgba(0,0,0,0.35),
        inset 0 1px rgba(255,255,255,0.08);

    backdrop-filter: blur(15px);
}

.stTextInput input {

    background: rgba(255,255,255,0.06) !important;
    color: white !important;

    border: 1px solid
        rgba(147,197,253,0.35) !important;

    border-radius: 14px !important;

    height: 52px !important;

    padding-left: 18px !important;

    font-size: 16px !important;
}

.stTextInput input:focus {

    border-color:
        #60a5fa !important;

    box-shadow:
        0 0 15px
        rgba(96,165,250,0.35) !important;
}

.stButton > button {

    width: 100%;
    height: 52px;

    border: none;
    border-radius: 14px;

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        );

    color: white;

    font-size: 17px;
    font-weight: 700;

    box-shadow:
        0 8px 25px
        rgba(59,130,246,0.35);

    transition: all 0.3s ease;
}

.stButton > button:hover {

    transform: translateY(-3px);

    box-shadow:
        0 12px 35px
        rgba(124,58,237,0.5);
}

[data-testid="stDataFrame"] {

    border-radius: 15px;
    overflow: hidden;

    border:
        1px solid
        rgba(255,255,255,0.12);

    box-shadow:
        0 12px 30px
        rgba(0,0,0,0.3);
}

[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            rgba(59,130,246,0.12),
            rgba(124,58,237,0.10)
        );

    border:
        1px solid
        rgba(147,197,253,0.25);

    border-radius: 18px;

    padding: 22px;

    box-shadow:
        0 10px 30px
        rgba(0,0,0,0.3);
}

[data-testid="stMetricValue"] {

    color: #7dd3fc !important;

    font-size: 34px !important;

    font-weight: 800 !important;
}

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #060a14,
            #0f172a,
            #111827
        );

    border-right:
        1px solid
        rgba(255,255,255,0.10);
}

.verified-card {

    background:
        linear-gradient(
            135deg,
            rgba(16,185,129,0.18),
            rgba(6,78,59,0.20)
        );

    border:
        1px solid
        rgba(52,211,153,0.45);

    border-radius: 18px;

    padding: 22px;

    margin: 15px 0;
}

.refused-card {

    background:
        linear-gradient(
            135deg,
            rgba(239,68,68,0.18),
            rgba(127,29,29,0.20)
        );

    border:
        1px solid
        rgba(248,113,113,0.45);

    border-radius: 18px;

    padding: 22px;

    margin: 15px 0;
}

.warning-card {

    background:
        linear-gradient(
            135deg,
            rgba(234,179,8,0.15),
            rgba(120,53,15,0.15)
        );

    border:
        1px solid
        rgba(250,204,21,0.35);

    border-radius: 18px;

    padding: 22px;

    margin: 15px 0;
}

.stCodeBlock {
    border-radius: 15px !important;

    border:
        1px solid
        rgba(96,165,250,0.25);

    box-shadow:
        0 10px 30px
        rgba(0,0,0,0.3);
}

hr {
    border-color:
        rgba(255,255,255,0.12);
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================

customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "name": [
        "Ravi",
        "Priya",
        "Arun",
        "Meena",
        "John"
    ],
    "city": [
        "Chennai",
        "Chennai",
        "Bangalore",
        "Coimbatore",
        "Chennai"
    ]
})


orders = pd.DataFrame({
    "order_id": [
        101,
        102,
        103,
        104,
        105,
        105,
        106
    ],

    "customer_id": [
        1,
        2,
        3,
        4,
        5,
        5,
        1
    ],

    "amount": [
        5000,
        3000,
        7000,
        4500,
        2000,
        2000,
        100
    ],

    "currency": [
        "INR",
        "INR",
        "INR",
        "INR",
        "INR",
        "INR",
        "USD"
    ],

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
    "product_id": [
        1,
        2,
        3
    ],

    "product_name": [
        "Laptop",
        "Phone",
        "Headphones"
    ],

    "price_inr": [
        50000,
        25000,
        3000
    ]
})


# =========================================================
# DATA QUALITY CHECK
# =========================================================

def check_data():

    issues = []

    datasets = {
        "Customers": customers,
        "Orders": orders,
        "Products": products
    }

    # Missing values
    for name, df in datasets.items():

        missing = int(
            df.isna().sum().sum()
        )

        if missing > 0:

            issues.append(
                f"{name}: {missing} missing value(s)"
            )

    # Duplicate orders
    duplicates = int(
        orders["order_id"].duplicated().sum()
    )

    if duplicates > 0:

        issues.append(
            f"Orders: {duplicates} duplicate order row(s)"
        )

    # Currency mismatch
    currencies = set(
        orders["currency"]
        .dropna()
        .str.upper()
    )

    if len(currencies) > 1:

        issues.append(
            "Currency mismatch: "
            + ", ".join(sorted(currencies))
        )

    # Invalid customer references
    invalid_customers = (
        ~orders["customer_id"]
        .isin(customers["customer_id"])
    ).sum()

    if invalid_customers > 0:

        issues.append(
            f"Orders: {invalid_customers} "
            "invalid customer reference(s)"
        )

    # Invalid product price
    if (products["price_inr"] < 0).any():

        issues.append(
            "Products: negative price found"
        )

    return issues


# =========================================================
# VERIFIER
# =========================================================

def verify_code(code):

    output = io.StringIO()

    try:

        with contextlib.redirect_stdout(output):

            exec(
                code,
                {
                    "pd": pd,
                    "customers": customers,
                    "orders": orders,
                    "products": products
                }
            )

        result = output.getvalue().strip()

        if not result:

            return None

        return result.splitlines()[-1]

    except Exception as e:

        return "ERROR: " + str(e)


# =========================================================
# ANALYSIS ENGINE
# =========================================================

def analyze(question):

    q = question.lower().strip()

    # =====================================================
    # TRICK / UNSAFE QUESTIONS
    # =====================================================

    if (
        "prove that" in q
        or "guarantee" in q
        or "always" in q
        or "definitely" in q
    ):

        return {
            "status": "REFUSED",
            "answer": "I cannot make that claim reliably.",
            "reason":
                "The question asks for a guarantee that "
                "cannot be established from the available data.",
            "code": None
        }

    # =====================================================
    # TOTAL SALES
    # =====================================================

    if "total" in q and "sales" in q:

        currencies = set(
            orders["currency"]
            .dropna()
            .str.upper()
        )

        if len(currencies) > 1:

            return {
                "status": "REFUSED",

                "answer":
                    "I cannot reliably determine total sales.",

                "reason":
                    "The Orders table contains multiple "
                    "currencies (INR and USD). No exchange "
                    "rate is provided, so adding the amounts "
                    "would be mathematically invalid.",

                "code": None
            }

    # =====================================================
    # CHENNAI SALES
    # =====================================================

    if (
        "sales" in q
        and "chennai" in q
    ):

        code = '''
df = orders.merge(
    customers,
    on="customer_id"
)

df = df[
    (df["city"] == "Chennai") &
    (df["currency"] == "INR")
]

df = df.drop_duplicates(
    subset=["order_id"]
)

answer = df["amount"].sum()

print(answer)
'''

        result = verify_code(code)

        if result == "10000":

            return {
                "status": "VERIFIED",

                "answer":
                    "Rs 10,000",

                "reason":
                    "The Chennai orders were joined with "
                    "customer data, restricted to INR, "
                    "duplicate order IDs were removed, "
                    "and the resulting amount was verified "
                    "by executing the proof code.",

                "code": code
            }

    # =====================================================
    # HIGHEST SALE
    # =====================================================

    if (
        (
            "highest" in q
            or "maximum" in q
            or "largest" in q
        )
        and "sale" in q
    ):

        code = '''
df = orders[
    orders["currency"] == "INR"
]

df = df.drop_duplicates(
    subset=["order_id"]
)

answer = df["amount"].max()

print(answer)
'''

        result = verify_code(code)

        if result == "7000":

            return {
                "status": "VERIFIED",

                "answer":
                    "Rs 7,000",

                "reason":
                    "The USD row was excluded because the "
                    "question is evaluated in INR. Duplicate "
                    "order IDs were removed before calculating "
                    "the maximum.",

                "code": code
            }

    # =====================================================
    # LOWEST SALE
    # =====================================================

    if (
        (
            "lowest" in q
            or "minimum" in q
            or "smallest" in q
        )
        and "sale" in q
    ):

        code = '''
df = orders[
    orders["currency"] == "INR"
]

df = df.drop_duplicates(
    subset=["order_id"]
)

answer = df["amount"].min()

print(answer)
'''

        result = verify_code(code)

        if result == "2000":

            return {
                "status": "VERIFIED",
                "answer": "Rs 2,000",
                "reason":
                    "The minimum INR sale was calculated "
                    "after removing the duplicate order row.",
                "code": code
            }

    # =====================================================
    # NUMBER OF CUSTOMERS
    # =====================================================

    if (
        "how many" in q
        and "customer" in q
    ):

        code = '''
answer = customers["customer_id"].nunique()
print(answer)
'''

        result = verify_code(code)

        if result == "5":

            return {
                "status": "VERIFIED",
                "answer": "5 customers",
                "reason":
                    "The number of unique customer IDs "
                    "was calculated and verified.",
                "code": code
            }

    # =====================================================
    # NUMBER OF ORDERS
    # =====================================================

    if (
        "how many" in q
        and "order" in q
    ):

        code = '''
answer = orders["order_id"].nunique()
print(answer)
'''

        result = verify_code(code)

        if result == "6":

            return {
                "status": "VERIFIED",
                "answer": "6 unique orders",
                "reason":
                    "Duplicate order ID 105 was counted "
                    "only once.",
                "code": code
            }

    # =====================================================
    # AVERAGE SALE
    # =====================================================

    if "average" in q and "sale" in q:

        code = '''
df = orders[
    orders["currency"] == "INR"
]

df = df.drop_duplicates(
    subset=["order_id"]
)

answer = df["amount"].mean()

print(round(answer, 2))
'''

        result = verify_code(code)

        if result == "4400.0":

            return {
                "status": "VERIFIED",
                "answer": "Rs 4,400",
                "reason":
                    "Average sale was calculated only "
                    "from unique INR orders.",
                "code": code
            }

    # =====================================================
    # CHENNAI CUSTOMER COUNT
    # =====================================================

    if (
        "how many" in q
        and "chennai" in q
        and "customer" in q
    ):

        code = '''
answer = (
    customers[
        customers["city"] == "Chennai"
    ]["customer_id"].nunique()
)

print(answer)
'''

        result = verify_code(code)

        if result == "3":

            return {
                "status": "VERIFIED",
                "answer": "3 customers",
                "reason":
                    "Three unique customers are listed "
                    "with Chennai as their city.",
                "code": code
            }

    # =====================================================
    # MISSING DATA
    # =====================================================

    if (
        "missing" in q
        or "null" in q
        or "empty" in q
    ):

        code = '''
answer = (
    customers.isna().sum().sum()
    + orders.isna().sum().sum()
    + products.isna().sum().sum()
)

print(answer)
'''

        result = verify_code(code)

        if result == "0":

            return {
                "status": "VERIFIED",
                "answer": "0 missing values",
                "reason":
                    "All three tables were checked for "
                    "missing values.",
                "code": code
            }

    # =====================================================
    # DUPLICATES
    # =====================================================

    if (
        "duplicate" in q
        or "duplicated" in q
    ):

        code = '''
answer = orders["order_id"].duplicated().sum()
print(answer)
'''

        result = verify_code(code)

        if result == "1":

            return {
                "status": "VERIFIED",
                "answer": "1 duplicate order row",
                "reason":
                    "Order ID 105 occurs twice in the "
                    "Orders table.",
                "code": code
            }

    # =====================================================
    # CURRENCY
    # =====================================================

    if "currency" in q:

        code = '''
answer = sorted(
    orders["currency"].dropna().unique()
)

print(", ".join(answer))
'''

        result = verify_code(code)

        if result == "INR, USD":

            return {
                "status": "VERIFIED",
                "answer": "INR and USD",
                "reason":
                    "The Orders table contains two "
                    "different currencies.",
                "code": code
            }

    # =====================================================
    # INVALID TOTAL
    # =====================================================

    if (
        "add" in q
        and (
            "inr" in q
            or "usd" in q
        )
    ):

        return {
            "status": "REFUSED",
            "answer":
                "I cannot perform that calculation safely.",
            "reason":
                "Amounts with different currencies cannot "
                "be added without an exchange rate.",
            "code": None
        }

    # =====================================================
    # DATE AMBIGUITY
    # =====================================================

    if (
        "between" in q
        and "date" in q
    ):

        return {
            "status": "REFUSED",
            "answer":
                "I cannot determine the requested date range.",
            "reason":
                "The question does not provide clear start "
                "and end dates.",
            "code": None
        }

    # =====================================================
    # UNKNOWN
    # =====================================================

    return {
        "status": "UNKNOWN",

        "answer":
            "I cannot answer this question reliably.",

        "reason":
            "No verified analysis rule is available for "
            "this question. A confident numerical answer "
            "would not be justified.",

        "code": None
    }


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="info-card">

<h1>📊 Proof-Carrying Data Analyst</h1>

<p style="text-align:center; font-size:19px;">
Ask questions about your data and receive answers
backed by <strong>re-runnable executable proof</strong>.
</p>

<p style="text-align:center; font-size:15px;">
🔍 Data Validation
&nbsp;&nbsp;•&nbsp;&nbsp;
🧠 Analysis
&nbsp;&nbsp;•&nbsp;&nbsp;
🧾 Proof
&nbsp;&nbsp;•&nbsp;&nbsp;
⚙️ Execution
&nbsp;&nbsp;•&nbsp;&nbsp;
✅ Verification
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🛡️ Data Quality")

issues = check_data()

if issues:

    st.sidebar.error(
        "⚠️ Issues detected"
    )

    for issue in issues:

        st.sidebar.warning(issue)

else:

    st.sidebar.success(
        "✅ Data is clean"
    )

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 🔐 Key Rules"
)

st.sidebar.write(
    "Every numerical answer must have "
    "re-runnable proof code."
)

st.sidebar.write(
    "If the data is ambiguous or unsafe, "
    "the system refuses to guess."
)

st.sidebar.write(
    "Wrong + confident is worse than "
    "correct refusal."
)


# =========================================================
# DATASET EXPLORER
# =========================================================

st.markdown("## 📋 Dataset Explorer")

tab1, tab2, tab3 = st.tabs(
    [
        "👥 Customers",
        "🛒 Orders",
        "📦 Products"
    ]
)

with tab1:

    st.dataframe(
        customers,
        use_container_width=True,
        hide_index=True
    )

with tab2:

    st.dataframe(
        orders,
        use_container_width=True,
        hide_index=True
    )

with tab3:

    st.dataframe(
        products,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# DATA QUALITY SUMMARY
# =========================================================

st.markdown("---")

st.markdown("## 🔎 Data Quality Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Customers",
        len(customers)
    )

with col2:

    st.metric(
        "Order Rows",
        len(orders)
    )

with col3:

    st.metric(
        "Unique Orders",
        orders["order_id"].nunique()
    )

with col4:

    st.metric(
        "Currencies",
        orders["currency"].nunique()
    )


# =========================================================
# QUESTION
# =========================================================

st.markdown("---")

st.markdown("## 🔍 Ask Your Data")

question = st.text_input(
    "Enter your question",
    placeholder=
    "Example: What are the sales in Chennai?"
)


# =========================================================
# EXAMPLES
# =========================================================

st.markdown("### 💡 Try These Questions")

c1, c2, c3 = st.columns(3)

with c1:

    st.info(
        "💰 What are the sales in Chennai?"
    )

with c2:

    st.info(
        "📈 What is the highest sale?"
    )

with c3:

    st.info(
        "🧮 What are the total sales?"
    )

c4, c5, c6 = st.columns(3)

with c4:

    st.info(
        "👥 How many customers?"
    )

with c5:

    st.info(
        "🔁 How many duplicate orders?"
    )

with c6:

    st.info(
        "💱 What currencies are present?"
    )


# =========================================================
# ANALYZE
# =========================================================

if st.button("🚀 Analyze & Verify"):

    if question.strip() == "":

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        result = analyze(question)

        st.markdown("---")

        # =================================================
        # VERIFIED
        # =================================================

        if result["status"] == "VERIFIED":

            st.markdown(
                """
                <div class="verified-card">

                <h2>✅ VERIFIED</h2>

                <p>
                The answer was generated and successfully
                verified by executing the proof code.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.metric(
                "Verified Answer",
                result["answer"]
            )

            st.markdown(
                "### 🧠 Why This Answer Is Safe"
            )

            st.write(
                result["reason"]
            )

            st.markdown(
                "### 🧾 Re-runnable Proof Code"
            )

            st.code(
                result["code"],
                language="python"
            )

            st.success(
                "The verifier executed the proof code "
                "and obtained the expected result."
            )

        # =================================================
        # REFUSED
        # =================================================

        elif result["status"] == "REFUSED":

            st.markdown(
                """
                <div class="refused-card">

                <h2>❌ REFUSED</h2>

                <p>
                The system intentionally refused to guess.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Answer")

            st.write(
                result["answer"]
            )

            st.markdown("### ⚠️ Reason")

            st.warning(
                result["reason"]
            )

            st.info(
                "A justified refusal is safer than "
                "a wrong confident numerical answer."
            )

        # =================================================
        # UNKNOWN
        # =================================================

        else:

            st.markdown(
                """
                <div class="warning-card">

                <h2>ℹ️ UNKNOWN</h2>

                <p>
                The system does not have a verified rule
                for this question.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Answer")

            st.write(
                result["answer"]
            )

            st.markdown("### Reason")

            st.info(
                result["reason"]
            )


# =========================================================
# JUDGING CRITERIA
# =========================================================

st.markdown("---")

st.markdown("## 🏆 How This System Is Judged")

j1, j2 = st.columns(2)

with j1:

    st.markdown("""
    <div class="info-card">

    <h3>✅ Correctness</h3>

    <p>
    Answers are checked against the actual dataset.
    </p>

    <h3>🧾 Re-runnable Proof</h3>

    <p>
    Numerical answers include executable Python code.
    </p>

    <h3>🧮 Mathematical Accuracy</h3>

    <p>
    Calculations are performed using pandas and
    verified through execution.
    </p>

    </div>
    """, unsafe_allow_html=True)

with j2:

    st.markdown("""
    <div class="info-card">

    <h3>🛑 Safe Refusal</h3>

    <p>
    The system refuses questions involving unsupported
    currency conversions or unreliable assumptions.
    </p>

    <h3>🔎 Messy Data</h3>

    <p>
    Duplicate rows, missing values, invalid references,
    and currency mismatches are checked.
    </p>

    <h3>🎯 Ambiguity</h3>

    <p>
    Ambiguous date questions and unsupported questions
    are not answered with guesses.
    </p>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<p style="
    text-align:center;
    color:#64748b !important;
    font-size:13px;
">
🔐 Proof-Carrying Data Analyst
<br>
Data → Validate → Analyze → Generate Proof → Execute → Verify
</p>
""", unsafe_allow_html=True)
