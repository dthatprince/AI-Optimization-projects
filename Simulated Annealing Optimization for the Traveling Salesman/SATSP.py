
import pandas as pd
from scipy import *
from math import *
from matplotlib.pyplot import *
import sys

# Instance of the problem
# FILE = "NUMBER.tsp"
if (len(sys.argv) > 1):
    FILE=sys.argv[1]
else:
    print("No  specified file...")
    sys.exit("THE USE : python SATSP.py Instance-number.csv")
	
df = pd.read_csv(FILE, header=None, sep=" ")

#print("\n data : \n", df)

dt=np.array(df)
#print("\n df :\n", dt)

############################################# Annealing Parameters ######## ##########################
T0 = 150 # initial temperature
Tmin = 1e-3 # final temperature
tau = 1e4 # constant for temperature decay
Alpha = 0.95 # constant for geometric decay
Step = 7 # number of iterations on a temperature level
IterMax = 200 # max number of iterations of the algorithm
################################################################### #############################################

# Creating a figure
TPSPause = 1e-10 # for displaying
fig1 = figure()
canv = fig1.add_subplot(1,1,1)
xticks([])
yticks([])

# Parsing the data file
# pre-condition: filename: file name (must exist)
# post-condition: (x, y) city coordinates
def parse(df):
	absc = dt[:, 1]
	ordo = dt[:, -1]
	return (array(absc),array(ordo))
	
#    return (array(absc),array(ordo))
	
# Display the coordinates of the points of the path as well as the best path found and its length
# pre-conditions:
# - best_route, best_dist: best ride found and its length,
def dispRes(best_route, best_dist):
    print("route = {}".format(best_route))
    print("distance = {}".format(best_dist))

# Refresh the figure of the trip, we trace the best route found
# pre-conditions:
# - best_route, best_dist: best ride found and its length,
# - x, y: coordinate tables of waypoints
def draw(best_route, best_dist, x, y):
    global canv,lx,ly
    canv.clear()
    canv.plot(x[best_route],y[best_route],'k')
    canv.plot([x[best_route[-1]], x[best_route[0]]],[y[best_route[-1]], \
      y[best_route[0]]],'k')
    canv.plot(x,y,'ro')
    title("Distance : {}".format(best_dist))
    pause(TPSPause)

# Draw the figure of the graphs of:
# - all the energy of the fluctuations retained
# - the best energy
# - the temperature decrease
def drawStats(Htime, Henergy, Hbest, HT):
    # display des courbes d'evolution
    fig2 = figure(2)
    subplot(1,3,1)
    semilogy(Htime, Henergy)
    title("Evolution of the total energy of the system")
    xlabel('Time')
    ylabel('Energy')
    subplot(1,3,2)
    semilogy(Htime, Hbest)
    title('Evolution of the best distance')
    xlabel('time')
    ylabel('Distance')
    subplot(1,3,3)
    plot(Htime, HT)
    title('Evolution of the temperature of the system')
    xlabel('Time')
    ylabel('Temperature')
    show()

# Factoring functions calculating the total distance
# pre-condition: p1(x1, y1), p2(x2, y2) city coordinates
# post-condition: Euclidean distance between 2 cities
def distance(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Calculation function of the system energy,
# pre-condition:
# - coords: coordinates of the path points
# - path: order of course of the cities
# post-condition:TSP: the total distance of the route
def totalEnergy(coords,path):
    energy = 0.0
    coord = coords[path]
#    print(coord)
    for i in range(-1,N-1): # on calcule la distance en fermant la boucle
        energy += distance(coord[i], coord[i+1])
    return energy

# fluctuation function around the "thermal" state of the system: exchange of 2 points
# pre-condition:
# - wpath: order of course of the cities
# - i, j indices of cities to swap
# post-condition: new order of course
def fluctuationTwo(path,i,j):
    nv = path[:]
    temp = nv[i]
    nv[i] = nv[j]
    nv[j] = temp
    return nv

# implementation function of the Metropolis algorithm for a path to its neighbor
# pre-conditions:
# - neighbor ch1, ch2: init path,
# - disti: distance of each trip
# - T: current system temperature
# post-condition: returns the fluctuation retained by the Metropolis criterion
def metropolis(ch1,dist1,ch2,dist2,T):
    global best_route, best_dist, x, y
    delta = dist1 - dist2 # calculating the differential
    if delta <= 0: # if improving,
        if dist1 <= best_dist: # comparison to the best, if better, save and refresh the figure
            best_dist = dist1
            best_route = ch1[:]
            draw(best_route, best_dist, x, y)
        return (ch1, dist1) # the fluctuation is retained, returns the neighbor
    else:
        if random.uniform() > exp(-delta/T): # the fluctuation is not retained according to the proba
            return (ch2, dist2)              # initial path
        else:
            return (ch1, dist1)              # the fluctuation is retained, returns the neighbor

# initializing history lists for the final graph
Henergy = []     # energy
Htime = []       # time
HT = []           # temperature
Hbest = []        # distance

# ######################################### INITIALIZING THE ALGORITHM ####### #####################
# Construction of the data from the file
(x,y) = parse(df) # x, y are kept in the state for graphic display
coords = array(list(zip(x,y)), dtype=float) # We build the array of coordinates (x, y)

# Problem peremeter
N = len(coords)    # numbre of cities

# definition of initial route: increasing order of cities
route = [i for i in range(N)]
# calculation of the initial energy of the system (the initial distance to be minimized)
dist = totalEnergy(coords,route)
#initialization of the best route
best_route = route[:]
best_dist = dist

# we trace the path of departure
draw(best_route, best_dist, x, y)

# main loop of the annealing algorithm
t = 0
T = T0
iterStep = Step

# ############################################ PRINCIPAL LOOP OF THE ALGORITHM ###### ######################

# Convergence loop on criteria of number of iteration (to test the parameters)
for i in range(IterMax):
# Convergence loop on temperature criterion
#while T> Tmin:
     # cooling law enforcement
    while (iterStep > 0): 
      # choice of two random cities
        i = random.random_integers(0,N-1)
        j = i
        while (i==j):
            j = random.random_integers(0,N-1)

        # creation of fluctuation and measurement of energy
        neighbor = fluctuationTwo(route,i,j)
        dist_neighbor = totalEnergy(coords,neighbor)

        # application of the Metropolis criterion to determine the persisted fulctuation
        (route, dist) = metropolis(neighbor,dist_neighbor,route,dist,T)

        iterStep -= 1

    # cooling law enforcement
    t += 1
    # rules of temperature decreases
    #T = T0*exp(-t/tau) //exp
    T = T*Alpha   #
    iterStep = Step  

    #historization of data
    if t % 2 == 0:
        Henergy.append(dist)
        Htime.append(t)
        HT.append(T)
        Hbest.append(best_dist)

############################################## END OF ALGORITHM - DISPLAY RESULTS ### #########################

# display result in console
dispRes(best_route, best_dist)
# graphic of stats
drawStats(Htime, Henergy, Hbest, HT)
