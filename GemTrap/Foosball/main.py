# -*- coding: utf-8 -*-

#==============================================================================
# FOOSBALL - by Alejandro Bordallo and Andrew Robinson
# Details: Foozball game sim for autonomous agents, simple ai, path planning
# TODO: Fix the weird bouncing angles that came from refactoring
#==============================================================================


#==============================================================================

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
FPS = 30			# Frames per second
RField = (2370, 1140)	# Green Field
R_WALL_WIDTH = 100		# Wall width in mm
RTapewidth = 50		# Line width in mm
RGoalwidth = 630		# Goal width in mm
RGoaldepth = 50		# Goal depth in mm
RBallsize = 50		# Ball diameter in mm

RPitch = (RField[0]+2*(R_WALL_WIDTH+RTapewidth), RField[1]+2*(R_WALL_WIDTH+RTapewidth))	# X, Y in mm
Rdx = 2			# To fit on screen
Rdy = 2
Fntsize = 36
PITCH = (RPitch[0]/Rdx, (RPitch[1]/Rdy))
Field = ((RField[0]+RTapewidth)/Rdx, ((RField[1]+RTapewidth)/Rdy))
WALL_WIDTH = R_WALL_WIDTH / Rdx
Tapewidth = RTapewidth / Rdx
Goalwidth = RGoalwidth / Rdy
Goaldepth = RGoaldepth / Rdx
BALL_SIZE = RBallsize / Rdx
BALL_RADIUS = BALL_SIZE / 2
CENTRE = (PITCH[0]/2, PITCH[1]/2)
Res = (PITCH[0], PITCH[1] + Fntsize)		# Window Resolution
Xres = Res[0]
Yres = Res[1]
Edge = WALL_WIDTH + Tapewidth
Linewidth = 3 * Tapewidth
GRASS = (0, 148, 10)		# Field Colour
WALL = (0, 0, 0)			# Wall Colour
TAPE = (255, 255, 255)		# Line Colour
TITLE = (10, 10, 10)		# Title font Colour
TITLEBACK = (240, 240, 240)	# Title Background Colour
LINE = (150, 150, 150)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)
TABLE_FRICTION = 1
COLLISION_FRICTION = 1			# Collision TABLE_FRICTIONion
MARGIN = 1

TITLE_TEXT = 'Foosball Match'
#==============================================================================

	#TODO Implement Character Object properties
#==============================================================================
	#  Game Object Classes

class Ball(pygame.sprite.Sprite):
	"""Sprite for ball on the pitch"""
	def __init__(self, posx = CENTRE[0]-BALL_RADIUS, posy = CENTRE[1]-BALL_RADIUS):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		#self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
		#self.image.fill(ORANGE)
		self.image, self.rect = load_image('ball.png', -1)
		self.image = pygame.transform.scale(self.image, (25, 25))
		#self.rect = self.image.get_rect()
		
		#screen = pygame.display.get_surface()
		#self.area = screen.get_rect()
		self.pitch = pygame.Rect(WALL_WIDTH, WALL_WIDTH, Field[0], Field[1])
		self.pitch.center = CENTRE
		#self.area = (PITCH[0], PITCH[1])
		#self.posx = 1000
		#self.posy = 1000
		self.rect.topleft = (posx, posy)
		self.speed = 0
		self.orientation = 0
		self.count = 0
		#self.touching = 0

	
	def update(self, dirxy, pushSpeed, pushOrient, bounce = 0, move = 0, push = 0):
		'''Update ball position.
		'''
		if bounce == 1:
			self._bounce()
		elif move == 1:
			self._move(dirxy)
		elif push == 1:
			self._push(pushSpeed, pushOrient)

		self._updatePosition()
		
