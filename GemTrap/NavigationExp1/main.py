#!/usr/bin/python-2.7
# -*- coding: utf-8 -*-

#==============================================================================
# NavigationExp1 - by Alejandro Bordallo
# Details: First navigation experiment
# TODO: (EASY) Rename functions/constants/varaibles for good code practice
# TODO: (EASY) *Ongoing* COMMENT and REFACTOR
# TODO: (MEDIUM) Store all found paths and choose the shortest successful path
# TODO: (HARD) Implement A* when box is checked
#==============================================================================


#==============================================================================
	# IMPORT LIBRARIES
#******************************************************************************
import os, pygame, sys
from pygame.locals import *
import numpy as np

from GridWorld import GridWorld
from Policy import Policy

import time

#import random
#import AStar

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

#  Set Main and Resource directories
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'Resources')

#==============================================================================

#==============================================================================
	# RESOURCE LOADING FUNCTIONS
#******************************************************************************	
#  Image Loader Function
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
	
# *****************************************************************************	
# Sound Loader Function
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
		print (('Cannot load sound: {0}'.format(fullname)))
		raise SystemExit(str(geterror()))
	return sound
	
# *****************************************************************************	

#==============================================================================
	# CONSTANT VALUES
# *****************************************************************************
SidePanel	= 300			# Size of Information Panel
EnvSize	= (360, 600)	# Size of Experiment Environment
TileSize	= (60, 60)		# Size of InSpace Tiles

# Total screen size, including environment and side panel
TotalSize 	= (EnvSize [0] + SidePanel, EnvSize [1])

# Diagonal length of a tile (Forgot why I calculated it for - unused)
TileDiag	= np.sqrt(np.power(TileSize[0],2)+np.power(TileSize[1],2))

# Total number of tiles in x and y axes
NumTiles	= (EnvSize[0]/TileSize[0], EnvSize[1]/TileSize[1])
RobSize	= (38, 58)					# YouBot Size

# Array Containing x,y co-ordinates of tile centers
CentreTiles= np.zeros((NumTiles[0]*NumTiles[1],2))

# Colours
WHITE	= (255, 255, 255)
BLACK	= (0, 0, 0)
RED   	= (255, 0, 0)
GREEN	= (0, 255, 0)
BLUE		= (0, 0, 255)

# Mouse button values
LEFT = 1
RIGHT = 2

# Mouse pixel click tolerances
ClickTol = 30
PanelTol = 10

#==============================================================================
	# USEFUL FUNCTIONS
#******************************************************************************

def transtonum((x, y)):
	'''Transform tile (x,y) indices into sequential tile index'''
	
	num = y * NumTiles[0] + x
	return num
	
def transtoxy(num):
	'''Transform tile sequential index into tile (x,y) indices'''
	
	y = num // NumTiles[0]
	x = num % NumTiles[0]
	return (x,y)
	
