import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Nassau Candy Dashboard", layout="wide")

# ----------------------------
# TITLE
# ----------------------------
st.title("🍬 Nassau Candy Distributor Analytics Dashboard")
st.write("Internship Project: Sales, Shipping & Profit Analysis")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.selectbox("Select Region", ["All"] + list(df["Region"].unique()))
ship_mode = st.sidebar.selectbox("Select Ship Mode", ["All"] + list(df["Ship Mode"].unique()))

# Apply filters
filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]

if ship_mode != "All":
    filtered_df = filtered_df[filtered_df["Ship Mode"] == ship_mode]

# ----------------------------
# KPI METRICS
# ----------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Units", int(filtered_df["Units"].sum()))
col3.metric("Total Profit", f"${filtered_df['Gross Profit'].sum():,.2f}")

# ----------------------------
# DATA PREVIEW
# ----------------------------
st.subheader("📦 Data Preview")
st.dataframe(filtered_df.head(20))

# ----------------------------
# SALES BY REGION
# ----------------------------
st.subheader("📈 Sales by Region")

region_sales = df.groupby("Region")["Sales"].sum()

fig, ax = plt.subplots()
region_sales.plot(kind="bar", ax=ax)
ax.set_ylabel("Sales")
st.pyplot(fig)

# ----------------------------
# SHIPPING MODE ANALYSIS
# ----------------------------
st.subheader("🚚 Shipping Mode Distribution")

ship_counts = df["Ship Mode"].value_counts()

fig2, ax2 = plt.subplots()
ship_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# ----------------------------
# PROFIT ANALYSIS
# ----------------------------
st.subheader("💰 Profit vs Cost")

fig3, ax3 = plt.subplots()
ax3.scatter(df["Cost"], df["Gross Profit"])
ax3.set_xlabel("Cost")
ax3.set_ylabel("Gross Profit")
st.pyplot(fig3)

# ----------------------------
# FOOTER
# ----------------------------
st.success("Dashboard loaded successfully 🚀")
st.write("Built for internship submission - Nassau Candy Project")