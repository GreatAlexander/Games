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
	def __init__(self, loglength = 9000, listlength = 11):
		self.tstamp = 0	# To be used for logging and replaying
		self.max_loglength = loglength

		self.world_data = [0., 0.], 0., 0., [0., 0.], 0., [0., 0.], 0., [0., 0.], 0., [0., 0.], 0.
		self.world_data = np.resize(self.world_data,(loglength,listlength))

	def update_info(self, ball_pos, ball_speed, ball_angle, blue1_pos, \
	blue1_angle, blue2_pos, blue2_angle, red1_pos, red1_angle, \
	red2_pos, red2_angle):

		self.tstamp += 1
		if self.tstamp <= self.max_loglength:
			self.world_data[self.tstamp,:] = ball_pos, ball_speed, ball_angle, \
			blue1_pos, blue1_angle, blue2_pos, blue2_angle, red1_pos, red1_angle, \
			red2_pos, red2_angle
		else:
			print('WARNING: Maximum Log Size for World Model reached')

	def request_info(self):
		return self.world_data[self.tstamp,:]