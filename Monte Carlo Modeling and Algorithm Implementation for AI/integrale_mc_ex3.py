import numpy as np
import math

nbiterations = 1000000
val = 0
res = 0
for numiter in range(nbiterations):
   x = np.random.uniform(0.0,4.0)   
   y = np.random.uniform(2.0,6.0)
   val = x*math.cos(x)+3*y*math.cos(y)+15;
   res +=val*16	 

   
print("Approximation : ",res/nbiterations)
