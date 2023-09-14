
#*****************************************
from scipy import *
from math import *
from matplotlib.pyplot import *
import sys
from functools import *

# Instance of the problem
if (len(sys.argv) > 1):
    FUNCTION=sys.argv[1]
else:
    print("No function name is specified...")
    sys.exit("USAGE : python SACONT.py sphere|griewank")

# ###################################### Annealing parameters ##################################
T0 = 100 #  initial temperature
Tmin = 1e-10 # final temperature
tau = 1e4 # constant for temperature decrease
Alpha = 0.99 # constant for geometric decrease
Palier = 50 # number of iterations on a temperature level
IterMax = 4000 # max number of iterations of the algorithm
DIM = 5    # dimension of the problem
INF = -600
SUP = 600
STEP = 0.3
# ###########################################################


# Displays the coordinates of the waypoints as well as the best route found and its length
# pre-conditions:
# - best_solution, best_evaluation: best route found and its length,
def dispRes(best_solution, best_evaluation):
    print("best solution = {}".format(best_solution))
    print("best evaluation = {}".format(best_evaluation))

# Display the figure of the graphs of:
# - the set of energies of the retained fluctuations
# - the best energy
# - the temperature decrease
def drawStats(HTime, Henergie, Hbest, HT):
    # display of evolution curves
    fig2 = figure(2)
    subplot(1,3,1)
    semilogy(HTime, Henergie)
    title("Evolution of the total energy of the system")
    xlabel('Time')
    ylabel('Energy')
    subplot(1,3,2)
    semilogy(HTime, Hbest)
    title('Evolution of the best function evaluation')
    xlabel('Time')
    ylabel('Evaluation')
    subplot(1,3,3)
    plot(HTime, HT)
    title('Evolution of the system temperature')
    xlabel('Time')
    ylabel('Temperature')
    show()

def init(inf,sup, n):
    return [random.uniform(inf, sup) for i in range(n)]

def sphere(sol):
    sum = 0
    for i in range(DIM):
        sum += (sol[i])**2    
    return sum
	
def griewank(sol):
    """Griewank's function multimodal, symmetric, inseparable """
    partA = 0
    partB = 1
    for i in range(DIM):
        partA += sol[i]**2
        partB *= math.cos(float(sol[i]) / math.sqrt(i+1))
    return 1 + (float(partA)/4000.0) - float(partB) 
	
# System energy calculation function,
# pre-condition:
# - sol: point of the plane
# postcondition: f(point)
def totalEnergy(sol):
    global FUNCTION
    if FUNCTION == "sphere":
        return sphere(sol)
    elif FUNCTION == "griewank":
        return griewank(sol)
    else:
        print("Error!")
        exit(1)
# fluctuation function around the "thermal" state of the system: exchange of 2 points
# pre-condition:
# - sol: order of browsing cities
# - i,j indices of cities to swap
# post-condition: new browsing order
def fluctuation(sol, step):
    nv = [x+random.uniform(-step,step) for x in sol]
    return nv
	
# implementation function of the Metropolis algorithm for a path relative to its neighbor
# pre-conditions:
# - neighboring x1, x2: init path,
# - disti: distance of each trip
# - T: current system temperature
# post-condition: returns the fluctuation retained by the Metropolis criterion
def metropolis(X1,eval1,X2,eval2,T):
    global best_solution, best_evaluation
    delta = eval1 - eval2 # differential calculation
    if delta <= 0: # if improved,
        if eval1 <= best_evaluation: # comparison to the best, if best, save and refresh the figure
            best_evaluation = eval1
            best_solution = X1[:]
  #          dispRes(best_solution, best_evaluation)
        return (X1, eval1) # the fluctuation is retained, returns the neighbor
    else:
        if random.uniform() > exp(-delta/T): # the fluctuation is not retained according to the probability
            return (X2, eval2)              # initial route
        else:
            return (X1, eval1)              # the fluctuation is retained, returns the neighbor

# initialization of history lists for the final graph
Henergie = []     # energy
HTime = []        # Time
HT = []           # temperature
Hbest = []        # distance

# ##################################### INITIALISATION DE L'ALGORITHME ############################

# definition of the initial route: ascending order of cities
sol = init(INF, SUP,DIM)
# calculation of the initial energy of the system (the initial distance to minimize)
fsol = totalEnergy(sol)
# initialization of the best route
best_solution = sol[:]
best_evaluation = fsol

# we trace the starting path
# on trace le chemin de depart
#draw(best_solution, best_evaluation, x, y)

# #################### MAIN ALGORITHM LOOP #############
t = 0
T = T0
iterPalier = Palier

#  convergence Loop on criterion of nb of iteration (to test the parameters)
for i in range(IterMax):
# Convergence loop on temperature criterion
#while T > Tmin:
    # temperature level TODO: add an improvement count
    while (iterPalier > 0): 

        # creating the fluctuation and measuring the energy
        neighbor = fluctuation(sol, STEP)
        eval_neighbor = totalEnergy(neighbor)

        # application of the Metropolis criterion to determine the retained fluctuation
        (sol, fsol) = metropolis(neighbor,eval_neighbor,sol,fsol,T)

        iterPalier -= 1

    # cooling law application
    t += 1
    # temperature decrease rules
    T = T0*exp(-t/tau)
    #print("\n temperature \n ", T)
    T = T*Alpha
    iterPalier = Palier

    # data logging (historical)
    if t % 2 == 0:
        Henergie.append(fsol)
        HTime.append(t)
        HT.append(T)
        Hbest.append(best_evaluation)
# ################## END OF THE ALGORITHM - DISP OF RESULTS ################

# console display of the result
dispRes(best_solution, best_evaluation)
# stats graph
drawStats(HTime, Henergie, Hbest, HT)
