import numpy as np

nbiterations = 1000000
val_pi = 0.0
for numiter in range(nbiterations):
	x = np.random.uniform(0.0,1.0)   
	y = np.random.uniform(0.0,1.0)
	if ((x*x + y*y) <= 1.0) :
		val_pi += 1 

   
print("Approximation of PI : ",val_pi*4/nbiterations)
