import streamlit as st
import pandas as pd

st.set_page_config(page_title="RetainAI", layout="wide")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("RetainAI — Predict which customers may leave (churn). Act instantly. Bring them back.")

st.markdown(
    "Detect risk early • Understand why customers disengage • Automatically guide them back to value"
)

# -------------------------------------------------
# SAMPLE DATA (Demo)
# -------------------------------------------------
data = {
    "Name": ["John", "Sarah", "Mike", "Emma", "David", "Sophia"],
    "Email": [
        "john@test.com",
        "sarah@test.com",
        "mike@test.com",
        "emma@test.com",
        "david@test.com",
        "sophia@test.com",
    ],
    "Last Login (days)": [15, 2, 9, 20, 1, 12],
    "Usage Drop (%)": [70, 10, 40, 80, 5, 60],
}

df = pd.DataFrame(data)

# -------------------------------------------------
# CHURN RISK LOGIC
# -------------------------------------------------
def churn_risk(row):
    if row["Last Login (days)"] > 10 or row["Usage Drop (%)"] > 60:
        return "HIGH"
    elif row["Last Login (days)"] > 5:
        return "MEDIUM"
    else:
        return "LOW"

df["Churn Risk"] = df.apply(churn_risk, axis=1)

# -------------------------------------------------
# DIAGNOSIS (Why system flagged)
# -------------------------------------------------
def detect_reason(days, risk):

    if days > 18:
        return "User likely stopped using the product and lost momentum."
    elif days > 10:
        return "User may not be seeing clear value yet."
    elif risk == "HIGH":
        return "Possible friction, confusion, or unmet expectation."
    else:
        return "Mild drop in engagement detected."

# -------------------------------------------------
# RETENTION ACTION
# -------------------------------------------------
def generate_recovery_message(name, reason):

    return f"""
Hi {name},

We noticed a drop in your recent activity and want to help you succeed.

What we found:
{reason}

What we are doing for you:
• A simple recovery plan is prepared  
• Direct support available if anything blocked you  
• We will help you reach your intended outcome faster  

Most customers in a similar situation quickly regain value after this step.

If something is stopping you, just reply — we will fix it fast.

— RetainAI
"""

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
st.subheader("Customer Risk Dashboard")
st.dataframe(df)

st.divider()

# -------------------------------------------------
# RETENTION ENGINE
# -------------------------------------------------
st.subheader("Autonomous Retention Engine")

selected_user = st.selectbox("Select Customer", df["Name"])

if st.button("Start Recovery"):

    user_row = df[df["Name"] == selected_user].iloc[0]

    reason = detect_reason(
        user_row["Last Login (days)"],
        user_row["Churn Risk"]
    )

    message = generate_recovery_message(
        user_row["Name"],
        reason
    )

    st.success("Recovery started successfully")
    st.info("System detected churn risk, diagnosed cause, and triggered targeted recovery.")

    st.subheader("Why this customer was flagged")
    st.write(reason)

    st.subheader("Recovery Message Sent")
    st.code(message)

    st.subheader("System Learning")
    st.info(
        "System will monitor engagement signals and adapt recovery strategy automatically."
    )
