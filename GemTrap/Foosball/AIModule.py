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

		if self.player is 'Defender' and self.team is 'Blue':
			self.start_pos = BLUE1_START_POS
			self.start_angle = BLUE_START_ANGLE
			self.left_side = BLUE1_LEFT_SIDE
			self.right_side = BLUE1_RIGHT_SIDE
		elif self.player is 'Attacker' and self.team is 'Blue':
			self.start_pos = BLUE2_START_POS
			self.start_angle = BLUE_START_ANGLE
			self.left_side = BLUE2_LEFT_SIDE
			self.right_side = BLUE2_RIGHT_SIDE
		elif self.player is 'Defender' and self.team is 'Red':
			self.start_pos = RED1_START_POS
			self.start_angle = RED_START_ANGLE
			self.left_side = RED1_LEFT_SIDE
			self.right_side = RED1_RIGHT_SIDE
		elif self.player is 'Attacker' and self.team is 'Red':
			self.start_pos = RED2_START_POS
			self.start_angle = RED_START_ANGLE
			self.left_side = RED2_LEFT_SIDE
			self.right_side = RED2_RIGHT_SIDE

		self.WorldModel = WMSubscriber

		self.target_approach_angle = 4
		self.target_approach_distance = AGENT_RADIUS
		self.ball_distance_tolerance = AGENT_RADIUS
		self.move_tolerance = 6
		self.angle_tolerance = 4
		self.kick_angle_tolerance = 6
		self.kick_distance_tolerance = AGENT_RADIUS
		self.kick_timer = FPS * 1
		self.recharge_timer = 0

	def update_info(self, angle):
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

		if self.player is 'Defender' and self.team is 'Blue':
			self.curr_pos = self.blue1_pos
			self.curr_angle = self.blue1_angle
		elif self.player is 'Attacker' and self.team is 'Blue':
			self.curr_pos = self.blue2_pos
			self.curr_angle = self.blue2_angle
		elif self.player is 'Defender' and self.team is 'Red':
			self.curr_pos = self.red1_pos
			self.curr_angle = self.red1_angle
		elif self.player is 'Attacker' and self.team is 'Red':
			self.curr_pos = self.red2_pos
			self.curr_angle = self.red2_angle


		self.curr_angle = angle	# WORLD MODEL FAULT - FIX THAT FIRST!

	def request_command(self):
		self.state_machine()
		command = self.path_planning()

		return command
#		return self.target_pos, self.target_angle

# STATE MACHINE
	def state_machine(self):
		if self.recharging_kick():
			self.behaviour_recharge()
		if self.ball_is_infront() and not self.recharging_kick():
			self.behaviour_kick()
		elif self.ball_is_reachable():
			self.behaviour_goto_ball()
		elif self.player_is_displaced():
			self.behaviour_goto_start()
		elif self.player_is_misaligned():
			self.behaviour_align_start()
		else:
			self.behaviour_wait()

#==============================================================================

	def recharging_kick(self):
		if self.recharge_timer <= 0:
			return False
		else:
			return True

	def ball_is_infront(self):
		self.target_pos = self.ball_pos
		self.vector_to_target = self.calc_vector_to_target()
		self.target_angle = self.calc_vect_angle_absolute(self.vector_to_target)
		self.angle_to_target_relative = self.curr_angle - self.target_angle
		self.distance_to_target = self.calc_distance_to_target(self.vector_to_target)

		if abs(self.angle_to_target_relative) <= self.kick_angle_tolerance \
		and abs(self.distance_to_target) <= self.kick_distance_tolerance:
			self.ball_infront = True
		else:
			self.ball_infront = False

		return self.ball_infront

	def ball_is_reachable(self):

		if self.ball_pos[0] >= self.left_side \
		and self.ball_pos[0] <= self.right_side:
			self.ball_reachable = True
		else:
			self.ball_reachable = False

		return self.ball_reachable

	def player_is_displaced(self):

		if (abs(self.curr_pos[0]-self.start_pos[0]) <= self.move_tolerance \
		and abs(self.curr_pos[1]-self.start_pos[1]) <= self.move_tolerance):
			self.player_displaced = False
		else:
			self.player_displaced = True

		return self.player_displaced

	def player_is_misaligned(self):

		if (abs(self.curr_angle-self.start_angle) <= self.angle_tolerance):
			self.player_misaligned = False
		else:
			self.player_misaligned = True

		return self.player_misaligned

	def behaviour_kick(self):
		self.state = 'Kick'
		self.recharge_timer = self.kick_timer
		self.target_pos = self.curr_pos
		self.vector_to_target = self.calc_vector_to_target()
		self.target_angle = self.curr_angle
