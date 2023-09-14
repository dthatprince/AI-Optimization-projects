
import pandas as pd
from scipy import *
from math import *
from matplotlib.pyplot import *
import sys
import random as rdm
import sys

# Instance of the problem
#FILE="NUMBRE.tsp"
if (len(sys.argv) > 1):
    FILE=sys.argv[1]
else:
    print("No file is specified...")
    sys.exit("USE : python tabooTSP.py INSTANCE_NUMBRE.tsp")

df = pd.read_csv(FILE, header=None, sep=" ")

#print("\n data : \n", df)

dt=np.array(df)
#print("\n df :\n", dt)


# ############## Parameters of taboo ################
# Parameters of the problem

# Parameters of taboo
ntaboo = 1
nbNeigh = 3
iterMax = 10000
idemMax = iterMax/10

# Creating the figure
TPSPause = 1e-10 # for displaying
fig1 = figure()
canv = fig1.add_subplot(1,1,1)
xticks([])
yticks([])

# Parsing de data file
# pre-condition : nomFILE : file name (must exist)
# post-condition : (x,y) coordinates of cities
def parse(df):
	absc = dt[:, 1]
	ordo = dt[:, -1]
	return (array(absc),array(ordo))
	
# Displays the coordinates of the points of the path, the best path found and its length
# pre-conditions :
#   - best_route, best_dist : best found route and its length,
def dispRes(best_route, best_dist):
    print("route = {}".format(best_route))
    print("distance = {}".format(best_dist))

# Refresh the figure of the road, we trace the best found route
# pre-conditions :
#   - best_route, best_dist : best found route and its length,
#   - x, y : coordinates of points of the path
def draw(best_route, best_dist, x, y):
    global canv
    canv.clear()
    canv.plot(x[best_route],y[best_route],'k')
    canv.plot([x[best_route[-1]], x[best_route[0]]],[y[best_route[-1]], \
      y[best_route[0]]],'k')
    canv.plot(x,y,'ro')
    title("Distance : {}".format(best_dist))
    pause(TPSPause)

# Figure of graphs of:
#   - all the energy of the retained fluctuations 
#   - The best energy
def drawStats(Htime, Henergy, Hbest):
    # display of evolution curves
    fig2 = figure(2)
    subplot(1,2,1)
    semilogy(Htime, Henergy)
    title("Evolution de la solution en cours")
    xlabel('time')
    ylabel('Energy')
    subplot(1,2,2)
    semilogy(Htime, Hbest)
    title('Evolution de la meilleure distance')
    xlabel('time')
    ylabel('Distance')
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
def evalue(coords,path):
    energy = 0.0
    coord = coords[path]
    for i in range(-1,N-1): # the distance is calculated by closing the loop
        energy += distance(coord[i], coord[i+1])
    return energy

# move the point at the end of the course (3 edges)
# pre-condition :
#   - path : Course order of cities
#   - i index of the city to put at the end of the course
# post-condition :new course order
def permuteOne(path,i):
    nv = path[:]
    e = nv.pop(i)
    nv.append(e)
    return nv

# exchange of 2 points (4 edges)
# pre-condition :
#   - path : Course order of cities
#   - i,j indices of cities to be swapped
# post-condition : new course order
def permuteTwo(path,i,j):
    nv = path[:]
    temp = nv[i]
    nv[i] = nv[j]
    nv[j] = temp
    return nv

# move the point (city) at the end of the course
# use permuteOne lperm
# generate only one neighbor
# pre-condition :
#   - path : Course order of cities
#   - i index of the city to put at the end of the course
#   - ltaboo : taboo list of path already traveled
# post-condition : new course order
def bestNeighbor(path, nbNeigh, ltaboo):
    global bestV, bestDist
    #list of indices to swap to generate Neighbors
    lperm = rdm.sample(range(N), nbNeigh)
    # case of the first neighbor
    prem = lperm.pop(0)
    bestV = permuteOne(path,prem)
    bestDist = evalue(coords,bestV)

    for i in lperm:
        Neigh = permuteOne(path,i)
        if Neigh not in ltaboo:
            d = evalue(coords,Neigh)
            if (d < bestDist):
                bestV = Neigh
                bestDist = d
    return (bestV,bestDist)

