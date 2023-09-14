# Data
tons = [423, 434, 580, 873, 1297, 1735, 2211, 1667, 1335, 850, 594, 423]

# Decision variables
months = range(1, 13)
X = {}
Y = {}
Z = {}

# Objective function coefficients
cost_X = 5000
cost_Y = 6000
cost_Z = 8000

# Initialize decision variables
for m in months:
    X[m] = 0
    Y[m] = 0
    Z[m] = 0

# Constraints
for m in months:
    if m <= 3:
        if 150 * (X[m] + Y[m] + Z[m]) < tons[m - 1]:
            diff = tons[m - 1] - 150 * (X[m] + Y[m] + Z[m])
            while diff >= 150:
                if X[m] < 12:
                    X[m] += 1
                elif Y[m] < 6:
                    Y[m] += 1
                else:
                    Z[m] += 1
                diff -= 150
    else:
        if 150 * (X[m - 3] + Y[m - 3] + Z[m - 3]) < tons[m - 1]:
            diff = tons[m - 1] - 150 * (X[m - 3] + Y[m - 3] + Z[m - 3])
            while diff >= 150:
                if X[m - 3] < 12:
                    X[m - 3] += 1
                elif Y[m - 3] < 6:
                    Y[m - 3] += 1
                else:
                    Z[m - 3] += 1
                diff -= 150

# Calculate objective value
total_cost = sum(cost_X * X[m] + cost_Y * Y[m] + cost_Z * Z[m] for m in months)

# Print the solution
for m in months:
    print(f"Month {m}: X={X[m]}, Y={Y[m]}, Z={Z[m]}")
print("Objective value:", total_cost)