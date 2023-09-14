/*********************************************
 * OPL 22.1.1.0 Model
 * Author: gatsby
 * Creation Date: May 11, 2023 at 1:57:44 PM
 *********************************************/
/*
using CP;

// Decision variable
dvar int+ NumberOfTrucks[1..12][1..3];




// Data
int Tons[1..12] = [423, 434, 580, 873, 1297, 1735, 2211, 1667, 1335, 850, 594, 423];
int CumulativePercentage[1..12] = [3, 7, 12, 19, 29, 43, 61, 74, 85, 92, 97, 100];
int MonthlyRentalCost[1..3] = [5000, 6000, 8000];

// Objective function: Minimize the total cost of renting trucks
//minimize


dexpr int TotalCost=  sum(i in 1..12, j in 1..3) NumberOfTrucks[i][j] * MonthlyRentalCost[j];

minimize TotalCost; 

// Add your constraints here

// Constraints
// Constraints
// Constraints
subject to {
    // Non-negativity constraints for the decision variables
    forall (i in 1..12, j in 1..3)
        NumberOfTrucks[i][j] >= 0;

    // Integrality constraints for the decision variables
    forall (i in 1..12, j in 1..3)
        NumberOfTrucks[i][j] == round(NumberOfTrucks[i][j]);

    // The number of trucks rented for each month must be within the limits specified in Table 2 (daily load in tons)
    forall (i in 1..12) {
        sum(j in 1..3) NumberOfTrucks[i][j] * 150 >= Tons[i];
    }

    // The rental companies only accept to rent over three months in the period of high demand (from November to February)
    forall (i in 1..12, j in 1..3) {
        ((i >= 11) || (i <= 2)) => (NumberOfTrucks[i][j] * j <= 3);
    }
}
*/
/*********************************************
 * OPL 22.1.1.0 Model
 * Author: gatsby
 * Creation Date: May 11, 2023 at 1:57:44 PM
 *********************************************/

/*********************************************
 * OPL 22.1.1.0 Model
 * Author: gatsby
 * Creation Date: May 11, 2023 at 1:57:44 PM
 *********************************************/
/*
using CP;

// Input data
int Tons[1..12] = [423, 434, 580, 873, 1297, 1735, 2211, 1667, 1335, 850, 594, 423];
int MonthlyRentalCost[1..3] = [5000, 6000, 8000];

// Decision variable
dvar int+ NumberOfTrucks[1..12][1..3];

// Objective function: Minimize the total cost of renting trucks
dexpr int TotalCost=  sum(i in 1..12, j in 1..3) NumberOfTrucks[i][j] * MonthlyRentalCost[j];

minimize TotalCost;
int i;
int j;

// Constraints
subject to {
    // Non-negativity constraints for the decision variables
        NumberOfTrucks[i][j] >= 0;

    // The number of trucks rented for each month must be within the limits specified in Table 2 (daily load in tons)
    forall (i in 1..12) {
        sum(j in 1..3) NumberOfTrucks[i][j] * 150 >= Tons[i];
    }

    // The rental companies only accept to rent over three months in the period of high demand (from November to February)
    forall (i in 1..12, j in 1..3) {
        if (i >= 11 || i <= 2) {
            NumberOfTrucks[i][j] * j <= 3;
        }
    }
}

// Heuristics approach: Best Fit Decreasing algorithm
tuple TruckSolution { int month; int type; int count; }
tuple TruckData {
    int month;
    int type;
    int count;
}

{TruckData} initialSolution = ...;


// Load the heuristic solution
execute {
    initialSolution = ...;  // Load the initial solution from a .dat file

    for (var t in initialSolution) {
        cplex.postHeuristicSolution(NumberOfTrucks[t.month][t.type], t.count);
    }
}
*/
using CP;
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

