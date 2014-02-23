# -*- coding: utf-8 -*-

#==============================================================================
# NavigationExp1 - by Alejandro Bordallo
# Details: First navigation experiment
# TODO: Setup simple environment + agent + obstacle
# TODO: Implement simple navigation algorithm (A*)
#==============================================================================


#==============================================================================
	#import os, pygame, sys, random, numpy
import os, pygame, sys
from pygame.locals import *
import numpy as np

from time import time

import AStar

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

	#  Set Main and Resource directories
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'Resources')
#==============================================================================

#==============================================================================
	#  Image / Sound Resource Loader Functions
def load_image(name, colorkey=None):
	'''Function to load image from resource folder'''
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
	'''Function to load sound from resource folder'''
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
	# Constant Values
SidePanel	= 200				# Size of Information Panel
EnvSize	= (360, 600)		# Size of Experiment Environment
TotalSize 	= (EnvSize [0] + SidePanel, EnvSize [1])
TileSize	= (60, 60)			# Size of InSpace Tiles
TileDiag	= np.sqrt(np.power(TileSize[0],2)+np.power(TileSize[1],2))
NumTiles	= (EnvSize[0]/TileSize[0], EnvSize[1]/TileSize[1])
RobSize	= (38, 58)			# YouBot Size
CentreTiles= np.zeros((NumTiles[0]*NumTiles[1],2))	# Array Containing x,y co-ordinates of Tile centers


WHITE	= (255, 255, 255)
BLACK	= (0, 0, 0)

#==============================================================================
	# Useful Functions

def transtonum(x, y):
	'''Transform Tile x,y index into sequential number'''
	num = (y - 1) * NumTiles[0] + x 
	return num
	
def transtoxy(num):
	'''Transform Tile sequential number into x,y index'''
	y = num // NumTiles[0]
	x = num % NumTiles[0]
	return x, y
	
def fpsshow(name, x, fr=None):
	''' Show current frame on screen '''
	myfont = pygame.font.SysFont("monospace", 15)
	if fr != None:
		text = myfont.render(name + ':' + str(fr), 1, (255, 255, 0))
		screen.blit(text, (x * 15, Pitch[1] - Wallwidth + 10))
	else:
		text = myfont.render(name, 1, (255, 255, 0))
		screen.blit(text, (x * 15, Pitch[1] - Wallwidth + 10))
		
def PotField(mapsize, start=(2,8), goal=(3,0)):
	
	PotMap = np.matrix(np.zeros(mapsize))
	sval = 0
	gval = -1 * max(mapsize[0],mapsize[1])
	#self.Map(start) = 0
	#self.Map(goal) = -1 * mapsize[0]	
	
	for y in range(0, mapsize[0]):
		for x in range(0, mapsize[1]):
			PotMap[y,x] = max(abs(x-goal[0]),abs(y-goal[1])) * 3
			PotMap[y,x] = PotMap[y,x] + max(abs(x-start[0]),abs(y-start[1]))
			
	return PotMap
	
#==============================================================================
	#  Game Object Classes
class YouBot(pygame.sprite.Sprite):
	"""YouBot Sprite"""
	def __init__(self, posx = 125, posy = 475):
		pygame.sprite.Sprite.__init__(self) # Call Sprite Initialiser
		self.image, self.rect = load_image('YouBot.png', -1)
		self.image = pygame.transform.scale(self.image, (RobSize[0]+15, RobSize[1]+15))
		self.rect = self.image.get_rect()

		self.rect.topleft = (posx, posy)
		
	def update(self, nextpos):
		"YouBot movement"
		
		self._move(dirxy)
		
	def _move(self, dirxy):
		"Update position of YouBot"
		currpos = np.matrix(self.rect.center)
		xymat = np.matrix(dirxy)
		self.nextpos = currpos + xymat
		
