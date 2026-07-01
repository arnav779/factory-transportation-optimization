import pandas as pd
from scipy.optimize import linprog

# Read data
supply = pd.read_csv("data.csv")["Supply"].tolist()
demand = pd.read_csv("warehouse.csv")["Demand"].tolist()

cost_df = pd.read_csv("cost.csv", index_col=0)
costs = cost_df.values.flatten()

# Equality constraints (Demand)
A_eq = []
for j in range(len(demand)):
    row = [0] * len(costs)
    for i in range(len(supply)):
        row[i * len(demand) + j] = 1
    A_eq.append(row)

b_eq = demand

# Inequality constraints (Supply)
A_ub = []
for i in range(len(supply)):
    row = [0] * len(costs)
    for j in range(len(demand)):
        row[i * len(demand) + j] = 1
    A_ub.append(row)

b_ub = supply

# Solve
result = linprog(
    c=costs,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    method="highs"
)

print("\nMinimum Transportation Cost:", result.fun)

solution = result.x.reshape(len(supply), len(demand))

print("\nOptimal Shipment Plan:\n")
print(pd.DataFrame(
    solution,
    index=["A", "B", "C"],
    columns=["W1", "W2", "W3"]
))

# Analysis Report
total_supply = sum(supply)
total_demand = sum(demand)

print("\nFactory Utilization")
for i, factory in enumerate(["A", "B", "C"]):
    used = solution[i].sum()
    print(f"{factory}: {used:.0f}/{supply[i]} units used")

print("\nSummary")
print("Total Supply:", total_supply)
print("Total Demand:", total_demand)
print("Minimum Transportation Cost:", result.fun)

import matplotlib.pyplot as plt

factories = ["A", "B", "C"]
used_capacity = [solution[i].sum() for i in range(len(supply))]

plt.bar(factories, used_capacity)
plt.title("Factory Utilization")
plt.xlabel("Factories")
plt.ylabel("Units Shipped")
plt.show()

import matplotlib.pyplot as plt

factories = ["A", "B", "C"]
used_capacity = [solution[i].sum() for i in range(len(supply))]

plt.bar(factories, used_capacity)
plt.title("Factory Utilization")
plt.xlabel("Factories")
plt.ylabel("Units Shipped")
plt.show()