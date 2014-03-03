'''
@author: Miro Mannino

'''

from tkinter import *
from GridWorld import GridWorld
from GUI import MDPGUI
from GUI import MDPChooser

if __name__ == '__main__':
	
	def showhelp():
		hlpStr = ("Markov Decision Process Examples\n"
				  "	Examples:\n"
				  "		gridworld 1: std grid world as the book (step cost -0.04, discount factor 1)\n"
				  "		gridworld 2: low discount factor 0.6 (step cost -0.04)\n"
				  "		gridworld 3: low step cost -0.01\n"
				  "		gridworld 4: suicide mode (step cost -2)\n"
				  )
		print(hlpStr)
		exit()
	
	if len(sys.argv) == 1: showhelp()
	
	if sys.argv[1] == "gridworld":
		
		w = GridWorld([[GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_EXIT], 
				   [GridWorld.CELL_VOID, GridWorld.CELL_WALL, GridWorld.CELL_VOID, GridWorld.CELL_PIT],
				   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID]], discountFactor = 1 )
		
		if len(sys.argv) < 3:
			mdpc = MDPChooser()
		elif sys.argv[2] == "1":	
			w.setRewards(-0.04, -1, 1)
			w.setProbabilities(0.8, 0.1, 0.1, 0)
			w.setDiscountFactor(1)
			g = MDPGUI(w)
		elif sys.argv[2] == "2":
			w.setRewards(-0.04, -1, 1)
			w.setProbabilities(0.8, 0.1, 0.1, 0)
			w.setDiscountFactor(0.9)
			g = MDPGUI(w)
		elif sys.argv[2] == "3":
			w.setRewards(-0.01, -1, 1)
			w.setProbabilities(0.8, 0.1, 0.1, 0)
			w.setDiscountFactor(1)
			g = MDPGUI(w)
		elif sys.argv[2] == "4":	
			w.setRewards(-2, -1, 1)
			w.setProbabilities(0.8, 0.1, 0.1, 0)
			w.setDiscountFactor(0.6)
			g = MDPGUI(w)
		else:
			mdpc = MDPChooser()
		
		mainloop()
	else:
		showhelp()
		
	
	
	#
	
	
	
	
			