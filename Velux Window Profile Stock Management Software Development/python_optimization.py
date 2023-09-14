# Data
L = 5  # meters
C = 50  # € per meter
A = 0.60  # meters
B = 2.80  # meters
E = 10  # bars started
N = 100  # windows per week

# Calculate current cost per window
current_cost_per_window = (2 * (B - A) + A) * C

# Calculate potential cost savings per window
potential_cost_savings_per_window = (2 * (B - A) + A) * (C - (C / 2))

# Calculate total potential cost savings per week
total_potential_cost_savings_per_week = N * potential_cost_savings_per_window

# Calculate annual potential cost savings
annual_potential_cost_savings = total_potential_cost_savings_per_week * 52

# Calculate maximum price for the software to be amortized in 3 years
maximum_price = annual_potential_cost_savings / 3

print(f"Maximum price for the software: €{maximum_price:.2f}")