def Printontiles(printind, potmap, background, tilefont):
	'''Print tile index numbers, (x,y) coordinates or potential field colours & values'''
	
	for y in range(0, NumTiles[1]):
		for x in range(0, NumTiles[0]):
			
			xy = (x,y)
			# Calculate (x,y) coordinate of tile centre given the (x,y) index and size of tile
			CentreTiles[transtonum(xy)] = (TileSize[0]/2 + TileSize[0]*(x),TileSize[1]/2 + TileSize[1]*(y))

			if printind == 0:	# Print tile index on the center of tile
				pygame.draw.rect(background, WHITE, (int(CentreTiles[transtonum(xy),0]-TileSize[0]/2), int(CentreTiles[transtonum(xy),1]-TileSize[1]/2), int(CentreTiles[transtonum(xy),0]+TileSize[0]/2), int(CentreTiles[transtonum(xy),1]+TileSize[1]/2)))				
				text = tilefont.render(str(int(transtonum(xy)+1)), 1, BLACK)
				background.blit(text, (CentreTiles[transtonum(xy),0]-10,CentreTiles[transtonum(xy),1]))

			elif printind == 1:	# Print tile (x,y) coordinate on center
				pygame.draw.rect(background, WHITE, (int(CentreTiles[transtonum(xy),0]-TileSize[0]/2), int(CentreTiles[transtonum(xy),1]-TileSize[1]/2), int(CentreTiles[transtonum(xy),0]+TileSize[0]/2), int(CentreTiles[transtonum(xy),1]+TileSize[1]/2)))				
				text = tilefont.render(str(int(CentreTiles[transtonum(xy),0])) + ',' + str(int(CentreTiles[transtonum(xy),1])), 1, BLACK)
				background.blit(text, (CentreTiles[transtonum(xy),0]-26,CentreTiles[transtonum(xy),1]))

			elif printind == 2:	# Colour Tiles following potential field and print potential values
				col = 255 - int(255 * ((potmap[y,x] - np.amin(potmap)) / np.ptp(potmap)))
				pygame.draw.rect(background, (col, col, col), (int(CentreTiles[transtonum(xy),0]-TileSize[0]/2), int(CentreTiles[transtonum(xy),1]-TileSize[1]/2), int(CentreTiles[transtonum(xy),0]+TileSize[0]/2), int(CentreTiles[transtonum(xy),1]+TileSize[1]/2)))
				text = tilefont.render(str(int(potmap[y,x])), 1, RED)	
				background.blit(text, (CentreTiles[transtonum(xy),0]-4,CentreTiles[transtonum(xy),1]))
			else:
				print "Printing index is out of bounds"
	
def Panelprint(screen, name, y, fr=None):
	'''Print information on side panel'''
	
	panelfont = pygame.font.SysFont("monospace", 15)
	tab = 25
	space = 20
	
	if fr != None:	# Check if information needs formatting (i.e. Data: Value)
		text = panelfont.render(name + ':' + str(fr), 1, BLACK)
		screen.blit(text, (EnvSize[0] + tab, y * space))
		
	else:		# Or no editing (i.e. Data)
		text = panelfont.render(name, 1, BLACK)
		screen.blit(text, (EnvSize[0] + tab, y * space))
		
def Checkboxprint(screen, boxnum, checked, boxnames):
	'''Print checkboxes on side panel'''
	
	checkboxfont = pygame.font.SysFont("monospace", 15)
	
	tab = 20
	space = 30
	boxsize = 20
	y = 310
	boxcentres = np.zeros((boxnum, 2))
	
	for i in range(0, boxnum):
		pygame.draw.rect(screen, BLACK, (EnvSize[0]+tab, y+(i*space), boxsize, boxsize))
		if checked[i] == 1:		
			pygame.draw.rect(screen, GREEN, (EnvSize[0]+tab +3, (y+(i*space))+3, boxsize-6, boxsize-6))
		else:
			pygame.draw.rect(screen, WHITE, (EnvSize[0]+tab +3, (y+(i*space))+3, boxsize-6, boxsize-6))
		text = checkboxfont.render(boxnames[i], 1, BLACK)
		screen.blit(text, (EnvSize[0] + tab + boxsize + 2, y+(i*space)))
		boxcentres[i] = EnvSize[0] + tab + (boxsize / 2), y+(i*space) + (boxsize / 2) 
		
	return boxcentres
	
def Backprint(background, EnvSize, TileSize, SidePanel):
	''' Print background lines and side panel'''
	
	locx = 0
	while locx <= EnvSize[0]:	# Draw lines vertically
		pygame.draw.line(background, BLACK, (locx, 0), (locx, EnvSize[1]))
		locx = locx + TileSize[0]
	
	locy = 0
	while locy <= EnvSize[1]:	# Draw lines horizontally
		pygame.draw.line(background, BLACK, (0, locy), (EnvSize[0], locy))
		locy = locy + TileSize[1]
		
	# Draw side panel separation black line and white background
	pygame.draw.rect(background, BLACK, (EnvSize[0]+1, 0, EnvSize[0]+10, EnvSize[1]))
	pygame.draw.rect(background, WHITE, (EnvSize[0]+11, 0, EnvSize[0]+11+SidePanel, EnvSize[1]))
	
		
