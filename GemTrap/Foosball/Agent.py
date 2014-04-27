from Global import *
import Loader
import MovingObject
from AIModule import AIModule
import PygameWrapper as pygw

class Agent(MovingObject.MovingObject):
	""" Agent class for players on the field """
	def __init__(self, posxy, playerid, orientation, WMSubscriber):
		MovingObject.MovingObject.__init__(self)

		self.player_icon(playerid)
		self.load_image()
		self.rect.center = (posxy[0], posxy[1])
		self.image = pygw.rotate(self.image, orientation)

		self.player_id = playerid
		self.pos = posxy
		self.angle = orientation

		self.WorldModel = WMSubscriber


	def load_image(self):
		self.image, self.rect = Loader.load_image(self.name, -1)
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

	def update(self):
		self.AI = AIModule(self.player_id, self.WorldModel)
		# Check for new command
		self.AI.update_info()
#		self.AI.state_machine()
#		self.new_command = self.AI.request_command()

		# Execute command
#		self.pos = next_pos
#		self.angle = orientation
