
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker Dashboard")

df = pd.read_csv("data/expenses.csv")
categories = st.sidebar.multiselect("Category", sorted(df['Category'].unique()), default=sorted(df['Category'].unique()))
df = df[df['Category'].isin(categories)]

c1,c2,c3 = st.columns(3)
c1.metric("Transactions", len(df))
c2.metric("Total Spend", f"₹{df['Amount'].sum():,.0f}")
c3.metric("Average Spend", f"₹{df['Amount'].mean():,.0f}")

st.subheader("Category Spend")
st.bar_chart(df.groupby('Category')['Amount'].sum())

st.subheader("Monthly Trend")
df['Date']=pd.to_datetime(df['Date'])
st.line_chart(df.groupby(df['Date'].dt.month)['Amount'].sum())

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)
