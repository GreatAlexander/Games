# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:07:08 2014
# AI Module containing State Machine for selecting Attacker/Defender Behaviours
@author: AlexBEAST
"""
from Global import *
import numpy as np
#from WorldModel import WorldModel

class AIModule(object):
	""" State Machine that contains the behaviours and transfers between
		them according to the given information """
	def __init__(self, playerid, WMSubscriber):
		if playerid == 1 or playerid == 3:
			self.player = 'Defender'
		else:
			self.player = 'Attacker'
		if playerid <= 2:
			self.team = 'Blue'
		else:
			self.team = 'Red'

		if playerid == 1:
			self.start_pos = BLUE1_START_POS
		elif playerid == 2:
			self.start_pos = BLUE2_START_POS
		elif playerid == 3:
			self.start_pos = RED1_START_POS
		elif playerid == 4:
			self.start_pos = RED2_START_POS

		self.WorldModel = WMSubscriber

	def update_info(self):
		worldModel = self.WorldModel.request_info()[-1]
		self.ball_pos = worldModel["ball"].center
		self.ball_speed = worldModel["ball"].speed
		self.ball_angle = worldModel["ball"].orientation
		self.blue1_pos = worldModel["blue1"].pos
		self.blue1_angle = worldModel["blue1"].orientation
		self.blue2_pos = worldModel["blue2"].pos
		self.blue2_angle = worldModel["blue2"].orientation
		self.red1_pos = worldModel["red1"].pos
		self.red1_angle = worldModel["red1"].orientation
		self.red2_pos = worldModel["red2"].pos
		self.red2_angle = worldModel["red2"].orientation

	def state_machine(self):
		if self.player is 'Attacker':
			if self.ball_is_reachable:
				self.attacker_behaviour_movetoball()
			elif self.player_is_displaced:
				self.attacker_behaviour_goback()
			else:
				self.attacker_behaviour_wait()

		if self.player is 'Defender':
			if self.ball_is_reachable:
				self.attacker_behaviour_movetoball()
			elif self.player_is_displaced:
				self.attacker_behaviour_goback()
			else:
				self.attacker_behaviour_wait()

	def ball_is_reachable(self):
#		if self.ball_pos[0] <= blue quadrant
		return True

	def defender_behaviour_movetoball(self):
		empty = 0

	def attacker_behaviour_movetoball(self):
		empty = 0

	def defender_behaviour_goback(self):
		empty = 0

	def attacker_behaviour_goback(self):
		empty = 0

	def defender_behaviour_wait(self):
		empty = 0

	def attacker_behaviour_wait(self):
		empty = 0