def PotField(mapsize, start, goal, blocks=None):
	''' Create field of potential values considering goal position and obstacle blocks 
	(Start is not taken into account to simplify gradient) '''
	
	PotMap = np.matrix(np.zeros(mapsize))	# Create empty potential field
	blocktol = 1						# Repulsor field range
	blockcost = 4						# Cost of traveling through obstacle repulsion
	
	#	sval = 0
	#	gval = -1 * max(mapsize[0],mapsize[1])
	#	goalbonus = 5
	#	self.Map(start) = 0
	#	self.Map(goal) = -1 * mapsize[0]	
	
	for y in range(0, mapsize[0]):
		for x in range(0, mapsize[1]):
			PotMap[y,x] = (abs(x-goal[0]) + abs(y-goal[1])) * 3
			#PotMap[y,x] = PotMap[y,x] + max(abs(x-start[0]),abs(y-start[1]))
	
	if blocks != None:
		for i in range(0, len(blocks)):
			for y in range(blocktol*-1, blocktol+1):
				if blocks[i][1]+y < 0 or blocks[i][1]+y >= mapsize[0]:
					continue
				for x in range(blocktol*-1, blocktol+1):
					if blocks[i][0]+x < 0 or blocks[i][0]+x >= mapsize[1]:
						continue
					PotMap[blocks[i][1]+y,blocks[i][0]+x] = PotMap[blocks[i][1]+y,blocks[i][0]+x] + blockcost
			PotMap[blocks[i][1],blocks[i][0]] = PotMap[blocks[i][1],blocks[i][0]] + blockcost * 4
	
	PotMap[goal[1],goal[0]] = 0
	
	return PotMap
	
def findPotpath(start, goal, potmap, rnd = 0):
	''' Attempt to find a path from Start to Goal via gradient descent.
	Stochasticity added through arbitrary selection of next node when
	equivaluable. If no complete path found, next best is selected and
	YouBot will stop at local minima (Kind of the point with Pot. Fields)'''
	
	fail = 0
	attempts = 100
	patt = 0
	temppath = np.array((start))
	
	for n in range(0, attempts):
		maxln = 15
		path = np.zeros((1,2))
		path[0] = start
		currnode=start
		mapsize = potmap.shape
		fail = 0
		ln = 0
		mintol = 0	# Add tolerance to avoid local minima, but increases path length and randomness
		
		while np.array_equal(path[-1], goal) == False:
			nnodes = np.empty(shape=(8,3))
			nnodes[:] = np.NAN
			i = 0
			for y in range(-1, 2):
				if currnode[1] + y < 0 or currnode[1] + y >= mapsize[0]:
					continue
				for x in range(-1, 2):
					if currnode[0] + x < 0 or currnode[0] + x >= mapsize[1] or (y == 0 and x == 0):
						continue
					if potmap[currnode[1] + y, currnode[0] + x] <= potmap[currnode[1], currnode[0]]:
						nnodes[i] = [currnode[0] + x, currnode[1] + y, potmap[currnode[1] + y,currnode[0] + x]]
						i = i + 1
			
			
			mincost = np.nanmin(nnodes, 0)[2]
			minnodes = np.where(nnodes[:,2] <= mincost + mintol)
			
			if nnodes.size == np.isnan(nnodes).sum():
				fail = fail + 1
				#print "Failed to find a path!"
				break
			
			if rnd == 0:
				nextind = np.nanargmin(nnodes, 0)[2]
			else:
				#minnodes = np.where(nnodes[:,2] == mincost)
				r = np.random.randint(0, len(minnodes[0]))
				nextind = minnodes[0][r]
	
			nextpt  = nnodes[nextind, 0:2]
			path = np.vstack((path, nextpt))
			currnode = nextpt
			
			if ln >= maxln:
				patt = patt + 1
				#print "Reached path maximum length!"
				break
			else:
				ln = ln + 1
			
		if np.array_equal(path[-1], goal):
			print "Success at finding path!"
			# TODO: Store all found paths and choose the shortest successful path
			break

		
	if n >= attempts-1:
		print "Too many failed attempts at randomly finding path!"

		# Temporary fix to random short paths
		temppath = np.vstack((start, path))
		print "Using Temppath Instead"
		print temppath
		return temppath
		
	else:
		print "Success"	
		print path
		return path
		#print path
	
