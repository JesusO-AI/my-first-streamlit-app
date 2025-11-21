import pandas as pd
import streamlit as st
import altair as alt

# Sidebar file uploader
st.sidebar.header('📂 Upload Your File')
uploaded_file = st.sidebar.file_uploader(
    "Upload General-Ledger.xlsx", type=["xlsx"])

if uploaded_file is not None:
    # Load uploaded Excel file
    pf = pd.read_excel(uploaded_file)
    st.success("File loaded successfully!")

    # --- Data Cleaning ---
    pf["TxnDate"] = pd.to_datetime(pf["TxnDate"], errors="coerce")
    pf["Debit"] = pd.to_numeric(pf["Debit"], errors="coerce")
    pf["Credit"] = pd.to_numeric(pf["Credit"], errors="coerce")
    pf.drop_duplicates(inplace=True)
    pf.dropna(subset=["TxnDate", "Debit", "Credit",
              "AccountName"], inplace=True)

    # --- Title ---
    st.subheader('Debit & Credit Analysis')

    # --- KPIs: Debit ---
    col1, col2, col3 = st.columns(3)
    col1.metric(label='Total Debit Amount', value=pf.Debit.sum(), border=True)
    col2.metric(label='Highest Debit Entry', value=pf.Debit.max(), border=True)
    col3.metric(label='Number of Transactions (Debit)',
                value=pf.Debit.count(), border=True)

    # --- KPIs: Credit ---
    col4, col5, col6 = st.columns(3)
    col4.metric(label='Total Credit Amount',
                value=pf.Credit.sum(), border=True)
    col5.metric(label='Highest Credit Entry',
                value=pf.Credit.max(), border=True)
    col6.metric(label='Number of Transactions (Credit)',
                value=pf.Credit.count(), border=True)

    # --- Bar Charts ---
    st.subheader('Debit by Account Name')
    st.bar_chart(pf, x="AccountName", y="Debit", stack=False)

    st.subheader('Credit by Account Name')
    st.bar_chart(pf, x="AccountName", y="Credit", stack=False)

    # --- Line Charts (Monthly max) ---
    df_monthly = pf.set_index("TxnDate").resample("M").max()
    st.subheader("Monthly Highest Debit Transactions")
    st.line_chart(df_monthly["Debit"])

    st.subheader("Monthly Highest Credit Transactions")
    st.line_chart(df_monthly["Credit"])

    # --- Date Range Filters ---
    min_date = pf["TxnDate"].min()
    max_date = pf["TxnDate"].max()

    # Debit filter
    start_debit, end_debit = st.date_input(
        "Date Range Debit", value=(min_date, max_date))
    df_filtered_debit = pf[(pf["TxnDate"] >= pd.to_datetime(start_debit)) &
                           (pf["TxnDate"] <= pd.to_datetime(end_debit))]
    st.write("Filtered Data (Debit)")
    st.dataframe(df_filtered_debit)
    st.line_chart(df_filtered_debit["Debit"])

    # Credit filter
    start_credit, end_credit = st.date_input(
        "Date Range Credit", value=(min_date, max_date))
    df_filtered_credit = pf[(pf["TxnDate"] >= pd.to_datetime(start_credit)) &
                            (pf["TxnDate"] <= pd.to_datetime(end_credit))]
    st.write("Filtered Data (Credit)")
    st.dataframe(df_filtered_credit)
    st.line_chart(df_filtered_credit["Credit"])

else:
    # Show instructions if no file is uploaded
    st.title("General Ledger Analysis Dashboard")
    st.info('👈 **Please upload your Excel file** using the sidebar to see the analysis.')
