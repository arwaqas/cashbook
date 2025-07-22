
import streamlit as st
import pandas as pd
import uuid

st.set_page_config(page_title="CashBook Tracker", layout="centered")

st.title("📘 CashBook Expense Tracker")

# Session state initialization
if "cashbooks" not in st.session_state:
    st.session_state.cashbooks = {}
if "current_cashbook" not in st.session_state:
    st.session_state.current_cashbook = None

# Sidebar for cashbook selection and creation
st.sidebar.header("📁 Manage CashBooks")
cashbook_names = list(st.session_state.cashbooks.keys())

selected = st.sidebar.selectbox("Select CashBook", ["-- Select --"] + cashbook_names)
if selected != "-- Select --":
    st.session_state.current_cashbook = selected

new_cashbook = st.sidebar.text_input("New CashBook Name")
if st.sidebar.button("➕ Create New CashBook") and new_cashbook.strip():
    if new_cashbook in st.session_state.cashbooks:
        st.sidebar.warning("CashBook already exists!")
    else:
        st.session_state.cashbooks[new_cashbook] = []
        st.session_state.current_cashbook = new_cashbook
        st.sidebar.success(f"Created '{new_cashbook}'")

# Main section for transaction entry
if st.session_state.current_cashbook:
    st.subheader(f"📓 Entries for: {st.session_state.current_cashbook}")

    col1, col2 = st.columns(2)
    with col1:
        description = st.text_input("Description")
    with col2:
        amount = st.number_input("Amount", min_value=0.0, step=0.1)

    col3, col4 = st.columns(2)
    if col3.button("🟢 Payment In"):
        if description and amount > 0:
            st.session_state.cashbooks[st.session_state.current_cashbook].append({
                "id": str(uuid.uuid4()),
                "description": description,
                "amount": amount,
                "type": "in"
            })
    if col4.button("🔴 Payment Out"):
        if description and amount > 0:
            st.session_state.cashbooks[st.session_state.current_cashbook].append({
                "id": str(uuid.uuid4()),
                "description": description,
                "amount": amount,
                "type": "out"
            })

    # Display current entries
    df = pd.DataFrame(st.session_state.cashbooks[st.session_state.current_cashbook])
    if not df.empty:
        df["Amount"] = df.apply(lambda x: f"+${x['amount']}" if x["type"] == "in" else f"-${x['amount']}", axis=1)
        df_display = df[["description", "Amount", "type"]].rename(columns={"description": "Description", "type": "Type"})
        st.dataframe(df_display, use_container_width=True)

        total_in = df[df["type"] == "in"]["amount"].sum()
        total_out = df[df["type"] == "out"]["amount"].sum()
        balance = total_in - total_out

        st.markdown("---")
        st.markdown(f"""
**Total In:** 🟢 ${total_in:,.2f}  
**Total Out:** 🔴 ${total_out:,.2f}  
**Balance:** 💰 ${balance:,.2f}
""")
    else:
        st.info("No entries yet.")
else:
    st.info("Please select or create a CashBook from the sidebar.")
