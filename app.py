import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import numpy as np

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Factory Transportation Optimization",
    page_icon="🏭",
    layout="wide"
)

# ----------------------------
# TITLE
# ----------------------------
st.title("🏭 Factory Transportation Optimization Dashboard")
st.markdown("### Supply Chain Cost Optimization using Linear Programming")
st.markdown("---")

# ----------------------------
# LOAD DATA
# ----------------------------
try:
    supply_df = pd.read_csv("data.csv")
    demand_df = pd.read_csv("warehouse.csv")
    cost_df = pd.read_csv("cost.csv", index_col=0)

except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# ----------------------------
# CLEAN COLUMN NAMES
# ----------------------------
supply_df.columns = supply_df.columns.str.strip()
demand_df.columns = demand_df.columns.str.strip()
cost_df.columns = cost_df.columns.str.strip()

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("Dashboard Filters")

factory = st.sidebar.selectbox(
    "Select Factory",
    cost_df.index.tolist()
)

warehouse = st.sidebar.selectbox(
    "Select Warehouse",
    cost_df.columns.tolist()
)

# ----------------------------
# EXTRACT DATA
# ----------------------------
supply = supply_df.iloc[:,1].values
demand = demand_df.iloc[:,1].values
cost = cost_df.values

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
total_factories = len(supply)
total_warehouses = len(demand)
total_supply = int(sum(supply))
total_demand = int(sum(demand))

# ----------------------------
# KPI CARDS
# ----------------------------
c1,c2,c3,c4 = st.columns(4)

c1.metric("🏭 Factories", total_factories)
c2.metric("📦 Warehouses", total_warehouses)
c3.metric("🚚 Total Supply", total_supply)
c4.metric("📥 Total Demand", total_demand)

st.markdown("---")

# ----------------------------
# DATA TABLES
# ----------------------------
tab1,tab2,tab3 = st.tabs([
    "Supply",
    "Demand",
    "Transportation Cost"
])

with tab1:
    st.subheader("Factory Supply")
    st.dataframe(supply_df,use_container_width=True)

with tab2:
    st.subheader("Warehouse Demand")
    st.dataframe(demand_df,use_container_width=True)

with tab3:
    st.subheader("Transportation Cost Matrix")
    st.dataframe(cost_df,use_container_width=True)

st.markdown("---")
# ----------------------------
# LINEAR PROGRAMMING OPTIMIZATION
# ----------------------------

num_factories = len(supply)
num_warehouses = len(demand)

# Objective Function
c = cost.flatten()

# Equality Constraints (Demand)
A_eq = []
b_eq = []

for j in range(num_warehouses):
    row = np.zeros(num_factories * num_warehouses)
    for i in range(num_factories):
        row[i * num_warehouses + j] = 1
    A_eq.append(row)
    b_eq.append(demand[j])

# Inequality Constraints (Supply)
A_ub = []
b_ub = []

for i in range(num_factories):
    row = np.zeros(num_factories * num_warehouses)
    for j in range(num_warehouses):
        row[i * num_warehouses + j] = 1
    A_ub.append(row)
    b_ub.append(supply[i])

bounds = [(0, None)] * (num_factories * num_warehouses)

result = linprog(
    c,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method="highs"
)

st.markdown("---")
st.subheader("🚛 Optimization Results")

if result.success:

    shipment = result.x.reshape(num_factories, num_warehouses)

    shipment_df = pd.DataFrame(
        shipment,
        index=cost_df.index,
        columns=cost_df.columns
    )

    c1, c2 = st.columns(2)

    with c1:
        st.success("✅ Optimization Successful")
        st.metric(
            "Minimum Transportation Cost",
            f"${result.fun:,.2f}"
        )

    with c2:
        st.metric(
            "Optimization Status",
            "Optimal"
        )

    st.markdown("### Optimal Shipment Plan")

    st.dataframe(
        shipment_df.style.format("{:.0f}"),
        use_container_width=True
    )

else:

    st.error("Optimization Failed!")
    st.write(result.message)

st.markdown("---")
# ----------------------------
# VISUALIZATIONS
# ----------------------------

st.subheader("📊 Dashboard Visualizations")

chart1, chart2 = st.columns(2)

# Factory Supply Chart
with chart1:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(cost_df.index, supply)
    ax.set_title("Factory Supply")
    ax.set_xlabel("Factories")
    ax.set_ylabel("Units")
    st.pyplot(fig)

# Warehouse Demand Chart
with chart2:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(cost_df.columns, demand)
    ax.set_title("Warehouse Demand")
    ax.set_xlabel("Warehouses")
    ax.set_ylabel("Units")
    st.pyplot(fig)

st.markdown("---")

# ----------------------------
# COST MATRIX HEATMAP
# ----------------------------

st.subheader("🔥 Transportation Cost Heatmap")

fig, ax = plt.subplots(figsize=(6,4))

heatmap = ax.imshow(cost, aspect="auto")

ax.set_xticks(range(len(cost_df.columns)))
ax.set_xticklabels(cost_df.columns)

ax.set_yticks(range(len(cost_df.index)))
ax.set_yticklabels(cost_df.index)

for i in range(cost.shape[0]):
    for j in range(cost.shape[1]):
        ax.text(j, i, cost[i, j],
                ha="center",
                va="center",
                color="white")

plt.colorbar(heatmap)

st.pyplot(fig)

st.markdown("---")

# ----------------------------
# PIE CHARTS
# ----------------------------

pie1, pie2 = st.columns(2)

with pie1:
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(
        supply,
        labels=cost_df.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Supply Distribution")
    st.pyplot(fig)

with pie2:
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(
        demand,
        labels=cost_df.columns,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Demand Distribution")
    st.pyplot(fig)

st.markdown("---")

#
# ----------------------------
# SHIPMENT CHART
# ----------------------------

if result.success:

    st.subheader("🚚 Optimal Shipment Distribution")

    fig, ax = plt.subplots(figsize=(8,5))

    shipment_df.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Factories")
    ax.set_ylabel("Units")
    ax.set_title("Factory to Warehouse Shipments")

    st.pyplot(fig)

st.markdown("---")

# ----------------------------
# BUSINESS INSIGHTS
# ----------------------------

st.subheader("💡 Business Insights")

highest_supply = cost_df.index[np.argmax(supply)]
highest_demand = cost_df.columns[np.argmax(demand)]

cheapest = np.min(cost)
location = np.where(cost == cheapest)

factory_name = cost_df.index[location[0][0]]
warehouse_name = cost_df.columns[location[1][0]]

st.success(f"🏭 Highest Supply Factory : {highest_supply}")

st.info(f"📦 Highest Demand Warehouse : {highest_demand}")

st.warning(
    f"💰 Cheapest Route : {factory_name} ➜ {warehouse_name} "
    f"(Cost = {cheapest})"
)

if total_supply >= total_demand:
    st.success("✅ Total Supply is sufficient to satisfy all demand.")
else:
    st.error("❌ Total Supply is NOT sufficient to satisfy demand.")

st.markdown("---")
st.caption("Developed using Python, Streamlit and Linear Programming (SciPy)")
