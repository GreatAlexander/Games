# -*- coding: utf-8 -*-

#==============================================================================
# NavigationExp1 - by Alejandro Bordallo
# Details: First navigation experiment
# TODO: (EASY) Add distance to closest obstacle
# TODO: (EASY) Implement checkable box
# TODO: (HARD) Implement A* when box is checked
#==============================================================================


#==============================================================================
	#import os, pygame, sys, random, numpy
import os, pygame, sys
from pygame.locals import *
import numpy as np

import time

#import AStar

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
SidePanel	= 300				# Size of Information Panel
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

LEFT = 1
RIGHT = 2

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
	
def Printontiles(printnum, printxy, printpot, potmap, background, tilefont):
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
#				print np.amin(potmap)
#				print np.amax(potmap)
#				print np.ptp(potmap)
				col = 255 - int(255 * ((potmap[y,x] - np.amin(potmap)) / np.ptp(potmap)))
				pygame.draw.rect(background, (col, col, col), (int(CentreTiles[transtonum(xy),0]-TileSize[0]/2), int(CentreTiles[transtonum(xy),1]-TileSize[1]/2), int(CentreTiles[transtonum(xy),0]+TileSize[0]/2), int(CentreTiles[transtonum(xy),1]+TileSize[1]/2)))
				text = tilefont.render(str(int(potmap[y,x])), 1, RED)	
				background.blit(text, (CentreTiles[transtonum(xy),0]-10,CentreTiles[transtonum(xy),1]))
	
def Panelprint(screen, name, y, fr=None):
	''' Show current frame on screen '''
	panelfont = pygame.font.SysFont("monospace", 15)
	tab = 25
	space = 20
	if fr != None:
		text = panelfont.render(name + ':' + str(fr), 1, BLACK)
		screen.blit(text, (EnvSize[0] + tab, y * space))
	else:
		text = panelfont.render(name, 1, BLACK)
		screen.blit(text, (EnvSize[0] + tab, y * space))
		
def Backprint(background, EnvSize, TileSize, SidePanel):
	''' Print Background lines and Side panel'''
	locx = 0
	while locx <= EnvSize[0]:
		
		pygame.draw.line(background, BLACK, (locx, 0), (locx, EnvSize[1]))
		locx = locx + TileSize[0]
	
	locy = 0
	while locy <= EnvSize[1]:
	
		pygame.draw.line(background, BLACK, (0, locy), (EnvSize[0], locy))
		locy = locy + TileSize[1]
		
	pygame.draw.rect(background, BLACK, (EnvSize[0]+1, 0, EnvSize[0]+10, EnvSize[1]))
	pygame.draw.rect(background, WHITE, (EnvSize[0]+11, 0, EnvSize[0]+11+SidePanel, EnvSize[1]))
	
	
	
		
def PotField(mapsize, start, goal, blocks=None):
	
	PotMap = np.matrix(np.zeros(mapsize))
	sval = 0
	gval = -1 * max(mapsize[0],mapsize[1])
	blocktol = 1
	blockcost = 6
	goalbonus = 5
	#self.Map(start) = 0
	#self.Map(goal) = -1 * mapsize[0]	
	
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
			PotMap[blocks[i][1],blocks[i][0]] = PotMap[blocks[i][1],blocks[i][0]] + blockcost * 1
	
	PotMap[goal[1],goal[0]] = 0
	
	return PotMap
	
def findPotpath(start, goal, potmap, rnd = 0):
	
	fail = 0
	attempts = 100
	patt = 0
	for n in range(0, attempts):
		path = np.array((start))
		currnode=start
		mapsize = potmap.shape
		fail = 0
		ln = 0
		maxln = 20
		mintol = 0	# Add tolerance to avoid local minima, but increases path length and randomness
		
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
					if potmap[currnode[1] + y, currnode[0] + x] <= potmap[currnode[1], currnode[0]]:
						nnodes[i] = [currnode[0] + x, currnode[1] + y, potmap[currnode[1] + y,currnode[0] + x]]
						i = i + 1
			
			
			mincost = np.nanmin(nnodes, 0)[2]
			minnodes = np.where(nnodes[:,2] <= mincost + mintol)
			#print nnodes
			#print minnodes
			
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
			break
				
		
	if n >= attempts-1:
		print "Too many failed attempts at randomly finding path!"
		#print path
	
	#print path
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
		