class Goal(pygame.sprite.Sprite):
	"""Goal Sprite"""
	def __init__(self, posx = 195, posy = 15):
		pygame.sprite.Sprite.__init__(self) # Call Sprite Initialiser
		self.image, self.rect = load_image('goal.png', -1)
		self.image = pygame.transform.scale(self.image, (35, 35))
		self.rect = self.image.get_rect()

		self.rect.topleft = (posx, posy)
		
	def update(self, nextpos):
		"YouBot movement"
		
		self._move(dirxy)
		
	def _move(self, dirxy):
		"Update position of YouBot"
		currpos = np.matrix(self.rect.center)
		xymat = np.matrix(dirxy)
		self.nextpos = currpos + xymat

#==============================================================================
	# Main Process
def main():
	"""this function is called when the program starts. It initializes everything it needs, then runs in a loop until the function returns."""

	# Initialize Everything
	print "Initialising..."
	pygame.init()
	screen = pygame.display.set_mode((TotalSize), 0)
	pygame.display.set_caption('Navigation Experiment')
	pygame.mouse.set_visible(1)
	clock = pygame.time.Clock()
	myfont = pygame.font.SysFont("monospace", 10)
	
	youbot = YouBot()
	YouBotsprite = pygame.sprite.RenderPlain(youbot)

	goal = Goal()
	Goalsprite = pygame.sprite.RenderPlain(goal)	
	
	# World Generation
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(WHITE)
	
	potmap = PotField((NumTiles[1],NumTiles[0]))
	# print("Potential Map:"); print(potmap)	
		
	
	# Numbering of Tiles
	printnum= 0		# Print Tile Number on the center
	printxy = 0		# Print Tile Coordinate on center
	printpot= 1		# Colour Tiles as Potential Field
	
	for y in range(1, NumTiles[1]+1):
		for x in range(1, NumTiles[0]+1):
			
			CentreTiles[transtonum(x,y)-1] = (TileSize[0]/2 + TileSize[0]*(x-1),TileSize[1]/2 + TileSize[1]*(y-1))

			if printnum:	# Print Tile Number on the center
				text = myfont.render(str(int(transtonum(x,y))), 1, BLACK)
				background.blit(text, (CentreTiles[transtonum(x,y)-1,0]-10,CentreTiles[transtonum(x,y)-1,1]))
			if printxy:		# Print Tile Coordinate on center
				text = myfont.render(str(int(CentreTiles[transtonum(x,y)-1,0])) + ',' + str(int(CentreTiles[transtonum(x,y)-1,1])), 1, BLACK)
				background.blit(text, (CentreTiles[transtonum(x,y)-1,0]-20,CentreTiles[transtonum(x,y)-1,1]))
			if printpot:	# Colour Tiles following Potential Field
				col = int(255 * (potmap[y-1,x-1] / 30))
				pygame.draw.rect(background, (col, col, col), (int(CentreTiles[transtonum(x,y)-1,0]-TileSize[0]/2), int(CentreTiles[transtonum(x,y)-1,1]-TileSize[1]/2), int(CentreTiles[transtonum(x,y)-1,0]+TileSize[0]/2), int(CentreTiles[transtonum(x,y)-1,1]+TileSize[1]/2)))
				#pygame.draw.rect(background, (0, 0, 0), (30, 30, 40, 40), 0)	
	
	# print("TileCentres:"); print(CentreTiles)
	
	locx = 0
	while locx <= EnvSize[0]:
		
		pygame.draw.line(background, BLACK, (locx, 0), (locx, EnvSize[1]))
		locx = locx + TileSize[0]
	
	locy = 0
	while locy <= EnvSize[1]:
	
		pygame.draw.line(background, BLACK, (0, locy), (EnvSize[0], locy))
		locy = locy + TileSize[1]
		
	
	#TODO: Add Right Panel White Background (Or figure out why it gets coloured as well with potential field)	
	
				
#==============================================================================
	# Main Loop
	going = True
	print "Main Loop"
	while going:			# Main game loop
		clock.tick(60)
		
		screen.blit(background, (0, 0))
		
				
		
		YouBotsprite.draw(screen)
		Goalsprite.draw(screen)
		pygame.display.flip()		
		
		
		if pygame.event.peek (QUIT):
			going = False  # Be IDLE friendly

	print "Exiting..."
	pygame.quit()
	sys.exit()

#==============================================================================
	#  Run if called

if __name__ == '__main__':
	main()

#==============================================================================