def gridworld():
	''' Create complete discrete environment for MDP modelling (InSpace Tiled), including Rewards and Transition probabilities'''
	w = GridWorld([[GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_EXIT, GridWorld.CELL_VOID, GridWorld.CELL_VOID], 
			   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID],
			   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID],
			   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_PIT, GridWorld.CELL_VOID],
			   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID],
			   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID],
			   [GridWorld.CELL_VOID, GridWorld.CELL_PIT, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID],
			   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID],
			   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID],
			   [GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID, GridWorld.CELL_VOID]], discountFactor = 1 )
	
	w.setRewards(-0.04, -1, 1)
	w.setProbabilities(0.8, 0.1, 0.1, 0)
#	w.setDiscountFactor(0.6)
	return w
	
def policy(w):
	''' Calculate policy for given world'''
	p = Policy(w)
	p.policyIteration(turbo=True)
	
	return p
	
def closestobst(youbot, BlockTile):
	
	dist = np.zeros((len(BlockTile),1))	
	
	for i in range(len(BlockTile)):
		dist[i] = np.sqrt(np.square(abs(youbot.rect.center[0] - BlockTile[i][0])) + np.square(abs(youbot.rect.center[1] - BlockTile[i][1])))
		
	obstind = np.argmin(dist)
	obstdist= np.round(dist[obstind], 2)
	
	return obstind, obstdist
	
#==============================================================================
	#  GAME SPRITES
#******************************************************************************
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
	
	def setposxy(self, startxy):
		self.rect.center = startxy	
		self.xytarg = self.rect.center
		
	def setxytarget(self, xycoord):
		"Set YouBot target for moving towards"
		self.xytarg = xycoord
		
	def update(self):
		"YouBot movement update"
		if np.array_equal(self.rect.center, self.xytarg):
			# Check if YouBot has reached its movement target
			self.ontarget = 1
		else:
			self.ontarget = 0
			
		self._move()
		
	def _move(self):
		"Update position of YouBot given its maximum speed and current/target positions"
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

#******************************************************************************		
class Goal(pygame.sprite.Sprite):
	"""Sprite representing Goal target"""
	def __init__(self, posx = 195, posy = 15):
		pygame.sprite.Sprite.__init__(self) # Call Sprite Initialiser
		self.image, self.rect = load_image('goal.png', -1)
		self.image = pygame.transform.scale(self.image, (35, 35))
		self.rect = self.image.get_rect()
		self.rect.topleft = (posx, posy)
		
	def setposxy(self, startxy):
		# Set position of Goal sprite
		self.rect.center = startxy

#******************************************************************************			
class Start(pygame.sprite.Sprite):
	"""Sprite representing Start position"""
	def __init__(self, posx = 195, posy = 15):
		pygame.sprite.Sprite.__init__(self) # Call Sprite Initialiser
		self.image, self.rect = load_image('start.png', -1)
		self.image = pygame.transform.scale(self.image, (35, 35))
		self.rect = self.image.get_rect()
		self.rect.topleft = (posx, posy)
		
	def setposxy(self, startxy):
		# Set Position of Start sprite
		self.rect.center = startxy
	
#******************************************************************************	
class Block(pygame.sprite.Sprite):
	"""Sprite representing obstacles"""
	def __init__(self, posx = 195, posy = 15):
		pygame.sprite.Sprite.__init__(self) # Call Sprite Initialiser
		self.image, self.rect = load_image('danger.png')
		self.image = pygame.transform.scale(self.image, (59, 59))
		self.rect = self.image.get_rect()
		self.rect.topleft = (posx, posy)
		
	def setposxy(self, startxy):
		self.rect.center = startxy

#==============================================================================
	# MAIN PROCESS