# move the point (city) at the end of the course
# use permuteOne
# generate nbNeigh
# pre-condition :
#   - path : Course order of cities
#   - i index of the city to put at the end of the course
#   - ltaboo : taboo list of path already traveled
# post-condition : new course order	
def bestNeighbor1(path, nbNeigh, ltaboo):
    global bestV, bestDist    
    # case of the first neighbor
    nb = 1
    # case of the first neighbor
    i = scp.random.random_integers(0,N-1)
    bestV = permuteOne(path,i)
    bestDist = evalue(coords,bestV)

    while nb <= nbNeigh:
        i = scp.random.random_integers(0,N-1)
        Neigh = permuteOne(path,i)
        if Neigh not in ltaboo:
            nb += 1
            d = evalue(coords,Neigh)
            if (d < bestDist):
                bestV = Neigh
                bestDist = d
    return (bestV,bestDist)

# Exchange 2 cities
# use permuteTwo
# generate nbNeigh
# pre-condition :
#   - path : Course order of cities
#   - i index of the city to put at the end of the course
#   - ltaboo : taboo list of path already traveled
# post-condition : new course order
def bestNeighor2(path, nbNeigh, ltaboo):
    global bestV, bestDist
    nb = 1
    # case of the first neighbor
    i = scp.random.random_integers(0,N-1)
    j = i
    while (i==j):
        j = scp.random.random_integers(0,N-1)
    
    bestV = permuteTwo(path,i,j)
    bestDist = evalue(coords,bestV)

    while nb <= nbNeigh:
        i = scp.random.random_integers(0,N-1)
        j = i
        while (i==j):
            j = scp.random.random_integers(0,N-1)

        Neigh = permuteTwo(path,i,j)
        if Neigh not in ltaboo:
            nb += 1
            d = evalue(coords,Neigh)
            if (d < bestDist):
                bestV = Neigh
                bestDist = d
    return (bestV,bestDist)

# initializing history lists
Henergy = []      # Energy
Htime = []        # time
Hbest = []        # distance

ltaboo = []       # taboo list

#random distribution of N cities on the map[0..1,0..1]
#x = scp.random.uniform(size=N)
#y = scp.random.uniform(size=N)

# Construction data from the file
(x,y) = parse(df) # x,y are kept as are for graphic display
coords = array(list(zip(x,y)),dtype=float) # We build the table of coordinates (x,y)

# Problem parameters
N = len(coords)    # nomber of cities

# definition of the initial route: increasing order of cities
route = [i for i in range(N)]
# calculation of the initial Energy of the system (the initial distance to be minimized)
dist = evalue(coords,route)
# initialization of the best route
best_route = route[:]
best_dist = dist

# we trace the departure path (initial path)
draw(best_route, best_dist, x, y)


# ##################################### PRINCIPAL LOOP OF THE ALGORITHM ############################

i=0
cptIdem = 0
# initialization of the taboo list
ltaboo.insert(0,best_route)

# main loop of the taboo algorithm
while i <= iterMax: # and cptIdem <= idemMax:
    # get the best Neighbor
    (Neighbor, dist) = bestNeighbor(route, nbNeigh, ltaboo)

	# comparison to the best, if it is better, save it and refresh the figure
    if dist < best_dist:
	    cptIdem = 0
	    best_dist = dist
	    best_route = Neighbor
	    draw(best_route, best_dist, x, y)

    # add to taboo list
    ltaboo.insert(0,Neighbor[:])
    if (len(ltaboo) > ntaboo):
    	ltaboo.pop()

    cptIdem += 1

    # next iteration
    i += 1
    route = Neighbor
    # historization of data
    if i % 10 == 0:
        Henergy.append(dist)
        Htime.append(i)
        Hbest.append(best_dist)

# ##################################### END OF ALGORITHM - DISPLAY RESULTS ############################

# display of the result in the console
dispRes(best_route, best_dist)
# statistics chart
drawStats(Htime, Henergy, Hbest)