#	def calcangle(oldpos, newpos):
#		"Calculate angle from 2 x,y cordinates"
#		xneg = 0
#		yneg = 0
#		xdif = oldpos[0] - newpos [0]		
#		ydif = oldpos[1] - newpos[1]
#		
#		if xdif < 0:
#			xneg = 1
#			xdif = abs(xdif)
#		if ydif < 0:
#			yneg = 1
#			ydif = abs(ydif)				
		
	def _updatePosition(self):
		"Update speed and position of ball."
		self.changeDirectionSlightlyAfterNSteps(15)
		xymod, xy = self.computeDynamics()
		
		self.getNextPosition(xymod)	
		if self.hasHitWall():
			self.bounceOffWall(xy)
			
		self.getNextPosition(xymod)	
		if self.hasHitWall():
			self.moveBallToBeWithinPitch()
				
		move = self.nextPosition.tolist()
		self.rect.center = move[0]
		
		self.slowDownDueToTableFriction()
		self.stopIfSlowEnough(0.8)

	def changeDirectionSlightlyAfterNSteps(self, steps):
		self.count += 1
		if self.count >= steps  and self.speed != 0:
			self.count = 0
			self.orientation +=  np.random.normal(0, 1)
	
	def computeDynamics(self):
		angle = self.orientation % 90
		xmod = self.speed * np.sin(np.deg2rad(angle))
		ymod = self.speed * np.cos(np.deg2rad(angle))
		xy = self.getXY()
		return np.matrix((xmod*xy[0], ymod*xy[1])), xy
	
	def getXY(self):
		self.orientation %= 360
		if self.orientation >= 0 and self.orientation < 90:
			return [1, -1]
		elif self.orientation >= 90 and self.orientation < 180:
			return [1, 1]	
		elif self.orientation >= 180 and self.orientation < 270:
			return [-1, 1]				
		elif self.orientation >= 270 and self.orientation <= 360:
			return [-1, -1]
	
	def getNextPosition(self, xymod):
		currentPosition = np.matrix(self.rect.center)
		self.nextPosition = currentPosition + xymod
		
	def hasHitWall(self):
		return self.hasGoneOffField()
	
	def hasGoneOffField(self):
		return self.hasGoneOffFieldSide() or self.hasGoneOffFieldEnd()
	
	def hasGoneOffFieldSide(self):
		return self.hasGoneOffFieldLeft() or self.hasGoneOffFieldRight()
	
	def hasGoneOffFieldLeft(self):
		return self.nextPosition[0, 0] < self.pitch.left
		
	def hasGoneOffFieldRight(self):
		return self.nextPosition[0, 0] > self.pitch.right
	
	def hasGoneOffFieldEnd(self):
		return self.hasGoneOffFieldTop() or self.hasGoneOffFieldBottom()
	
	def hasGoneOffFieldTop(self):
		return self.nextPosition[0, 1] < self.pitch.top
	
	def hasGoneOffFieldBottom(self):	
		return self.nextPosition[0, 1] > self.pitch.bottom
	
	def bounceOffWall(self, xy):
		if self.hasGoneOffFieldSide():
			self.orientation = 360 - self.orientation
		elif self.hasGoneOffFieldEnd():
			if xy[0] == 1:
				self.orientation = 180 - self.orientation
			elif xy[0] == -1:
				self.orientation = 540 - self.orientation
		self.slowDownDueToCollisionFriction()
		self.speed *= COLLISION_FRICTION
		
	def moveBallToBeWithinPitch(self):
		if self.hasGoneOffFieldLeft():
			self.nextPosition[0, 0] = self.pitch.left + MARGIN
		elif self.hasGoneOffFieldRight():
			self.nextPosition[0, 0] = self.pitch.right - MARGIN
		elif self.hasGoneOffFieldTop():
			self.nextPosition[0, 1] = self.pitch.top + MARGIN
		elif self.hasGoneOffFieldBottom():
			self.nextPosition[0, 1] = self.pitch.bottom - MARGIN
			
	
	def slowDownDueToTableFriction(self):
		self.slowDownDueToFriction(TABLE_FRICTION)
		
	def slowDownDueToCollisionFriction(self):
		self.slowDownDueToFriction(COLLISION_FRICTION)
		
	def slowDownDueToFriction(self, friction):
		self.speed *= friction
				
	def stopIfSlowEnough(self, threshold):
		if self.speed <= threshold:
			self.speed = 0
		
	def _move(self, dirxy):
		'''Update position of the ball
		'''
		currentPosition = np.matrix(self.rect.center)
		xymat = np.matrix(dirxy)
		self.nextPosition = currentPosition + xymat * self.speed
		if not self.hasGoneOffField():
			move = self.nextPosition.tolist()
			self.rect.center = move[0]
			
	def _bounce(self, xymat = np.matrix((1, 1))):
		'''Update position of the ball
		'''
		self.getNextPosition(xymat*self.speed)
		
		if self.hasGoneOffFieldSide():
			xymat[0, 0] *= -1 
		if self.hasGoneOffFieldEnd():
			xymat[0, 1] *= -1
			
		self.getNextPosition(xymat*self.speed)	
		move = self.nextPosition.tolist()
		self.rect.center = move[0]
		
	def _push(self, speed, theta):
		'''Updates position of the ball given speed and orientation
		'''
		self.speed = speed
		self.orientation = theta

#==============================================================================



#  fpsClock = pygame.time.Clock()
def initializeEverything():
	pygame.init()
	screen = pygame.display.set_mode((Res), 0)
	pygame.display.set_caption(TITLE_TEXT)
	pygame.mouse.set_visible(1)
	return screen
	
def drawBackground(screen):
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(WALL)
	return background

