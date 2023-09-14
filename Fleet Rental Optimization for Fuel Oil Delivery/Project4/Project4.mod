range Months = 1..12;

// Demand for each month
int Tons[Months] = ...;

// Decision variables
dvar int+ X[Months]; // 12-month contracts
dvar int+ Y[Months]; // 6-month contracts
dvar int+ Z[Months]; // 3-month contracts

// Objective function
minimize
  sum(m in Months) (60000 *X[m] + 720000*Y[m] + 96000 *Z[m]);

// Constraints
subject to {
  // Delivery requirements
  forall(m in Months)
    150*(X[m] + Y[m] + Z[m]) >= Tons[m];

  // Contract availability
  forall(m in 5..8) {
    X[m] == 0;
    Y[m] == 0;
  }
}
