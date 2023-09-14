// Data
int C = 150;  // truck capacity
int Cost12 = 5000;
int Cost6 = 6000;
int Cost3 = 8000;

range Months = 1..12;
int demand[Months] = [423, 434, 580, 873, 1297, 1735, 2211, 1667, 1335, 850, 594, 423];

// Decision variables
dvar int+ Y12[Months];  // 12-month contracts
dvar int+ Y6[Months];   // 6-month contracts
dvar int+ Y3[Months];   // 3-month contracts

// Auxiliary parameters
int Z12[Months][Months];  // Contribution of 12-month contracts
int Z6[Months][Months];   // Contribution of 6-month contracts
int Z3[Months][Months];   // Contribution of 3-month contracts

// Define Z parameters
forall(i in Months, j in Months) {
  if (i >= j && i < j+12) Z12[i][j] = 1; else Z12[i][j] = 0;
  if (i >= j && i < j+6) Z6[i][j] = 1; else Z6[i][j] = 0;
  if (i >= j && i < j+3) Z3[i][j] = 1; else Z3[i][j] = 0;
}



// Objective
minimize
  sum(i in Months) (Cost12*Y12[i] + Cost6*Y6[i] + Cost3*Y3[i]);

// Constraints
subject to {
  // Meeting the demand
  forall(i in Months)
    sum(j in Months) (Z12[i][j]*Y12[j] + Z6[i][j]*Y6[j] + Z3[i][j]*Y3[j]) >= demand[i]/C;

  // Contract type limitations
  forall(i in 11..3) {  // November to March
    Y12[i] <= 0;
    Y6[i] <= 0;
  }
}
/*
using CP;
//Helper Functions
int customMax;



// Supply-Demand data
range Months = 1..12;
int supply_demand[Months] = [423, 434, 580, 873, 1297, 1735, 2211, 1667, 1335, 850, 594, 423];

// Updated OPL model
range HighDemandMonths = 11..3;

// Decision variables
dvar int+ x[Months];
dvar int+ y[Months];
dvar int+ z[Months];


//Regular Variable
int totalCapacity = 0;

// Objective
minimize sum(i in Months) (x[i]*8000*3 + y[i]*6000*6 + z[i]*5000*12);

// Constraints
subject to {
  forall(i in Months) {
    x[Months] >= 0;
    y[Months] >= 0;
    z[Months] >= 0;
    forall(j in max1(1,i-2)..i){
      totalCapacity = totalCapacity + x[j]*150;
      };
    for(j in max(1,i-5)..i) totalCapacity += y[j]*150;
    for(j in max(1,i-11)..i) totalCapacity += z[j]*150;
    totalCapacity >= supply_demand[i];
  }
  
  forall(i in HighDemandMonths) {
    y[i] == 0;
    z[i] == 0;
  }
}*/
