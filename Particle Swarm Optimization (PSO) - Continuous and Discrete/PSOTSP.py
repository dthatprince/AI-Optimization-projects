
from scipy import *
from math import *
from matplotlib.pyplot import *
from functools import *
import sys
import random as rnd

# Instance of the problem
#FIC="NUMBER.tsp"
if (len(sys.argv) > 1):
    FIC=sys.argv[1]
else:
    print("No  specifie filed...")
    sys.exit("USAGE : python RSTSP.py instance_number.tsp")

# ################ PSO prameters ###################

# params contrition factor
ksi, c1, c2 = 0.7298844, 2.05, 2.05
# usual parameters
psi,cmax = (0.7, 1.47) 
# psi,cmax = (0.8, 1.62)
# psi,cmax = (1, 1) 
# ###################################################

# Creating figure
TPSPause = 0.1 # for displying
fig1 = figure()
canv = fig1.add_subplot(1,1,1)
xticks([])
yticks([])

# Parse the data file
# pre-condition: filename: filename (must exist)
# post-condition: (x,y) city coordinates
def parse(nameFile):
    absc=[]
    ordo=[]
    with open(nameFile,'r') as intFile:
        for line in intFile:
            absc.append(float(line.split(' ')[1]))
            ordo.append(float(line.split(' ')[2]))
    return (array(absc,dtype=float),array(ordo,dtype=float))


# Displays the coordinates of the waypoints as well as the best route found and its length
# pre-conditions:
# - best_route, best_dist: best route found and its length,
def dispRes(best):
    print("route = {}".format(best['bestpos']))
    print("distance = {}".format(best['bestfit']))

# Refreshes the figure of the route, we draw the best route found
# pre-conditions:
# - best_route, best_dist: best route found and its length,
# - x, y: path point coordinate arrays
def draw(best_route, best_dist, x, y):
    global canv,lx,ly
    canv.clear()
    canv.plot(x[best_route],y[best_route],'k')
    canv.plot([x[best_route[-1]], x[best_route[0]]],[y[best_route[-1]], \
      y[best_route[0]]],'k')
    canv.plot(x,y,'ro')
    title("Distance : {}".format(best_dist))
    pause(TPSPause)


# Figure of the graphs of:
# - the set of energies of the retained fluctuations
# - the best energy
def drawStats(Htime, Hbest):
    # display of evolution curves
    fig2 = figure(2)
    subplot(1,1,1)
    semilogy(Htime, Hbest)
    title('Evolution of the best distance')
    xlabel('Time')
    ylabel('Distance')
    show()