#******************************************************************************
def main():
	"""This function is called when the program starts."""

	print "Initialising..."
	#*************************************************************************
	# PYGAME SETUP
	pygame.init()
	screen = pygame.display.set_mode((TotalSize), 0)
	pygame.display.set_caption('Navigation Experiment')
	pygame.mouse.set_visible(1)
	clock = pygame.time.Clock()
	#*************************************************************************

	#*************************************************************************
	# PARAMETERS SETUP
	mouseenable = 1	# Enable mouse control
	pressed = 0		# Set mouse click to de-pressed state
	pathind = 1		# Path step index
	frm = 0			# Current Frame number
	arrived = 0		# YouBot has not arrived at its target yet
	MDPNav = 0		# Enable/Disable MDP Navigation instead of Potential Field	

	# Start, Goal and Obstacle positions (Max x=5, y=9)	
	start= [2,9]
	goal= [3,0]
	blockxy =[(1,6), (4,3)]
	numblocks = len(blockxy)
	
	# Generate Potential Field
	potmap = PotField((NumTiles[1],NumTiles[0]), start, goal, blockxy)
	
	# Find stochastic optimal path for potential field
	potpath = findPotpath(start, goal, potmap, 1)
	
	# Numbering of Tiles
	tilefont = pygame.font.SysFont("monospace", 13)
	# printind = 0		# Print Tile Number on the center
	# printind = 1		# Print Tile Coordinate on center
	printind = 2		# Colour Tiles as Potential Field
	
	# CheckBoxes
	boxnum = 2
	checked = [0, 1]
	if len(checked) != boxnum:
		print "Checkbox numbers do not match!"
	boxnames = ["Stop YouBot", "Enable MDP Planning"]
	
	#*************************************************************************
	
	#*************************************************************************
	# GRAPHICS
	# Initialise YouBot representation
	youbot = YouBot()
	YouBotsprite = pygame.sprite.RenderPlain(youbot)
	
	# Initialise Start representation
	startsprite = Start()
	Startsprite = pygame.sprite.RenderPlain(startsprite)

	# Initialise Goal representation
	goalsprite = Goal()
	Goalsprite = pygame.sprite.RenderPlain(goalsprite)
	
	# Initialise Obstacle representations
	block0 = Block()
	block1 = Block()
	Block0sprite = pygame.sprite.RenderPlain(block0)
	Block1sprite = pygame.sprite.RenderPlain(block1)
	
	# Initialise World background representation
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	
	# Print tiles, background and side panel
	Printontiles(printind, potmap, background, tilefont)
	Backprint(background, EnvSize, TileSize, SidePanel)	

	#*************************************************************************
	
	#*************************************************************************
	# INITIALISATION
	
	# Store centre position of important tiles
	StartTile	= CentreTiles[transtonum(start)]
	GoalTile	= CentreTiles[transtonum(goal)]
	BlockTile = np.zeros((numblocks, 2))
	BlockTile[0]= CentreTiles[transtonum(blockxy[0])]
	BlockTile[1]= CentreTiles[transtonum(blockxy[1])]
	
	# Set sprite positions to centre of the important tiles
	youbot.setposxy(StartTile)
	startsprite.setposxy(StartTile)
	goalsprite.setposxy(GoalTile)
	block0.setposxy(BlockTile[0])
	block1.setposxy(BlockTile[1])
	
	# Next position for each policy step
	pos = start

	# MDP environment intialisation and Policy generation
	if MDPNav == 1:
		w = gridworld()
		p = policy(w)
	
#	print(p.utilityVectorToString())
#	print(p.policyToString())
#	print ""
#	print(p.getPolicyFromUtilityVector(start))
	
#==============================================================================
	# MAIN LOOP
