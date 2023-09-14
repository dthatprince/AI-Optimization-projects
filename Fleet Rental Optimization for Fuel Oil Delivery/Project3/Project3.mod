range Months = 1..12;

// Demand for each month
int Tons[Months] = ...;

// Decision variables
dvar int+ X[Months]; // 12-month contracts
dvar int+ Y[Months]; // 6-month contracts
dvar int+ Z[Months]; // 3-month contracts

// Objective function
minimize
  sum(m in Months) (5000*X[m] + 6000*Y[m] + 8000*Z[m]);

// Constraints
subject to {

  forall(m in 1..3)
    150*(X[m] + Y[m] + Z[m]) >= Tons[m];
  
  forall(m in 4..6)
    150*(X[m-3] + Y[m] + Z[m]) >= Tons[m];
    
  forall(m in 7..9)
    150*(X[m-6] + Y[m-3] + Z[m]) >= Tons[m];
    
  forall(m in 10..12)
    150*(X[m-9] + Y[m-6] + Z[m]) >= Tons[m];
  
  // Contract availability
  forall(m in 5..8) {
    X[m] == 0;
    Y[m] == 0;
  }

}
