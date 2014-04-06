# -*- coding: utf-8 -*-

#==============================================================================
# Strategy Prototype1- by Alejandro Bordallo
# Details: First strategy prototype: testing world generation, agent navigation
#		resource gathering and coding/debuggin framework
#
# TODO: (ALWAYS) Rename functions/constants/varaibles for good code practice
# TODO: (ALWAYS) COMMENT and REFACTOR everything
#
# TODO: (EASY) Add extra agents to move randomly across the map
# TODO: (EASY) Print sprites sequentially so occlusion works properly (e.g. If
#		agent is behind a tree then draw agent first then tree on top)
# TODO: (EASY) Add sidepanel (from NavExp) for realtime information and GUI
# TODO: (EASY) Randomise placement of objects in the field (Except House/Agent)
# TODO: (MEDIUM) Introduce simple interaction / navigation of agents
# TODO: (MEDIUM) Introduce functions for interaction with rocks/trees
# TODO: (MEDIUM) Add agent functions for carrying/leaving resources
# TODO: (MEDIUM) Add a barn for resource collection, a house every X resources
# TODO: (HARD) Implement A* recursively for each agent (Efficiently!)
# TODO: (HARD) Implement centralised planning for agent actions (Who goes where)
#==============================================================================


#==============================================================================
	# IMPORT LIBRARIES
#******************************************************************************
import os, pygame, sys
from pygame.locals import *
import numpy as np
import time


if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

	#  Set Main and Resource directories
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'Resources')

#==============================================================================
	# CONSTANT VALUES
#******************************************************************************
# Setup Values
FPS = 30				# Frames per second
xres = 600
yres = 600
res = (xres, yres)		# Window Resolution

GRASS = (34, 176, 10)	# Grass Colour

#==============================================================================

#==============================================================================
	# RESOURCE LOADING FUNCTIONS
#******************************************************************************
def load_image(name, colorkey=None):
	fullname = os.path.join(data_dir, name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error:
		print (('Cannot load image:', fullname))
		raise SystemExit(str(geterror()))
	#image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	fullname = os.path.join(data_dir, name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error:
		print (('Cannot load sound: %s' % fullname))
		raise SystemExit(str(geterror()))
	return sound
	
#==============================================================================

#==============================================================================
	#  GAME AGENT AND OBJECT SPRITES
class Villager(pygame.sprite.Sprite):
	"""Main agent, controlled by user"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.image, self.rect = load_image('boy.png', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = (10, 10)
		self.speed = 20
		self.touching = 0
		self.dying = 0

	def update(self,dirxy):
		"Move agent based on key presses or change appearance"
		#pos = pygame.mouse.get_pos()
		#self.rect.midtop = pos
		#if self.punching:
			#self.rect.move_ip(5, 10)
		if self.dying:
			self._dying()
		else:
			self._walk(dirxy)

	def touch(self, target):
		"Returns true if sprite collides with target"
		if not self.touching:
			self.touching = 1
			hitbox = self.rect.inflate(-5, -5)
			return hitbox.colliderect(target.rect)

	def _walk(self, dirxy):
		"Update position of Sprite'"
		#currpos = self.rect.move((self.move, 0))
		currpos = np.matrix(self.rect.center)
		xymat = np.matrix(dirxy)
		nextpos = currpos + xymat * self.speed
		if nextpos[0, 0] > self.area.left and \
		nextpos[0, 0] < self.area.right and \
		nextpos[0, 1] > self.area.top and \
		nextpos[0, 1] < self.area.bottom:
			move = nextpos.tolist()
			self.rect.center = move[0]

	def _dying(self):
		"Add sprite animations of character death = Explosions!"

	def dead(self):
		"Agent has been struck!"
		self.dying = 1
		
class Rock(pygame.sprite.Sprite):
	"""Produces a Rock"""
	def __init__(self, posxy):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
#		Im = pygame.image.load('Resources\hyptosis_tile2.png')
#		self.rect = pygame.Rect(196, 356, 60, 60)	# Select just the rock
#		self.image = Im.subsurface(self.rect)
		self.image, self.rect = load_image('Rock.png', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posxy
		self.touching = 0
		
class Tree(pygame.sprite.Sprite):
	"""Produces a Tree"""
	def __init__(self, posxy):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.image, self.rect = load_image('Tree_Tall.png', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posxy
		self.touching = 0
			
#==============================================================================
	# MAIN FUNCTION
#******************************************************************************
def main():
	"""this function is called when the program starts. It initializes everything it needs, then runs in a loop until the function returns."""
	#************************************************************************
	# INITIALISATION
	pygame.init()
	screen = pygame.display.set_mode((res), 0)
	pygame.display.set_caption('Strategy Prototype 1')
	pygame.mouse.set_visible(1)

	background = pygame.Surface(screen.get_size()) # Background construction
	background = background.convert()
	background.fill(GRASS)
	
	screen.blit(background, (0, 0))	# Display Background
	pygame.display.flip()
	
	#************************************************************************
	# VARIABLES
	frm = 0	# Current frame	

	#************************************************************************
	# GAME OBJECTS
	clock = pygame.time.Clock()

	villager1 = Villager()
	villagersprite = pygame.sprite.RenderPlain((villager1))
	
	rock1 = Rock((100, 100))
	rock2 = Rock((300, 300))
	
	tree1 = Tree((200, 200))
	tree2 = Tree((400, 400))
	
	rocksprite = pygame.sprite.RenderPlain(rock1, rock2)
	treesprite = pygame.sprite.RenderPlain(tree1, tree2)
	
	#************************************************************************
	# MAIN LOOP		
	going = True
	tstart = time.clock()
	tstop = time.clock()
	
	while going:			# Main game loop
		
		clock.tick(60)		# Set frames per second
		if frm >= 30:		# Independent frame counter
			frm = 0
		else:
			frm = frm + 1
		
		screen.blit(background, (0, 0))	# Put background on screen
		
		#******************************************************************
		# KEYBOARD AND MOUSE EVENTS
		
		# Handle Input Events
		dirxy = [0, 0]
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				going = False
				print('User quit the game')
			elif event.type == KEYDOWN:
				keys = pygame.key.get_pressed()
				if keys[K_LEFT]:
					dirxy[0] = dirxy[0] - 1
				if keys[K_RIGHT]:
					dirxy[0] = dirxy[0] + 1
				if keys[K_UP]:
					dirxy[1] = dirxy[1] - 1
				if keys[K_DOWN]:
					dirxy[1] = dirxy[1] + 1
					
		#******************************************************************
		# OBJECTS AND SPRITES		
		villagersprite.update(dirxy)
		# rocksprite.update()
		# treesprite.update()
		
		# Draw Everything
		rocksprite.draw(screen)
		treesprite.draw(screen)
		villagersprite.draw(screen)

		pygame.display.flip()	# Display all


	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()