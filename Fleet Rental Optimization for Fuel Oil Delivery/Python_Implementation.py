import cplex

model = cplex.Cplex()

numMonths = 12
num12MonthContracts = model.variables.add(
    lb=[0],
    ub=[cplex.infinity],
    types=[model.variables.type.integer],
    names=["num12MonthContracts"]
)
num6MonthContracts = model.variables.add(
    lb=[0],
    ub=[cplex.infinity],
    types=[model.variables.type.integer],
    names=["num6MonthContracts"]
)
num3MonthContracts = model.variables.add(
    lb=[0],
    ub=[cplex.infinity],
    types=[model.variables.type.integer],
    names=["num3MonthContracts"]
)

deliveryLoad = [423, 434, 580, 873, 1297, 1735, 2211, 1667, 1335, 850, 594, 423]

model.objective.set_linear("num12MonthContracts", 12 * 5000)
model.objective.set_linear("num6MonthContracts", 6 * 6000)
model.objective.set_linear("num3MonthContracts", 3 * 8000)
model.objective.set_sense(model.objective.sense.minimize)

load_constraint = [
    cplex.SparsePair(["num12MonthContracts"], [12 * 150]),
    cplex.SparsePair(["num6MonthContracts"], [6 * 150]),
    cplex.SparsePair(["num3MonthContracts"], [3 * 150])
]
model.linear_constraints.add(
    lin_expr=load_constraint,
    senses=["G", "G", "G"],
    rhs=[0, 0, 0]
)

model.solve()

num12MonthContracts_value = model.solution.get_values("num12MonthContracts")
num6MonthContracts_value = model.solution.get_values("num6MonthContracts")
num3MonthContracts_value = model.solution.get_values("num3MonthContracts")

# Heuristic algorithm
remainingLoad = sum(deliveryLoad)

while remainingLoad > 0:
    if remainingLoad >= 5 * deliveryLoad[6]:
        num12MonthContracts_value += 1
        remainingLoad -= deliveryLoad[6]
    elif remainingLoad >= 2 * deliveryLoad[6]:
        num6MonthContracts_value += 1
        remainingLoad -= deliveryLoad[6]
    else:
        num3MonthContracts_value += 1
        remainingLoad -= deliveryLoad[6]

cost12MonthContracts = num12MonthContracts_value * 12 * 5000
cost6MonthContracts = num6MonthContracts_value * 6 * 6000
cost3MonthContracts = num3MonthContracts_value * 3 * 8000
totalCost = cost12MonthContracts + cost6MonthContracts + cost3MonthContracts

print("Number of 12-month contracts:", num12MonthContracts_value)
print("Number of 6-month contracts:", num6MonthContracts_value)
print("Number of 3-month contracts:", num3MonthContracts_value)
print("Associated cost:", totalCost)
