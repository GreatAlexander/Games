# -*- coding: utf-8 -*-

import numpy as np

class PotField:
	
	def __init__(self, mapsize=(4, 4), start=(0,0), goal=(mapsize[0],mapsize[1])):
		self.Map = np.matrix(np.zeros(mapsize))
		sval = 0
		gval = -1 * mapsize[0]
		#self.Map(start) = 0
		#self.Map(goal) = -1 * mapsize[0]
		
		for y in range(0, mapsize[1]):
			for x in range(0, mapsize[0]):
				self.Map(x,y) = max(abs(x-start[0]),abs(y-start[1]))
				self.Map(x,y) = self.Map(x,y) + gval + max(abs(x-goal[0]),abs(y-goal[1]))
		
		