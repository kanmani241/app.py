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

/* ---------- MAIN BACKGROUND ---------- */

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

/* ---------- TEXTURE ---------- */

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

/* ---------- MAIN CONTAINER ---------- */

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* ---------- TITLE ---------- */

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

/* ---------- NORMAL TEXT ---------- */

p {
    color: #dbe4f0 !important;
    line-height: 1.6;
}

/* ---------- HEADER CARD ---------- */

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

/* ---------- INPUT ---------- */

.stTextInput input {

    background: rgba(255,255,255,0.06) !important;

    color: white !important;

    border: 1px solid
        rgba(147,197,253,0.35) !important;

    border-radius: 14px !important;

    height: 52px !important;

    padding-left: 18px !important;

    font-size: 16px !important;

    box-shadow:
        inset 0 0 15px rgba(0,0,0,0.2);
}

.stTextInput input:focus {

    border-color:
        #60a5fa !important;

    box-shadow:
        0 0 15px
        rgba(96,165,250,0.35) !important;
}

/* ---------- BUTTON ---------- */

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

    background:
        linear-gradient(
            90deg,
            #3b82f6,
            #8b5cf6
        );
}

/* ---------- DATAFRAME ---------- */

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

/* ---------- METRIC ---------- */

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

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

[data-testid="stMetricValue"] {

    color: #7dd3fc !important;

    font-size: 34px !important;

    font-weight: 800 !important;

    text-shadow:
        0 0 15px
        rgba(125,211,252,0.35);
}

/* ---------- SIDEBAR ---------- */

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

section[data-testid="stSidebar"] h2 {

    color: #93c5fd !important;

}

/* ---------- VERIFIED CARD ---------- */

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

    box-shadow:
        0 10px 30px
        rgba(16,185,129,0.15);
}

/* ---------- REFUSED CARD ---------- */

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

    box-shadow:
        0 10px 30px
        rgba(239,68,68,0.15);
}

/* ---------- UNKNOWN CARD ---------- */

.unknown-card {

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

/* ---------- CODE ---------- */

.stCodeBlock {

    border-radius: 15px !important;

    border:
        1px solid
        rgba(96,165,250,0.25);

    box-shadow:
        0 10px 30px
        rgba(0,0,0,0.3);
}

/* ---------- DIVIDER ---------- */

hr {

    border-color:
        rgba(255,255,255,0.12);

}

/* ---------- ALERTS ---------- */

div[data-testid="stAlert"] {

    border-radius: 14px;

}

/* ---------- SMALL ANIMATION ---------- */

.stButton > button,
.stTextInput input,
.info-card,
.verified-card,
.refused-card {

    transition:
        all 0.3s ease;

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
        101, 102, 103, 104,
        105, 105, 106
    ],

    "customer_id": [
        1, 2, 3, 4,
        5, 5, 1
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
# DATA CHECK
# =========================================================

def check_data():

    issues = []

    datasets = {
        "Customers": customers,
        "Orders": orders,
        "Products": products
    }

    for name, df in datasets.items():

        missing = int(
            df.isna().sum().sum()
        )

        if missing > 0:

            issues.append(
                f"{name} contains "
                f"{missing} missing value(s)."
            )

    duplicates = int(
        orders["order_id"].duplicated().sum()
    )

    if duplicates > 0:

        issues.append(
            f"Orders contains "
            f"{duplicates} duplicate order row(s)."
        )

    currencies = set(
        orders["currency"]
        .dropna()
        .str.upper()
    )

    if len(currencies) > 1:

        issues.append(
            "Multiple currencies found: "
            + ", ".join(
                sorted(currencies)
            )
        )

    return issues


# =========================================================
# VERIFY CODE
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

        lines = (
            output
            .getvalue()
            .strip()
            .splitlines()
        )

        if not lines:
            return None

        return lines[-1]

    except Exception as e:

        return "ERROR: " + str(e)


# =========================================================
# ANALYZE QUESTION
# =========================================================

def analyze(question):

    q = question.lower().strip()

    # -----------------------------------------------------
    # TOTAL SALES
    # -----------------------------------------------------

    if "total" in q and "sales" in q:

        currencies = set(
            orders["currency"]
            .str.upper()
        )

        if len(currencies) > 1:

            return {
                "status": "REFUSED",

                "answer":
                    "I cannot reliably determine total sales.",

                "reason":
                    "The data contains multiple currencies "
                    "(INR and USD), and no exchange rate "
                    "is provided.",

                "code": None
            }

    # -----------------------------------------------------
    # CHENNAI SALES
    # -----------------------------------------------------

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
                    "The generated proof code "
                    "executed successfully.",

                "code": code
            }

    # -----------------------------------------------------
    # HIGHEST SALE
    # -----------------------------------------------------

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
                    "The generated proof code "
                    "executed successfully.",

                "code": code
            }

    # -----------------------------------------------------
    # UNKNOWN
    # -----------------------------------------------------

    return {
        "status": "UNKNOWN",

        "answer":
            "I cannot answer this question reliably.",

        "reason":
            "No verified analysis rule is available "
            "for this question.",

        "code": None
    }


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="info-card">

