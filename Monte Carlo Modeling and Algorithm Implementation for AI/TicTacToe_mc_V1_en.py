#TicTacToe by the simple Monte Carlo method 
import numpy as np
#we define a state by a 3*3 array in which each box contains 
#'', 'X' ou '0'
#This function allows you to say if a move is valid or not. 
def valid(tab):
    val = True
    
    sh = tab.shape
    if (sh!=(3,3)):
      val = False
      
    nbX = 0
    nbO = 0
    for lnum in range(3):
      for cnum in range(3):
        if (tab[lnum,cnum] not in ['','X','O']):
          val = False
          break
        elif (tab[lnum,cnum]=='X'):
          nbX = nbX+1
        elif (tab[lnum,cnum]=='O'):
          nbO = nbO+1

    if ((nbX-nbO) not in [-1, 0, 1]):
      val = False	
    return val

# The following function tells us if there are three aligned values
# It returns either the aligned symbol X or O,
# Or no 3 boxes aligned so this function returns N 
def threeAlign(tab):
   if ((tab[0,0]==tab[0,1]) & (tab[0,0]==tab[0,2]) & (tab[0,0]!='')):
     val = tab[0,0]
   elif ((tab[1,0]==tab[1,1]) & (tab[1,0]==tab[1,2]) & (tab[1,0]!='')):
     val = tab[1,0]
   elif ((tab[2,0]==tab[2,1]) & (tab[2,0]==tab[2,2]) & (tab[2,0]!='')):
     val = tab[2,0]
   elif ((tab[0,0]==tab[1,0]) & (tab[0,0]==tab[2,0]) & (tab[0,0]!='')):
     val = tab[0,0]
   elif ((tab[0,1]==tab[1,1]) & (tab[0,1]==tab[2,1]) & (tab[0,1]!='')):
     val = tab[0,1]
   elif ((tab[0,2]==tab[1,2]) & (tab[0,2]==tab[2,2]) & (tab[0,2]!='')):
     val = tab[0,2]
   elif ((tab[0,0]==tab[1,1]) & (tab[0,0]==tab[2,2]) & (tab[0,0]!='')):
     val = tab[0,0]
   elif ((tab[0,2]==tab[1,1]) & (tab[0,2]==tab[2,0]) & (tab[0,2]!='')):
     val = tab[0,2]
   else:
     val = 'N'
	 
   return val



#the following function returns the list of empty cells 
def celEmpty(tab):
   lstEmpty = []
   for lnum in range(3):
     for cnum in range(3):
       if (tab[lnum,cnum]==''):
         lstEmpty.append((lnum, cnum))
         
   return lstEmpty

#Initialize a game 
#declare a list of 9 elements equal to '' 
#transform this array into a 3x3 matrix with numpy's reshape function 

def initGame():
  l = ['']*9
  tab = np.array(l)
  tab = tab.reshape(3,3)
  return tab
  
#This function displays the grid 
def displayGrid(tab):
  print('|',tab[0,0],'|',tab[0,1],'|',tab[0,2],'|')
  print('|',tab[1,0],'|',tab[1,1],'|',tab[1,2],'|')
  print('|',tab[2,0],'|',tab[2,1],'|',tab[2,2],'|')

#Associate a number to a state
#Metode to choose and guide the direction of the game 
def calculerNum(tab):
  exp = 0
  num = 0
  for lnum in range(3):
    for cnum in range(3):
      if (tab[lnum,cnum]=='X'):
        num = num+2**exp
      elif (tab[lnum,cnum]=='O'):
        num = num+2**(exp+1)
      exp = exp+2
  return num
    
#Main script
tab = initGame()

#We play one random game 
nbMoves = 0
playernum = 0
while ((nbMoves<9)&(threeAlign(tab)=='N')):
  print('Player : ',playernum+1)
  lstEmpty = celEmpty(tab)
  pos = np.random.randint(len(celEmpty(tab)))
  cel = lstEmpty[pos]
  if (playernum==0):
    tab[cel]='X'
  else:	
    tab[cel]='O'
#Dislay the grid
  displayGrid (tab)
  playernum = 1-playernum
  nbMoves = nbMoves+1
  
if (threeAlign(tab)!='N'):
  if (threeAlign(tab)=='X'):
    print('Winner : player 1 (X)')
  else:
    print('Winner : player 2 (O)')
else:
  print('Tie game!')
  
    