import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Nassau Candy Dashboard", layout="wide")

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip()

# -----------------------
# TITLE
# -----------------------
st.title("🍬 Nassau Candy Distributor Dashboard")
st.write("Internship Project: Sales, Shipping & Profit Analysis")

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("🔍 Filters")

if "Region" in df.columns:
    region = st.sidebar.selectbox("Select Region", ["All"] + list(df["Region"].unique()))
else:
    region = "All"

if "Ship Mode" in df.columns:
    ship_mode = st.sidebar.selectbox("Select Ship Mode", ["All"] + list(df["Ship Mode"].unique()))
else:
    ship_mode = "All"

filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]

if ship_mode != "All":
    filtered_df = filtered_df[filtered_df["Ship Mode"] == ship_mode]

# -----------------------
# KPI CARDS
# -----------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

if "Sales" in df.columns:
    col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")

if "Units" in df.columns:
    col2.metric("Total Units", int(filtered_df["Units"].sum()))

if "Gross Profit" in df.columns:
    col3.metric("Total Profit", f"${filtered_df['Gross Profit'].sum():,.2f}")

# -----------------------
# DATA PREVIEW
# -----------------------
st.subheader("📦 Data Preview")
st.dataframe(filtered_df.head(20))

# -----------------------
# SALES BY REGION
# -----------------------
if "Region" in df.columns and "Sales" in df.columns:
    st.subheader("📈")
    