<h1>📊 Proof-Carrying Data Analyst</h1>

<p style="text-align:center; font-size:18px;">
Ask questions about your data and receive answers
backed by <strong>executable proof</strong>.
</p>

<p style="text-align:center; font-size:15px;">
🔍 Data Validation
&nbsp;&nbsp;•&nbsp;&nbsp;
🧠 Analysis
&nbsp;&nbsp;•&nbsp;&nbsp;
🧾 Proof Generation
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
        "⚠️ Data issues found"
    )

    for issue in issues:

        st.sidebar.warning(issue)

else:

    st.sidebar.success(
        "✅ No data issues found"
    )


st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 🔐 Verification"
)

st.sidebar.write(
    "Every supported answer is checked "
    "by executing its proof code against "
    "the dataset."
)


# =========================================================
# DATA SECTION
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
# QUESTION SECTION
# =========================================================

st.markdown("---")

st.markdown(
    "## 🔍 Ask Your Data"
)

st.write(
    "Enter a question about the available datasets."
)

question = st.text_input(
    "Question",
    placeholder=
    "Example: What are the sales in Chennai?"
)


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.markdown(
    "##### 💡 Example Questions"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        "💰 What are the sales in Chennai?"
    )

with col2:

    st.info(
        "📈 What is the highest sale?"
    )

with col3:

    st.info(
        "🧮 What are the total sales?"
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🚀 Analyze & Verify"
):

    if question.strip() == "":

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        result = analyze(question)

        st.divider()

        # -------------------------------------------------
        # VERIFIED
        # -------------------------------------------------

        if result["status"] == "VERIFIED":

            st.markdown(
                """
                <div class="verified-card">

                <h2>✅ VERIFIED</h2>

                <p>
                The answer was successfully validated
                by executing the proof code.
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
                "### 🧠 Verification Reason"
            )

            st.write(
                result["reason"]
            )

            if result["code"]:

                st.markdown(
                    "### 🧾 Executable Proof"
                )

                st.code(
                    result["code"],
                    language="python"
                )

        # -------------------------------------------------
        # REFUSED
        # -------------------------------------------------

        elif result["status"] == "REFUSED":

            st.markdown(
                """
                <div class="refused-card">

                <h2>❌ REFUSED</h2>

                <p>
                The system refused to provide an
                unreliable answer.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "### Answer"
            )

            st.write(
                result["answer"]
            )

            st.markdown(
                "### ⚠️ Reason"
            )

            st.warning(
                result["reason"]
            )

        # -------------------------------------------------
        # UNKNOWN
        # -------------------------------------------------

        else:

            st.markdown(
                """
                <div class="unknown-card">

                <h2>ℹ️ UNKNOWN</h2>

                <p>
                This question does not have a
                verified analysis rule yet.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "### Answer"
            )

            st.write(
                result["answer"]
            )

            st.markdown(
                "### Reason"
            )

            st.info(
                result["reason"]
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <p style="
        text-align:center;
        color:#64748b !important;
        font-size:13px;
    ">
    🔐 Proof-Carrying Data Analyst
    &nbsp; | &nbsp;
    Data → Analysis → Proof → Verification
    </p>
    """,
    unsafe_allow_html=True
)
