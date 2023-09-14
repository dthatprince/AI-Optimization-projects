
from scipy import *
from math import *
from functools import *
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import sys


DIM = 4    # dimension of the problem
INF = -600
SUP = 600

Nb_cycles = 1000
Nb_flowers = 10
MaxVisites = 50

nbOnlookers = Nb_flowers
nbemploy = Nb_flowers
nbscout = 2

# Instance of the problem
if (len(sys.argv) > 1):
    FONCTION=sys.argv[1]
else:
    print("No specified file...")
    sys.exit("USE : python PSOCONT.py sphere|griewank")

# Displays the best solution found
# pre-conditions:
# - best: best solution found,
def dispRes(best):
    print("point = {}".format(best['pos']))
    print("eval = {}".format(best['eval']))
	   
def sphere(sol):
    return reduce(lambda acc,e:acc+e*e,sol,0)

def griewank(sol):
    (s,p,i) = reduce(lambda acc,e:(acc[0]+e*e,acc[1]*cos(e/sqrt(acc[2])),acc[2]+1),sol,(0,1,1))
    return s/4000
	
# Evaluation function,
# pre-condition:
# - sol: point of the plan
# post-condition: f (point)
def eval(sol):
    global FONCTION
    if FONCTION == "sphere":
        return sphere(sol)
    elif FONCTION == "griewank":
        return griewank(sol)
    else:
        print("error!")
        exit(1)

# Bounding function that stops the value at the limits of the search space
def bounding(val, inf, sup):
	return min (sup, max (inf, val))

# fitness (pb of minimization)
def fitness(ev):
	if (ev >= 0):
		return 1. / (ev + 1.)
	else:
		return (abs(ev) + 1.)

# Create a flower (food source)
# a flower is described by:
# - pos: solution list of variables
# - eval: eval of the rectangle
# - fit: fitness of the solution
# - nbvis: number of non-improvement visits of the flower
# - proba: probability of being selected at the foraging stage, depends on the fitness
def initOne(dim, inf, sup):
    pos = [random.uniform(inf, sup) for i in range(dim)]
    ev = eval(pos)
    return {'pos':pos, 'eval':ev, 'fit':fitness(ev), 'nbvis':0, 'proba':0}

# Init of the population
def initGarden(nb, dim, inf, sup):
	return [initOne(dim,inf,sup) for i in range(nb)]

# Return a flower with a best fitness
def bestIndiv(p1,p2):
	if (p1["fit"] > p2["fit"]):
		return p1 
	else:
		return p2

# Returns a copy of the flower with the best fitness in the population
def getBest(garden):
	return dict(reduce(lambda acc, e: bestIndiv(acc,e),garden[1:],garden[0]))

# Sum of fitness of the population (for proba calculation)
def somFitness(garden):
	return reduce(lambda a,e: a+e['fit'],garden,0)

# Calculates the probas of the population (percentage of total fitness)
def updateProbaSum(garden):
	somfit = somFitness(garden) # sum of all the fitness of the flowers of the garden
	return list(map(lambda e: {'pos':e['pos'][:], 'eval':e['eval'], 'fit':e['fit'], 'nbvis':e['nbvis'], 'proba':e['fit']/somfit}, garden))

# Calculate the probas of the population
def updateProba(garden):
	return updateProbaSum(garden)

# Generate a neighbor solution
def forage(flower, garden):
	global Nb_flowers

	# we will randomly choose another flower <> to modify a dim of the selected one
	neighbor = flower
	while(neighbor == flower):
		neighbor = garden[random.randint(0,Nb_flowers)]
	
	# copy of the original
	newFlower = dict(flower)

	sol = newFlower["pos"][:] # we retrieve the variables
	# random dimension to modify
	dim2exchange = random.randint(0,len(sol))
	# calculation of the offset to apply		
	val = sol[dim2exchange];
	valNeighb = neighbor["pos"][dim2exchange]
	shift = (val - valNeighb) * (2*random.uniform() - 1)

	# application of the modification with boundary delimitation
	sol[dim2exchange] = bounding(val + shift, INF, SUP)
		
	# we set the calculated values
	ev = eval(sol)
	newFlower["eval"] = ev
	newFlower["pos"] = sol
	newFlower["fit"] = fitness(ev)
	newFlower["proba"] = 0
	newFlower["nbvis"] = 0
	
	# replacement if better fitness,
	# otherwise, return the previous one by incrementing cpt visits
	if (newFlower["fit"] > flower["fit"]):
		return newFlower
	else:
		flower["nbvis"] += 1
		return flower


# For each flower, look in the neighborhood if the counter of visits allows it
def sendEmployed(fl,garden):
	global MaxVisites
	if (fl["nbvis"] < MaxVisites):
		return forage(fl, garden)
	else:
		return fl

# Step employeds, we visit all the flowers
def sendEmployeds(garden):
	return list(map(lambda e: sendEmployed(e,garden),garden))

# Step onlooker, we visit the flowers according to their sexytude
def sendOnloockers(nbOnlookers, garden):
	global Nb_flowers, MaxVisites
	i = 0 # iterateur pour les flowers
	t = 0 # iterateur pour les forageuses

	# Forager phase
	while (t < nbOnlookers):
		flower = garden[i]
		# we choose a flower according to its proba
		r = random.uniform()
		if (r <= flower['proba']): 
			garden[i] = forage(garden[i], garden)
			# we go to the next onlooker
			t += 1 
		# next flower, if the list of sources is totally visited, we start again at the beginning
		i = (i+1) % Nb_flowers 
	return garden

# Step scouts, we return the index of the most visited flower
def mostVisited(garden):
	global Nb_flowers
	worstFlower = 0;
	for i in range(1,Nb_flowers): 
		if(garden[worstFlower]['nbvis'] < garden[i]['nbvis']): 
			worstFlower = i
	return worstFlower

# Step scouts, we replace the most visited flower beyond the maximum by a newFlower flower
def sendScouts(nbscout, garden):
	global MaxVisites,DIM,INF,SUP
	for i in range(nbscout):
		worstFlower = mostVisited(garden)
		if (garden[worstFlower]['nbvis'] >= MaxVisites):
			flower = initOne(DIM,INF,SUP)
			garden[worstFlower] = flower
	return garden

# initialization of the population
garden = initGarden(Nb_flowers,DIM,INF,SUP)
# initialization of the best solution
best = getBest(garden)
cpt = 0

for i in range(Nb_cycles): 
	# Step  employeds: all solutions
	garden = sendEmployeds(garden)

	# Update the probas
	garden = updateProba(garden)
	
	# Step onlookers: solution according to sexytude
	garden = sendOnloockers(nbOnlookers, garden)

	# Step Scouts: generating a newFlower solution
	garden = sendScouts(nbscout, garden)
	
	# Update the best
	besttour = getBest(garden)
	if (besttour["fit"] > best["fit"]):
		cpt+=1
		best = besttour
		

dispRes(best)