class Block(pygame.sprite.Sprite):
	"""Goal Sprite"""
	def __init__(self, posx = 195, posy = 15):
		pygame.sprite.Sprite.__init__(self) # Call Sprite Initialiser
		self.image, self.rect = load_image('danger.png')
		self.image = pygame.transform.scale(self.image, (59, 59))
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
	start=(2,9)
	goal=(3,0)
	blockxy =[(1,6), (4,3)]
	
	youbot = YouBot()
	YouBotsprite = pygame.sprite.RenderPlain(youbot)

	goalsprite = Goal()
	Goalsprite = pygame.sprite.RenderPlain(goalsprite)
	
	block0 = Block()
	block1 = Block()
	Block0sprite = pygame.sprite.RenderPlain(block0)
	Block1sprite = pygame.sprite.RenderPlain(block1)
	
	# World Generation
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	#background.fill(WHITE)
	
	

	potmap = PotField((NumTiles[1],NumTiles[0]), start, goal, blockxy)
	# print("Potential Map:"); print(potmap)

	potpath = findPotpath(start, goal, potmap, 1)	
		
	
	# Numbering of Tiles
	tilefont = pygame.font.SysFont("monospace", 15)
	printnum= 0		# Print Tile Number on the center
	printxy = 0		# Print Tile Coordinate on center
	printpot= 1	# Colour Tiles as Potential Field
	Printontiles(printnum, printxy, printpot, potmap, background, tilefont)

	Backprint(background, EnvSize, TileSize, SidePanel)
				
#==============================================================================
	# Main Loop
	going = True
	print "Main Loop"
	
	StartTile= CentreTiles[transtonum(start)]	
	GoalTile = CentreTiles[transtonum(goal)]
	Block0Tile=CentreTiles[transtonum(blockxy[0])]
	Block1Tile=CentreTiles[transtonum(blockxy[1])]
	
	mouseenable = 1
	pressed = 0
	clicktol = 30
	relocate = 1
	
	pathind = 1
	cnt = 0
	arrived = 0
	youbot.setstartxy(StartTile)
	goalsprite.setstartxy(GoalTile)
	block0.setstartxy(Block0Tile)
	block1.setstartxy(Block1Tile)
	
	tstart = time.clock()
	tstop = time.clock()
	while going:			# Main game loop
		
		clock.tick(60)		# Set frames per second
		if cnt >= 30:		# Independent frame counter
			cnt = 0
		else:
			cnt = cnt + 1
		
		screen.blit(background, (0, 0))	# Put background on screen
		
		# Draw all sprites to the screen
		Block0sprite.draw(screen)
		Block1sprite.draw(screen)
		Goalsprite.draw(screen)
		YouBotsprite.draw(screen)
		
		travtime = np.round(tstop - tstart, 2)
		if travtime < 0.1:
			travtime = 0
		# Side panel printing commands
		Panelprint(screen, "Frame:%02d" % cnt, 0)
		Panelprint(screen, "Travel time", 1, travtime)
		#TODO: Fix travel time when relocating
		Panelprint(screen, "YouBot Position", 2, youbot.rect.center)
		Panelprint(screen, "Distance to Goal", 3, np.round(np.sqrt(abs(youbot.rect.center[0]-GoalTile[0])+abs(youbot.rect.center[1]-GoalTile[1])), 2))
		Panelprint(screen, "Step Number", 4, pathind)
		if arrived:
			Panelprint(screen, "YouBot has arrived!", 5)
		elif np.array_equal(start, goal) == False:
			tstop = time.clock()
		Panelprint(screen, "Cursor Position", 6, pygame.mouse.get_pos())
		Panelprint(screen, "Goal Position", 7, goalsprite.rect.center)
		Panelprint(screen, "Block0 Position", 8, block0.rect.center)
		Panelprint(screen, "Block1 Position", 9, block1.rect.center)
		Panelprint(screen, "Start Position", 11, start)
		if pressed:
			if picked == 0:
				Panelprint(screen, "Relocating Block0", 10)
			elif picked == 1:
				Panelprint(screen, "Relocating Block1", 10)
			elif picked == 2:
				Panelprint(screen, "Relocating YouBot", 10)
			elif picked == 3:
				Panelprint(screen, "Relocating Goal", 10)
		Panelprint(screen, "Bottom", 29)
		if np.array_equal(potpath[-1], goal) == False and np.array_equal(CentreTiles[transtonum(potpath[-1])], youbot.rect.center):
			Panelprint(screen, "Youbot stuck at Local Minima!", 12)
			
			
		pygame.display.flip()
		
		# Set next target once Youbot arrives to previously set target
		if youbot.ontarget == 1 and pathind < potpath.shape[0]:
			youbot.setxytarget((CentreTiles[transtonum((potpath[pathind]))]))		
			pathind = pathind + 1
			
		youbot.update()
		
		# Check if the YouBot has reached its goal destination
		if youbot.ontarget == 1 and arrived == 0 and np.array_equal(youbot.xytarg, CentreTiles[transtonum(goal)]):
			print "YouBot has arrived!"
			arrived = 1
			
		event = pygame.event.poll()
		key = pygame.key.get_pressed()
		
		if event.type == QUIT or key[K_ESCAPE]:
			going = False  # Be IDLE friendly
			
		if mouseenable == 1:
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
				# "Clicked"
				pressed = 1
				if abs(event.pos[0] - block0.rect.center[0]) < clicktol and abs(event.pos[1] - block0.rect.center[1]) < clicktol:
					picked = 0
					# "Picked Block0"
				elif abs(event.pos[0] - block1.rect.center[0]) < clicktol and abs(event.pos[1] - block1.rect.center[1]) < clicktol:
					picked = 1
					# "Picked Block1"
				elif abs(event.pos[0] - youbot.rect.center[0]) < clicktol and abs(event.pos[1] - youbot.rect.center[1]) < clicktol:
					picked = 2
					# "Picked YouBot"
				elif abs(event.pos[0] - goalsprite.rect.center[0]) < clicktol and abs(event.pos[1] - goalsprite.rect.center[1]) < clicktol:
					picked = 3
					# "Picked Goal"
				else:
					picked = -1
					# "Picked NONE"
				
			elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
				# "Unclicked"
				pressed = 0
				arrived = 0
				#start = transtoxy(youbot.xytarg)
				if picked != 2 and relocate == 1:
					start = potpath[pathind-1]
				potmap = PotField((NumTiles[1],NumTiles[0]), start, goal, blockxy)		
				potpath = findPotpath(start, goal, potmap, 1)
				Printontiles(printnum, printxy, printpot, potmap, background, tilefont)
				Backprint(background, EnvSize, TileSize, SidePanel)
				pathind = 0
				arrived = 0
				#relocate = 1
