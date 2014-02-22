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


if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

	#  Set Main and Resource directories
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'Resources')
#==============================================================================

#==============================================================================
	#  Image / Sound Resource Loader Functions
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
	# Constant Values
SidePanel	= 200
EnvSize	= (360, 600)
TotalSize 	= (EnvSize [0] + SidePanel, EnvSize [1])
TileSize	= (60, 60)
NumTiles	= (EnvSize[0]/TileSize[0], EnvSize[1]/TileSize[1])
RobSize	= (38, 53)
CentreTiles= np.zeros((NumTiles[0]*NumTiles[1],2))

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

#==============================================================================
	#  Game Object Classes
class YouBot(pygame.sprite.Sprite):
	"""YouBot Sprite"""
	def __init__(self, posx = 200, posy = 200):
		pygame.sprite.Sprite.__init__(self) # Call Sprite Initialiser
		self.image, self.rect = load_image('ball.png', -1)
		self.image = pygame.transform.scale(self.image, (25, 25))
		self.rect = self.image.get_rect()

		self.rect.topleft = (posx, posy)
		
	def update(self, dirxy):
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
	pygame.init()
	screen = pygame.display.set_mode((TotalSize), 0)
	pygame.display.set_caption('Navigation Experiment')
	pygame.mouse.set_visible(1)
	clock = pygame.time.Clock()
	myfont = pygame.font.SysFont("monospace", 10)
	
	youbot = YouBot()
	YouBotsprite = pygame.sprite.RenderPlain(youbot)	
	
	# World Generation
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(WHITE)
	
	locx = 0
	while locx <= EnvSize[0]:
		
		pygame.draw.line(background, BLACK, (locx, 0), (locx, EnvSize[1]))
		locx = locx + TileSize[0]
	
	locy = 0
	while locy <= EnvSize[1]:
	
		pygame.draw.line(background, BLACK, (0, locy), (EnvSize[0], locy))
		locy = locy + TileSize[1]
		
	# Numbering
	y = 0
	x = 0
	for y in range(1, NumTiles[1]+1):
		for x in range(1, NumTiles[0]+1):
			
			CentreTiles[transtonum(x,y)-1] = (TileSize[0]/2 + TileSize[0]*(x-1),TileSize[1]/2 + TileSize[1]*(y-1))
			text = myfont.render(str(int(CentreTiles[transtonum(x,y)-1,0])) + ',' + str(int(CentreTiles[transtonum(x,y)-1,1])), 1, BLACK)

			
			background.blit(text, (CentreTiles[transtonum(x,y)-1,0]-20,CentreTiles[transtonum(x,y)-1,1]))
	
		
	
#==============================================================================
	# Main Loop
	going = True
	while going:			# Main game loop
		clock.tick(60)
		
		screen.blit(background, (0, 0))
		
		YouBotsprite.draw(screen)
		pygame.display.flip()		
		
		
		if pygame.event.peek (QUIT):
			going = False  # Be IDLE friendly

	pygame.quit()
	sys.exit()

#==============================================================================
	#  Run if called

if __name__ == '__main__':
	main()

#==============================================================================