# Factorization of total distance calculation functions
# pre-condition: p1(x1,y1),p2(x2,y2) city coordinates
# post-condition: Euclidean distance between 2 cities
def distance(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Function for calculating the length of the route,
# pre-condition:
# - coords: coordinates of the points of the path
# - route: order of route of the cities
# post-condition: Pb of the VC: the total distance of the route
def eval(coords,route,dim):
    longueur = 0.0
    coord = coords[route]
    for i in range(-1,dim-1): #we calculate the distance by closing the loop
        longueur += distance(coord[i], coord[i+1])
    return longueur

# Create a particle
# a particle is described by:
# - pos: variable list solution
# - speed: movement speed (null at initialization)
# - fit: area of the rectangle
# - bestpos: best configuration visited
# - bestfit: evaluation of the best configuration visited
# - bestneighb: best neighbor (global for this version)
def initOne(dim,coords):
    pos = rnd.sample(range(dim),dim)
    fit = eval(coords,pos,dim)
    return {'velocity':[], 'pos':pos, 'fit':fit, 'bestpos':pos, 'bestfit':fit, 'bestneighb':[]}

# Swarm initialization
def initswarm(nb,dim,coords):
    return [initOne(dim,coords) for i in range(nb)]

# Returns the best fitness particle
def maxPartic(p1,p2):
    if (p1["fit"] < p2["fit"]):
        return p1 
    else:
        return p2

# Returns a copy of the best fitness particle in the population
def getBest(swarm):
    return dict(reduce(lambda acc, e: maxPartic(acc,e),swarm[1:],swarm[0]))

# Updated intFileo for population particles
def maj(partic,bestpart):
    nv = dict(partic)
    if(partic["fit"] < partic["bestfit"]):
        nv['bestpos'] = partic["pos"][:]
        nv['bestfit'] = partic["fit"]
    nv['bestneighb'] = bestpart["bestpos"][:]
    return nv

def localUpdate(partic,swarm,nb,nb_neighbors):
    i = swarm.index(partic)
    l = [swarm[(i+j)%nb] for j in range(1,nb_neighbors+1)]
    bestpart = getBest(l)
    nv = dict(partic)
    if(partic["fit"] < partic["bestfit"]):
        nv['bestpos'] = partic["pos"][:]
        nv['bestfit'] = partic["fit"]
    nv['bestneighb'] = bestpart["bestpos"][:]
    return nv


def minus(pos1, pos2):
    d = len(pos1)
    resSpeed = []
    poscopie = pos1[:]
    for i in range(d):
        e = pos2[i]
        j = poscopie.index(e)
        if (i!=j):
            resSpeed.append((i,j))
            poscopie[i], poscopie[j] = poscopie[j], poscopie[i]

    return resSpeed

def plus(velocity1, velocity2):
    resSpeed = velocity1 + velocity2
    return resSpeed

def ntime(k, velocity):
    resSpeed = []
    while(k>=1):
        # resSpeed = resSpeed + velocity
        k -= 1
    tronc = int(round(k*len(velocity)))
    for i in range(tronc):
        resSpeed.append(velocity[i])
    return resSpeed

def move(part, velocity):
    partres = part[:]
    for (i,j) in velocity:
        partres[i], partres[j] = partres[j], partres[i]        
    return partres

# Calculate the speed and displacement of a particle
def deplace(partic,dim,coords):
    global ksi,c1,c2,psi,cmax
    
    nv = dict(partic)

    # velocityesse = plus(ntime(psi,partic["velocity"]), \
    #                 plus(ntime(cmax*random.uniform(),minus(partic["bestpos"], partic["pos"])), \
    #                     ntime(cmax*random.uniform(),minus(partic["bestneighb"],partic["pos"]))))
    velocityesse = plus(ntime(ksi,partic["velocity"]),plus(ntime(c1*random.uniform(),minus(partic["bestpos"], partic["pos"])),ntime(c2*random.uniform(),minus(partic["bestneighb"],partic["pos"]))))
    position = move(partic['pos'], velocityesse)    

    nv['velocity'] = velocityesse
    nv['pos'] = position
    nv['fit'] = eval(coords,position,dim)

    return nv

# ################### ALGORITHM INITIALIZATION ###########
# Build data from file
(x,y) = parse(FIC) # x,y are kept as is for graphical display
coords = array(list(zip(x,y)),dtype=float) # We build the table of coordinates (x,y)



# Parameter of the problem
dim = len(x)    # number of cities
Nb_cycles = 1000*dim
Nb_partic = 10+2*int(ceil(sqrt(dim)))
nb_neighbors = 3
Htime = []       # time
Hbest = []        # distance

# ############# MAIN ALGORITHM LOOP #############

# swarm initialization
swarm = initswarm(Nb_partic,dim,coords)
# initialization of the best solution 
best = getBest(swarm)
best_cycle = best

# we trace the starting path
draw(best['bestpos'], best['bestfit'], x, y)

for i in range(Nb_cycles):
    # intFileormation update
    # swarm = [update(e,best_cycle) for e in swarm]
    swarm = [localUpdate(e,swarm,Nb_partic,nb_neighbors) for e in swarm]
    # speed and displacement calculations
    swarm = [deplace(e,dim,coords) for e in swarm]
    # Updated the best solution
    best_cycle = getBest(swarm)
    if (best_cycle["bestfit"] < best["bestfit"]):
        best = best_cycle
        draw(best['bestpos'], best['bestfit'], x, y)

    # data logging
    if i % 10 == 0:
        Htime.append(i)
        Hbest.append(best['bestfit'])


# ############# END OF ALGORITHM - DISPLAY OF RESULTS ########
# console display of the result
dispRes(best)
# statistics graph
drawStats(Htime, Hbest)
