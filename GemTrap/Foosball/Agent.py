from Global import *
import Loader
import MovingObject
import numpy as np
from AIModule import AIModule
import PygameWrapper as pygw

class Agent(MovingObject.MovingObject):
	""" Agent class for players on the field """
	def __init__(self, posxy, playerid, angle, WMSubscriber):
		MovingObject.MovingObject.__init__(self)

		self.player_icon(playerid)
		self.load_image()
		self.rect.center = (posxy[0], posxy[1])
		
		self.orientation = self.abs_to_agent(angle)
		self.or_image = self.image
		self.image = pygw.rotate(self.or_image, self.orientation)
		

		self.player_id = playerid
		self.pos = posxy
		self.angle = angle # ANGLE = [0 to 360 Clockwise]

		self.WorldModel = WMSubscriber
		
		self.AI = AIModule(self.player_id, self.WorldModel)
		
		self.speed_rotation = 0.5
		self.speed_forward = 2.
		self.cnt = 30
		self.command = 'Wait'


	def load_image(self):
		self.image, self.rect = Loader.load_image(self.name)
		self.image = pygw.transform(self.image, (75, 75))

	def player_icon(self, playerid):
		if playerid == 1:
			self.name = 'BlueDefender.png'
		elif playerid == 2:
			self.name = 'BlueAttacker.png'
		elif playerid == 3:
			self.name = 'RedDefender.png'
		elif playerid == 4:
			self.name = 'RedAttacker.png'
			
	def agent_to_abs(self, agent_angle):
		if agent_angle < 0:
			absolute_angle = agent_angle * -1
		elif agent_angle >= 0:
			absolute_angle = 360 - agent_angle
			
		return absolute_angle
			
	def abs_to_agent(self, absolute_angle):
		if absolute_angle < 180:
			agent_angle = absolute_angle * -1
		elif absolute_angle >= 180:
			agent_angle = 360 - absolute_angle
			
		return agent_angle
		
	def update_AI(self):
		# Check for new command
		self.AI.update_info(self.angle)
		
		self.cnt += 1
		if self.cnt >= 5:
			self.command = self.AI.request_command()
			self.cnt = 0
		
#	def new_angle(self):
#		curr_angle = self.angle
#		new_angle = curr_angle
#		
#		if self.command is 'Left':
#			new_angle = curr_angle - self.speed_rotation
#		elif self.command is 'Right':
#			new_angle = curr_angle + self.speed_rotation
#		
#		return new_angle
		
	def getNextPosition(self, xymod):
		currentPosition = np.matrix(self.rect.center)
		self.nextPosition = currentPosition + xymod
		
	def new_pos(self):
		"Update position of agent"
		xymod = self.computeDynamics()
		self.getNextPosition(xymod)
		
		move = self.nextPosition.tolist()
		
		return move[0]
		
	def computeDynamics(self):
		self.angle %= 360
		angle = self.angle % 90
		if self.angle >= 0 and self.angle < 90 or self.angle >= 180 and self.angle < 270:
			xmod = self.speed_forward * np.sin(np.deg2rad(angle))
			ymod = self.speed_forward * np.cos(np.deg2rad(angle))
		elif self.angle >= 90 and self.angle < 180 or self.angle >= 270 and self.angle <= 360:
			xmod = self.speed_forward * np.cos(np.deg2rad(angle))
			ymod = self.speed_forward * np.sin(np.deg2rad(angle))
		xy = self.getXY()
			
		return np.matrix((xmod*xy[0], ymod*xy[1]))

	def getXY(self):
		if self.angle >= 0 and self.angle < 90:
			return [1, -1]
		elif self.angle >= 90 and self.angle < 180:
			return [1, 1]
		elif self.angle >= 180 and self.angle < 270:
			return [-1, 1]
		elif self.angle >= 270 and self.angle <= 360:
			return [-1, -1]

	def update(self):
		
		self.update_AI()
		
		new_pos = self.rect.center
		dir_mod = 0
		
#		if self.command is not 'Wait':
#			new_angle = self.new_angle()
			
		if self.command is 'TurnLeft':
			dir_mod = 1
		elif self.command is 'TurnRight':
			dir_mod = -1
		elif self.command is 'Forward':
			new_pos = self.new_pos()
			
#			new_orientation = 0
		
		new_orientation = self.orientation + dir_mod * self.speed_rotation		
		
		if new_orientation < -180:
			new_orientation = 180
		elif new_orientation > 180:
			new_orientation = -180
		old_center = (new_pos[0], new_pos[1])
		self.image = pygw.rotate(self.or_image, new_orientation)
		self.rect = self.image.get_rect()
		self.rect.center = old_center
		
		
		self.orientation = new_orientation
		self.angle = self.agent_to_abs(self.orientation)
		self.pos = new_pos

		
#		self.target_pos, self.target_angle = self.AI.request_command()

		# Execute command
#		self.pos = next_pos
#		self.angle = orientation
