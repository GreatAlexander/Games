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
RED   = (255, 0, 0)

#==============================================================================
	# Useful Functions

def transtonum((x, y)):
	'''Transform Tile x,y index into sequential number'''
	num = y * NumTiles[0] + x
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
		
def PotField(mapsize, start, goal):
	
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
	
def findPotpath(start, goal, potmap, rnd = 0):
	path = np.array((start))
	currnode=start
	mapsize = potmap.shape
	n = 0
	while np.array_equal(path[-1], goal) == False:
		nnodes = np.empty(shape=(8,3))
		nnodes[:] = np.NAN
		i = 0
		for y in range(-1, 2):
			if currnode[1] + y < 0 or currnode[1] + y >= mapsize[0]:
				continue
			for x in range(-1, 2):
				if currnode[0] + x < 0 or currnode[0] + x >= mapsize[1]:
					continue
				if potmap[currnode[1] + y, currnode[0] + x] < potmap[currnode[1], currnode[0]]:
					nnodes[i] = [currnode[0] + x, currnode[1] + y, potmap[currnode[1] + y,currnode[0] + x]]
					i = i + 1
#		print "NeighbourNodes:"
#		print nnodes
						
					
		mincost = np.nanmin(nnodes, 0)[2]
#		print "MinCost: %i" % mincost
		if rnd == 0:
			nextind = np.nanargmin(nnodes, 0)[2]
		else:
			minnodes = np.where(nnodes == mincost)
			r = np.random.randint(0, len(minnodes[0]))
			nextind = minnodes[0][r]
#		print "MinNodes:"		
#		print minnodes
#		
#		print "NextIndex: %i" % nextind
#		print " "
		nextpt  = nnodes[nextind, 0:2]
		path = np.vstack((path, nextpt))
		currnode = nextpt
#		print "NextPoint:"
#		print nextpt
		n = n + 1
		if n >= 50:
			print "Break!"
			print path
			break
#	print "Path:"
#	print path
	return path
	
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
		self.speed = np.array((1,1))
		self.xytarg = self.rect.center
		self.ontarget = 0
	
	def setstartxy(self, startxy):
		self.rect.center = startxy	
		self.xytarg = self.rect.center
		
	def setxytarget(self, xycoord):
		"Set YouBot Move target"
		self.xytarg = xycoord
		
	def update(self):
		"YouBot movement update"
		if np.array_equal(self.rect.center, self.xytarg):
			self.ontarget = 1
		else:
			self.ontarget = 0
			
		self._move()
		
	def _move(self):
		"Update position of YouBot"
		self.currpos = np.array(self.rect.center)
		
		xydir = np.array(self.speed)
		xdis = self.xytarg[0] - self.currpos[0]
		ydis = self.xytarg[1] - self.currpos[1]
		
		if self.currpos[0] <= self.xytarg[0]:
			xydir[0] = min([self.speed[0], xdis])
		elif self.currpos[0]>self.xytarg[0]:
			xydir[0] = max([-self.speed[0], xdis])
			
		if self.currpos[1] <= self.xytarg[1]:
			xydir[1] = min([self.speed[1], ydis])
		elif self.currpos[1]>self.xytarg[1]:
			xydir[1] = max([-self.speed[1], ydis])
		
		self.nextpos = self.currpos + xydir
		self.rect.center = self.nextpos
		