#		self.target_approach_angle = 4
#		self.target_approach_distance = AGENT_RADIUS + 20

	def behaviour_recharge(self):
		self.state = 'Recharging'
		self.recharge_timer -= 1
		self.target_pos = self.curr_pos
		self.vector_to_target = self.calc_vector_to_target()
		self.target_angle = self.curr_angle
#		self.target_approach_angle = 4
#		self.target_approach_distance = AGENT_RADIUS + 20

	def behaviour_goto_ball(self):
		self.state = 'Goto_Ball'
		self.target_pos = self.ball_pos
		self.vector_to_target = self.calc_vector_to_target()
		self.target_angle = self.calc_vect_angle_absolute(self.vector_to_target)
		self.target_approach_angle = 4
		self.target_approach_distance = self.ball_distance_tolerance

	def behaviour_goto_start(self):
		self.state = 'Goto_Start'
		self.target_pos = self.start_pos
		self.vector_to_target = self.calc_vector_to_target()
		self.target_angle = self.calc_vect_angle_absolute(self.vector_to_target)
		self.target_approach_angle = 2
		self.target_approach_distance = 2

	def behaviour_align_start(self):
		self.state = 'Align_Start'
		self.target_pos = self.curr_pos
		self.vector_to_target = self.calc_vector_to_target()
		self.target_angle = self.start_angle
		self.target_approach_angle = 2
		self.target_approach_distance = 2

	def behaviour_wait(self):
		self.state = 'Wait'
		self.target_pos = self.curr_pos
		self.vector_to_target = self.calc_vector_to_ball()
#		self.target_angle = self.calc_vect_angle_absolute(self.vector_to_target)
		self.target_angle = self.curr_angle
		self.target_approach_angle = 2
		self.target_approach_distance = 2000

	def calc_vector_to_target(self):
		return [self.target_pos[0] - self.curr_pos[0], \
		self.target_pos[1] - self.curr_pos[1]]

	def calc_vector_to_ball(self):
		return [self.ball_pos[0] - self.curr_pos[0], \
		self.ball_pos[1] - self.curr_pos[1]]

	def calc_distance_to_start(self):
		vect = [self.start_pos[0] - self.curr_pos[0], \
		self.start_pos[1] - self.curr_pos[1]]
		distance_to_start = np.sqrt(np.square(vect[0]) + np.square(vect[1]))
		return distance_to_start

	def calc_distance_to_target(self, vect):
		distance_to_target = np.sqrt(np.square(vect[0]) + np.square(vect[1]))
		return distance_to_target

	def calc_vect_angle_absolute(self, vect):
		hyp = np.sqrt(np.square(vect[0]) + np.square(vect[1]))
		xmod = abs(vect[0])
		ymod = abs(vect[1])

		if vect[1] == 0:
			if vect[0] > 0:
				absolute_angle = 90
			else:
				absolute_angle = 270
		elif vect[0] == 0:
			if vect[1] > 0:
				absolute_angle = 180
			else:
				absolute_angle = 0
		else:
			vect_angle = np.rad2deg(np.arctan(ymod/xmod))

			if vect[0] > 0 and vect[1] < 0:
				absolute_angle = 90 - vect_angle
			elif vect[0] > 0 and vect[1] > 0:
				absolute_angle = 90 + vect_angle
			elif vect[0] < 0 and vect[1] > 0:
				absolute_angle = 270 - vect_angle
			elif vect[0] < 0 and vect[1] < 0:
				absolute_angle = 270 + vect_angle

		if hyp == 0:
			absolute_angle = 0

		return absolute_angle

	def path_planning(self):

		self.distance_to_target = self.calc_distance_to_target(self.vector_to_target)
		self.angle_to_target_absolute = self.calc_vect_angle_absolute(self.vector_to_target)

		self.angle_to_target_relative = self.curr_angle - self.target_angle

		if self.angle_to_target_relative >= self.target_approach_angle:
			return 'TurnLeft'
		elif self.angle_to_target_relative <= -self.target_approach_angle:
			return 'TurnRight'
		elif self.distance_to_target >= self.target_approach_distance:
			return 'Forward'
		elif self.state is 'Kick':
			return 'Kick'
		else:
			return 'Wait'
