import numpy as np

nbiterations = 1000000
val = 0
for numiter in range(nbiterations):
   x = np.random.uniform(1.0,4.0)   
   y = x*x*x-5*x*x+20
   val +=y*3	 

   
print("Approximation : ",val/nbiterations)
