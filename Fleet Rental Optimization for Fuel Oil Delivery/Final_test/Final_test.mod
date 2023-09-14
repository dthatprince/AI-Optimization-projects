/*********************************************
 * OPL 22.1.1.0 Model
 * Author: gatsby
 * Creation Date: May 12, 2023 at 6:49:51 PM
 *********************************************/

range Months = 1..12;

// Demand for each month
int Tons[Months] = ...;

// Decision variables
dvar int+ X[Months]; // 12-month contracts
dvar int+ Y[Months]; // 6-month contracts
dvar int+ Z[Months]; // 3-month contracts

// Objective function
minimize
  sum(m in Months) (60000*X[m] + 72000*Y[m] + 96000*Z[m]);

// Constraints
subject to {
  // Delivery requirements for each month
  forall(m in 1..12) {
    sum(i in 1..m) ((i >= m-11) * 150*X[i] + (i >= m-5) * 150*Y[i]) + 150*Z[m] >= Tons[m];
  }
  // Contract availability
  forall(m in 5..8) {
    X[m] == 0;
    Y[m] == 0;
  }
}

 