#******************************************************************************
	going = True
	print "Main Loop"
	tstart = time.clock()
	tstop = time.clock()
	
	while going:			# Main game loop
		
		clock.tick(60)		# Set frames per second
		if frm >= 30:		# Independent frame counter
			frm = 0
		else:
			frm = frm + 1
		
		screen.blit(background, (0, 0))	# Put background on screen
		
		# Draw all sprites to the screen
		Block0sprite.draw(screen)
		Block1sprite.draw(screen)
		Startsprite.draw(screen)
		Goalsprite.draw(screen)
		YouBotsprite.draw(screen)
		
		# Calculate YouBot travel time (If very small consider negligible)
		travtime = np.round(tstop - tstart, 2)
		if travtime < 0.1:
			travtime = 0
		
		#********************************************************************
		# SIDE PANEL
		Panelprint(screen, "Frame:%02d" % frm, 0)
		Panelprint(screen, "Travel time", 1, travtime)
		
		Panelprint(screen, "Start Tile", 3, CentreTiles[transtonum(start)])
		Panelprint(screen, "YouBot Position", 4, youbot.rect.center)
		Panelprint(screen, "Goal Position", 5, goalsprite.rect.center)
		Panelprint(screen, "Distance to Goal", 6, np.round(np.sqrt(abs(youbot.rect.center[0]-GoalTile[0])+abs(youbot.rect.center[1]-GoalTile[1])), 2))
		Panelprint(screen, "Step Number", 7, pathind)

		obstind, obstdist = closestobst(youbot, BlockTile)
		Panelprint(screen, "Closest: Block{0} at {1}".format(obstind, obstdist), 8)
		Panelprint(screen, "Block0 Position", 9, block0.rect.center)
		Panelprint(screen, "Block1 Position", 10, block1.rect.center)

		if pressed:		# Check if the cursor is picking something up
			if picked == 0:
				Panelprint(screen, "Relocating Block0", 11)
			elif picked == 1:
				Panelprint(screen, "Relocating Block1", 11)
			elif picked == 2:
				Panelprint(screen, "Relocating YouBot", 11)
			elif picked == 3:
				Panelprint(screen, "Relocating Goal", 11)
		
		if arrived:
			Panelprint(screen, "YouBot has arrived!", 13)
		elif np.array_equal(start, goal) == False:
			tstop = time.clock()	
		
		Panelprint(screen, "Cursor Position", 14, pygame.mouse.get_pos())
				
		Panelprint(screen, "Bottom", 29)
		if np.array_equal(potpath[-1], goal) == False and np.array_equal(CentreTiles[transtonum(potpath[-1])], youbot.rect.center):
			Panelprint(screen, "Youbot stuck at Local Minima!", 12)
			
		boxcentres = Checkboxprint(screen, boxnum, checked, boxnames)
			
		pygame.display.flip()
		
		#********************************************************************
		# PATH COMPUTATION
		
		# Set next target once Youbot arrives to previously set target
			# Potential Field
		if youbot.ontarget == 1 and pathind < potpath.shape[0] and MDPNav == 0:
			youbot.setxytarget((CentreTiles[transtonum((potpath[pathind]))]))		
			pathind = pathind + 1
			
			# MDP Policy computation
		elif youbot.ontarget == 1 and MDPNav == 1 and arrived == 0:
			# print("Q Values:")
			# print(p.getQValues(pos))
			# print("Policy: %s" % p.getPolicyFromUtilityVector(pos))
			a = p.getPolicyFromUtilityVector(pos)
			if a == 'N':
				pos[1] = pos[1] - 1
			elif a == 'S':
				pos[1] = pos[1] + 1
			elif a == 'W':
				pos[0] = pos[0] - 1
			elif a == 'E':
				pos[0] = pos[0] + 1
			youbot.setxytarget((CentreTiles[transtonum(pos)]))

		if checked[0] == 0:
			youbot.update()
		
		# Check if the YouBot has reached its goal destination
		if youbot.ontarget == 1 and arrived == 0 and np.array_equal(youbot.xytarg, CentreTiles[transtonum(goal)]):
			print "YouBot has arrived!"
			arrived = 1
			
		#********************************************************************
		# KEYBOARD AND MOUSE EVENTS
		
		event = pygame.event.poll()
		key = pygame.key.get_pressed()
		
		if event.type == QUIT or key[K_ESCAPE]:
			going = False	# Be IDLE friendly
			
		if mouseenable == 1:
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and pressed == 0:
				# When left mouse button is clicked, find closest object to cursor
				pressed = 1	# Raise flag to signify we are picking something up
				picked = -1
				
				if abs(event.pos[0] - block0.rect.center[0]) < ClickTol and abs(event.pos[1] - block0.rect.center[1]) < ClickTol:
					picked = 0	# Picked Block0
					
				elif abs(event.pos[0] - block1.rect.center[0]) < ClickTol and abs(event.pos[1] - block1.rect.center[1]) < ClickTol:
					picked = 1	# Picked Block1
					
				elif abs(event.pos[0] - youbot.rect.center[0]) < ClickTol and abs(event.pos[1] - youbot.rect.center[1]) < ClickTol:
					picked = 2	# Picked YouBot
					
				elif abs(event.pos[0] - goalsprite.rect.center[0]) < ClickTol and abs(event.pos[1] - goalsprite.rect.center[1]) < ClickTol:
					picked = 3	# Picked Goal
					
				else:
					picked = -1
					pressed = 0
					
				if abs(event.pos[0] - boxcentres[0][0]) < PanelTol and abs(event.pos[1] - boxcentres[0][1]) < PanelTol:
					checked[0] = 1 - checked[0]	# Check/Uncheck Box 0
					pressed = 0
					
				elif abs(event.pos[0] - boxcentres[1][0]) < PanelTol and abs(event.pos[1] - boxcentres[1][1]) < PanelTol:
					checked[1] = 1 - checked[1]	# Check/Uncheck Box 1
					pressed = 0
				
			elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT and pressed == 1:
				# De-pressed left mouse button and picking something up
				pressed = 0
				arrived = 0
				
				#start = transtoxy(youbot.xytarg)
				if picked != 2:
					start = potpath[pathind-1]
				potmap = PotField((NumTiles[1],NumTiles[0]), start, goal, blockxy)		
				potpath = findPotpath(start, goal, potmap, 1)
				Printontiles(printind, potmap, background, tilefont)
				Backprint(background, EnvSize, TileSize, SidePanel)
				pathind = 0
				if np.array_equal(youbot.xytarg, CentreTiles[transtonum(goal)]):
					potpath = np.vstack((potpath, (goal)))
					print "YouBot is already at Goal!"
				print "potpath"
				print potpath
				# youdiff = abs(np.subtract(CentreTiles, youbot.rect.center))
				# younum = np.argmin(youdiff[:,0]+youdiff[:,1])
				# start = potpath[pathind]

			
		if np.array_equal(youbot.rect.center, CentreTiles[transtonum(start)]):
			# If YouBot is at the start of path then reset clock unless it does not need to move
			if np.array_equal(start, goal) == False:
				tstart = time.clock()
				# Update position of YouBot when sprite gets relocated
				youbot.setposxy(CentreTiles[transtonum(start)])
			
		if pressed == 1:
			# Pressed left mouse button
		
			if picked == 0:	# "Chosen Block0"
				tilediff = abs(np.subtract(CentreTiles, pygame.mouse.get_pos()))
				num = np.argmin(tilediff[:,0]+tilediff[:,1])
				block0.setposxy(CentreTiles[num])
				blockxy[0] = transtoxy(num)
				
			elif picked == 1:	# "Chosen Block1"
				tilediff = abs(np.subtract(CentreTiles, pygame.mouse.get_pos()))
				num = np.argmin(tilediff[:,0]+tilediff[:,1])				
				block1.setposxy(CentreTiles[num])				
				blockxy[1] = transtoxy(num)
				
			elif picked == 2:	# "Chosen YouBot"
				tilediff = abs(np.subtract(CentreTiles, pygame.mouse.get_pos()))
				num = np.argmin(tilediff[:,0]+tilediff[:,1])
				youbot.setposxy(CentreTiles[num])
				startsprite.setposxy(CentreTiles[num])
				start = transtoxy(num)
				
			elif picked == 3:	# "Chosen Goal"
				tilediff = abs(np.subtract(CentreTiles, pygame.mouse.get_pos()))
				num = np.argmin(tilediff[:,0]+tilediff[:,1])
				goalsprite.setposxy(CentreTiles[num])
				goal = transtoxy(num)
				
		#********************************************************************
		# UPDATE VALUES
		# Important tiles
		StartTile	= CentreTiles[transtonum(start)]
		GoalTile	= CentreTiles[transtonum(goal)]
		BlockTile[0]= CentreTiles[transtonum(blockxy[0])]
		BlockTile[1]= CentreTiles[transtonum(blockxy[1])]
				
	#*************************************************************************
	# END OF PROGRAM
	print "Exiting..."
	pygame.quit()
	sys.exit()

#==============================================================================
	# Run code if called as main
if __name__ == '__main__':
	main()
#==============================================================================