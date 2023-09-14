from docplex.mp.model import Model

# Data
tons = [423, 434, 580, 873, 1297, 1735, 2211, 1667, 1335, 850, 594, 423]

# Create model
model = Model("Contract Optimization")

# Decision variables
months = range(1, 13)
X = model.integer_var_dict(months, name="X")  # 12-month contracts
Y = model.integer_var_dict(months, name="Y")  # 6-month contracts
Z = model.integer_var_dict(months, name="Z")  # 3-month contracts

# Objective function
model.minimize(
    model.sum((12 * 5000) * X[m] + (6*6000) * Y[m] + (8000*4) * Z[m] for m in months)
)

# Constraints
for m in months:
    model.add_constraint(
        model.sum(
            ((i >= m - 11) * 150 * X[i] + (i >= m - 5) * 150 * Y[i])
            for i in months
        ) + 150 * Z[m] >= tons[m - 1]
    )

for m in range(5, 9):
    model.add_constraint(X[m] == 0)
    model.add_constraint(Y[m] == 0)

# Solve the model
solution = model.solve()

# Print the solution
if solution:
    for m in months:
        print(f"Month {m}: X={solution[X[m]]}, Y={solution[Y[m]]}, Z={solution[Z[m]]}")
    print("Objective value: ", solution.objective_value)
else:
    print("No solution found.")