#				youdiff = abs(np.subtract(CentreTiles, youbot.rect.center))
#				younum = np.argmin(youdiff[:,0]+youdiff[:,1])
#				start = potpath[pathind]

			
		if np.array_equal(youbot.rect.center, CentreTiles[transtonum(start)]):
			if np.array_equal(start, goal) == False:
				tstart = time.clock()
			if relocate == 1:	
				youbot.setstartxy(CentreTiles[transtonum(start)])
				#relocate = 0
			
		if pressed == 1:
			if picked == 0:	# "Chosen Block0"
				tilediff = abs(np.subtract(CentreTiles, pygame.mouse.get_pos()))
				num = np.argmin(tilediff[:,0]+tilediff[:,1])
				block0.setstartxy(CentreTiles[num])
				blockxy[0] = transtoxy(num)
				
			elif picked == 1:	# "Chosen Block1"
				tilediff = abs(np.subtract(CentreTiles, pygame.mouse.get_pos()))
				num = np.argmin(tilediff[:,0]+tilediff[:,1])				
				block1.setstartxy(CentreTiles[np.argmin(tilediff[:,0]+tilediff[:,1])])				
				blockxy[1] = transtoxy(num)
				
			elif picked == 2:	# "Chosen YouBot"
				tilediff = abs(np.subtract(CentreTiles, pygame.mouse.get_pos()))
				num = np.argmin(tilediff[:,0]+tilediff[:,1])
				youbot.setstartxy(CentreTiles[np.argmin(tilediff[:,0]+tilediff[:,1])])
				start = transtoxy(num)
				
			elif picked == 3:	# "Chosen Goal"
				tilediff = abs(np.subtract(CentreTiles, pygame.mouse.get_pos()))
				num = np.argmin(tilediff[:,0]+tilediff[:,1])
				goalsprite.setstartxy(CentreTiles[np.argmin(tilediff[:,0]+tilediff[:,1])])
				goal = transtoxy(num)
				

	print "Exiting..."
	pygame.quit()
	sys.exit()

#==============================================================================
	#  Run if called

if __name__ == '__main__':
	main()

#==============================================================================