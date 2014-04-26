import Global
import Loader
import MovingObject
import AI
import PygameWrapper as pygw

class Agent(MovingObject.MovingObject):
	""" Agent class for players on the field """
	def __init__(self, posxy, playerid, orientation = -90):
		MovingObject.MovingObject.__init__(self)

		self.player_icon(playerid)
		self.load_image()
		self.rect.center = (posxy[0], posxy[1])
		self.image = pygw.rotate(self.image, orientation)

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
		self.position = self.rect.center