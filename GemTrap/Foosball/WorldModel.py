# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 16:43:52 2014
# World Model Module including the latest world information used by the players
@author: AlexBEAST
"""

from Global import *
import numpy as np

class WorldModel(object):
	""" World Model containing all of the up to date information relevant to
		the agents. It is from here they request information (i.e. Vision)
		and post information about their strategies (for the referee).
		The information is kept with a time stamped log, which can then
		be used for later analysis or replaying of matches"""
	def __init__(self):
		self.world_data = []

	def update_info(self, dataList):
		currentWorld = {}
		for item in dataList:
			item.updateCurrentWorld(currentWorld)
		
		self.world_data.append(currentWorld)
		
	def request_info(self):
		return self.world_data