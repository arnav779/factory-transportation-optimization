import pandas as pd
import streamlit as st

df = pd.read_csv("data.csv")

# ✅ ADD THIS LINE (FIX)
df.columns = df.columns.str.strip()

st.title("Nassau Candy Project")