class Goal(pygame.sprite.Sprite):
	"""Goal Sprite"""
	def __init__(self, posx = 195, posy = 15):
		pygame.sprite.Sprite.__init__(self) # Call Sprite Initialiser
		self.image, self.rect = load_image('goal.png', -1)
		self.image = pygame.transform.scale(self.image, (35, 35))
		self.rect = self.image.get_rect()

		self.rect.topleft = (posx, posy)
		
	def setstartxy(self, startxy):
		self.rect.center = startxy
		
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

	# Start and Goal positions (Max x=5, Max y=9)	
	start=(4,9)
	goal=(1,0)
	
	youbot = YouBot()
	YouBotsprite = pygame.sprite.RenderPlain(youbot)

	goalsprite = Goal()
	Goalsprite = pygame.sprite.RenderPlain(goalsprite)	
	
	# World Generation
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(WHITE)
	
	

	potmap = PotField((NumTiles[1],NumTiles[0]), start, goal)
	# print("Potential Map:"); print(potmap)

	potpath = findPotpath(start, goal, potmap, 1)	
		
	
	# Numbering of Tiles
	tilefont = pygame.font.SysFont("monospace", 15)
	printnum= 0		# Print Tile Number on the center
	printxy = 0		# Print Tile Coordinate on center
	printpot= 1		# Colour Tiles as Potential Field
	
	for y in range(0, NumTiles[1]):
		for x in range(0, NumTiles[0]):
			
			xy = (x,y)
			CentreTiles[transtonum(xy)] = (TileSize[0]/2 + TileSize[0]*(x),TileSize[1]/2 + TileSize[1]*(y))

			if printnum:	# Print Tile Number on the center
				text = tilefont.render(str(int(transtonum(xy)+1)), 1, BLACK)
				background.blit(text, (CentreTiles[transtonum(xy),0]-10,CentreTiles[transtonum(xy),1]))
			if printxy:		# Print Tile Coordinate on center
				text = tilefont.render(str(int(CentreTiles[transtonum(xy),0])) + ',' + str(int(CentreTiles[transtonum(xy),1])), 1, BLACK)
				background.blit(text, (CentreTiles[transtonum(xy),0]-20,CentreTiles[transtonum(xy),1]))
			if printpot:	# Colour Tiles following Potential Field
				col = 255 - int(255 * (potmap[y,x] / np.amax(potmap)))
				pygame.draw.rect(background, (col, col, col), (int(CentreTiles[transtonum(xy),0]-TileSize[0]/2), int(CentreTiles[transtonum(xy),1]-TileSize[1]/2), int(CentreTiles[transtonum(xy),0]+TileSize[0]/2), int(CentreTiles[transtonum(xy),1]+TileSize[1]/2)))
				text = tilefont.render(str(int(potmap[y,x])), 1, RED)	
				background.blit(text, (CentreTiles[transtonum(xy),0]-10,CentreTiles[transtonum(xy),1]))
				
	# print("TileCentres:"); print(CentreTiles)
#	print CentreTiles
#	print transtonum(goal)
#	print CentreTiles[transtonum(goal)]
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
	#youbot.setxytarget((CentreTiles[transtonum((goal))]))
	
	pathind = 1
	cnt = 0
	arrived = 0
	youbot.setstartxy(CentreTiles[transtonum(start)])
	goalsprite.setstartxy(CentreTiles[transtonum(goal)])
		
	
	print transtonum(start)
	print CentreTiles[transtonum(start)]
	
	while going:			# Main game loop
		clock.tick(60)
		
		screen.blit(background, (0, 0))
		
		Goalsprite.draw(screen)
		YouBotsprite.draw(screen)
		pygame.display.flip()
		
		
		if youbot.ontarget == 1 and pathind < potpath.shape[0]:
			print potpath[pathind]
			youbot.setxytarget((CentreTiles[transtonum((potpath[pathind]))]))		
			pathind = pathind + 1
			print "Step: %i" % pathind
			
		youbot.update()
		if youbot.ontarget == 1 and arrived == 0 and np.array_equal(youbot.xytarg, CentreTiles[transtonum(goal)]):
			print "YouBot has arrived!"
			arrived = 1
		
#		if cnt >= 60 and arrived == 0:
#			print "Youbot Target:"
#			print youbot.xytarg
#			print "Goal:"
#			print CentreTiles[transtonum(goal)]
#			print "Youbot Arrived:"
#			print youbot.ontarget
#			cnt = 1
			
		else:
			cnt = cnt + 1
		
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