def drawPitch(background):
	outlinebox = pygame.Rect(WALL_WIDTH, WALL_WIDTH, PITCH[0] - 2*WALL_WIDTH, PITCH[1] - 2*WALL_WIDTH)
	pitchbox = pygame.Rect(Edge, Edge, PITCH[0] - 2*Edge, PITCH[1] - 2*Edge)
	titlebox = pygame.Rect(0, PITCH[1], Xres, Yres)
	line1box = pygame.Rect(PITCH[0]*1/4-Linewidth/2, WALL_WIDTH, Linewidth, PITCH[1]-2*WALL_WIDTH)
	line2box = pygame.Rect(PITCH[0]*2/4-Linewidth/2, WALL_WIDTH, Linewidth, PITCH[1]-2*WALL_WIDTH)
	line3box = pygame.Rect(PITCH[0]*3/4-Linewidth/2, WALL_WIDTH, Linewidth, PITCH[1]-2*WALL_WIDTH)
	goalyellow=pygame.Rect(WALL_WIDTH/2, PITCH[1]/2 - Goalwidth/2, Goaldepth, Goalwidth)
	goalblue=pygame.Rect(PITCH[0] - WALL_WIDTH, PITCH[1]/2 - Goalwidth/2, Goaldepth, Goalwidth)

	pygame.draw.rect(background, TAPE, outlinebox, 0)
	pygame.draw.rect(background, GRASS, pitchbox, 0)
	pygame.draw.rect(background, TITLEBACK, titlebox, 0)
	pygame.draw.rect(background, TAPE, line1box, 0)
	pygame.draw.rect(background, TAPE, line2box, 0)
	pygame.draw.rect(background, TAPE, line3box, 0)
	pygame.draw.rect(background, YELLOW, goalyellow, 0)
	pygame.draw.rect(background, BLUE, goalblue, 0)
	pygame.draw.line(background, LINE, (PITCH[0]*1/4, WALL_WIDTH), (PITCH[0]*1/4, PITCH[1]-WALL_WIDTH))
	pygame.draw.line(background, LINE, (PITCH[0]*2/4, WALL_WIDTH), (PITCH[0]*2/4, PITCH[1]-WALL_WIDTH))
	pygame.draw.line(background, LINE, (PITCH[0]*3/4, WALL_WIDTH), (PITCH[0]*3/4, PITCH[1]-WALL_WIDTH))

def centreTitleOnBackground(background):
	if pygame.font:
		font = pygame.font.Font(None, Fntsize)
		text = font.render(TITLE_TEXT, 1, TITLE)
		textpos = text.get_rect(centerx=Xres/2, centery=Yres - Fntsize/2)
		background.blit(text, textpos)

def showFeatureOnScreen(screen, name, x, fr=None):
	''' Show current frame on screen 
	'''
	myfont = pygame.font.SysFont("monospace", 15)
	if fr != None:
		text = myfont.render(name + ':' + str(fr), 1, (255, 255, 0))
		screen.blit(text, (x * 15, PITCH[1] - WALL_WIDTH + 10))
	else:
		text = myfont.render(name, 1, (255, 255, 0))
		screen.blit(text, (x * 15, PITCH[1] - WALL_WIDTH + 10))
		
def updateFeaturesOnScreen(screen, frame, ball):
	showFeatureOnScreen(screen, 'Frame', 5, "%02d" % frame)
	showFeatureOnScreen(screen, 'Pos', 15, ball.rect.center)
	showFeatureOnScreen(screen, 'Speed', 25, np.around(ball.speed, 3))
	showFeatureOnScreen(screen, 'Theta', 35, np.around(ball.orientation, 2))

def drawEverything(screen, background, ballSprite):
	screen.blit(background, (0, 0))
	ballSprite.draw(screen)
	
def main():
	"""this function is called when the program starts. It initializes 
	everything it needs, then runs in a loop until the function returns.
	"""

	screen = initializeEverything()

	#TODO Implement Full (Tiled/Object) Background
	background = drawBackground(screen)
	drawPitch(background)
	#pygame.draw.circle(background, ORANGE, (CENTRE[0], CENTRE[1]), BALL_SIZE/2, 0)
	centreTitleOnBackground(background)

	# Prepare Game Objects
	clock = pygame.time.Clock()

	ball = Ball()
	ballSprite = pygame.sprite.RenderPlain(ball)


	frame = 0				# Current Frame

	dirxy = [0, 0]
	bounce = 0
	move = 0
	push = 1
	going = True

	pushSpeed = np.random.randint(10, 26)
	pushOrient = np.random.randint(0, 360)
		
	while going:			# Main game loop
		clock.tick(60)


		ballSprite.update(dirxy, pushSpeed, pushOrient, bounce, move, push)
		push = 0
		
		#Draw Everything
		drawEverything(screen, background, ballSprite)
		
		frame += 1
		updateFeaturesOnScreen(screen, frame, ball)

		if frame == 30:
			frame = 0		
		
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				going = False
				print('User quit the game')

	pygame.quit()
	sys.exit()

#==============================================================================
	# Run if called

if __name__ == '__main__':
	main()
	
#==============================================================================