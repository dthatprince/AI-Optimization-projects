int numMonths = 12;
int num12MonthContracts = 1;
int num6MonthContracts = 2;
int num3MonthContracts = 4;

int deliveryLoad[numMonths] = [423, 434, 580, 873, 1297, 1735, 2211, 1667, 1335, 850, 594, 423];

int remainingLoad = sum(m in 1..numMonths) deliveryLoad[m];

execute {
    while (remainingLoad > 0) {
        if (remainingLoad >= 5 * deliveryLoad[6]) {
            num12MonthContracts++;
            remainingLoad -= deliveryLoad[6];
        } else if (remainingLoad >= 2 * deliveryLoad[6]) {
            num6MonthContracts++;
            remainingLoad -= deliveryLoad[6];
        } else {
            num3MonthContracts++;
            remainingLoad -= deliveryLoad[6];
        }
    }
}

int cost12MonthContracts = num12MonthContracts * 12 * 5000;
int cost6MonthContracts = num6MonthContracts * 6 * 6000;
int cost3MonthContracts = num3MonthContracts * 3 * 8000;
int totalCost = cost12MonthContracts + cost6MonthContracts + cost3MonthContracts;

writeln("Number of 12-month contracts: ", num12MonthContracts);
writeln("Number of 6-month contracts: ", num6MonthContracts);
writeln("Number of 3-month contracts: ", num3MonthContracts);
writeln("Associated cost: ", totalCost);
