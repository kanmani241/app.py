import pandas as pd  
import streamlit as st  
import io  
import contextlib  

st.set_page_config(  
    page_title="Proof-Carrying Data Analyst",  
    page_icon="📊",  
    layout="wide"  
)  

customers = pd.DataFrame({  
    "customer_id": [1, 2, 3, 4, 5],  
    "name": ["Ravi", "Priya", "Arun", "Meena", "John"],  
    "city": ["Chennai", "Chennai", "Bangalore",  
             "Coimbatore", "Chennai"]  
})  

orders = pd.DataFrame({  
    "order_id": [101, 102, 103, 104, 105, 105, 106],  
    "customer_id": [1, 2, 3, 4, 5, 5, 1],  
    "amount": [5000, 3000, 7000, 4500, 2000, 2000, 100],  
    "currency": ["INR", "INR", "INR", "INR", "INR", "INR", "USD"],  
    "date": ["2025-01-10", "2025-02-01", "2025-02-10",  
             "2025-03-05", "2025-03-20", "2025-03-20",  
             "2025-04-01"]  
})  

products = pd.DataFrame({  
    "product_id": [1, 2, 3],  
    "product_name": ["Laptop", "Phone", "Headphones"],  
    "price_inr": [50000, 25000, 3000]  
})  

def check_data():  
    issues = []  
    for name, df in {  
        "Customers": customers,  
        "Orders": orders,  
        "Products": products  
    }.items():  
        missing = int(df.isna().sum().sum())  
        if missing > 0:  
            issues.append(f"{name} contains {missing} missing value(s).")  
    duplicates = orders["order_id"].duplicated().sum()  
    if duplicates > 0:  
        issues.append(f"Orders contains {duplicates} duplicate order row(s).")  
    currencies = set(orders["currency"].dropna().str.upper())  
    if len(currencies) > 1:  
        issues.append("Multiple currencies found: " + ", ".join(sorted(currencies)))  
    return issues  

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

def analyze(question):  
    q = question.lower()  

    if "total" in q and "sales" in q:  
        currencies = set(orders["currency"].str.upper())  
        if len(currencies) > 1:  
            return {  
                "status": "REFUSED",  
                "answer": "I cannot reliably determine total sales.",  
                "reason": "The data contains multiple currencies "  
                          "(INR and USD), and no exchange rate is provided.",  
                "code": None  
            }  

    if "sales" in q and "chennai" in q:  
        code = '''  
df = orders.merge(customers, on="customer_id")  
df = df[(df["city"] == "Chennai") & (df["currency"] == "INR")]  
df = df.drop_duplicates(subset=["order_id"])  
answer = df["amount"].sum()  
print(answer)  
'''  
        result = verify_code(code)  
        if result == "10000":  
            return {  
                "status": "VERIFIED",  
                "answer": "\u20b910,000",  
                "reason": "The generated proof code executed successfully.",  
                "code": code  
            }  

    if (("highest" in q or "maximum" in q or "largest" in q)  
            and "sale" in q):  
        code = '''  
df = orders[orders["currency"] == "INR"]  
df = df.drop_duplicates(subset=["order_id"])  
answer = df["amount"].max()  
print(answer)  
'''  
        result = verify_code(code)  
        if result == "7000":  
            return {  
                "status": "
