# -*- coding: utf-8 -*-

#==============================================================================
# FOOZBALL - by Alejandro Bordallo
# Details: Foozball game test, autonomous agents, simple ai, path planning
# TODO:
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
FPS = 30			# Frames per second
RField = (2370, 1140)	# Green Field
RWallwidth = 100		# Wall width in mm
RTapewidth = 50		# Line width in mm
RGoalwidth = 630		# Goal width in mm
RGoaldepth = 50		# Goal depth in mm
RBallsize = 50		# Ball diameter in mm

RPitch = (RField[0]+2*(RWallwidth+RTapewidth), RField[1]+2*(RWallwidth+RTapewidth))	# X, Y in mm
Rdx = 2			# To fit on screen
Rdy = 2
Fntsize = 36
Pitch = (RPitch[0]/Rdx, (RPitch[1]/Rdy))
Field = ((RField[0]+RTapewidth)/Rdx, ((RField[1]+RTapewidth)/Rdy))
Wallwidth = RWallwidth / Rdx
Tapewidth = RTapewidth / Rdx
Goalwidth = RGoalwidth / Rdy
Goaldepth = RGoaldepth / Rdx
Ballsize = RBallsize / Rdx
Ballradius = Ballsize / 2
Center = (Pitch[0]/2, Pitch[1]/2)
Res = (Pitch[0], Pitch[1] + Fntsize)		# Window Resolution
Xres = Res[0]
Yres = Res[1]
Edge = Wallwidth + Tapewidth
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
Frict = 0.99
CFrict = 0.55			# Collision Friction
Margin = 1
#==============================================================================

	#TODO Implement Character Object properties
#==============================================================================
	#  Game Object Classes

class Ball(pygame.sprite.Sprite):
	"""Sprite for ball on the pitch"""
	def __init__(self, posx = Center[0]-Ballradius, posy = Center[1]-Ballradius):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		#self.image = pygame.Surface([Ballsize, Ballsize])
		#self.image.fill(ORANGE)
		self.image, self.rect = load_image('ball.png', -1)
		self.image = pygame.transform.scale(self.image, (25, 25))
		self.rect = self.image.get_rect()
		
		#screen = pygame.display.get_surface()
		#self.area = screen.get_rect()
		self.pitch = pygame.Rect(Wallwidth, Wallwidth, Field[0], Field[1])
		self.pitch.center = Center
		#self.area = (Pitch[0], Pitch[1])
		#self.posx = 1000
		#self.posy = 1000
		self.rect.topleft = (posx, posy)
		self.speed = 0
		self.orientation = 0
		self.cnt = 0
		#self.touching = 0

	
	def update(self, dirxy, pushspeed, pushorient, bnc = 0, mv = 0, psh = 0):
		"Move Hero character based on key presses or change appearance"
		#pos = pygame.mouse.get_pos()
		#self.rect.midtop = pos
		#if self.punching:
			#self.rect.move_ip(5, 10)
		#if self.dying:
		#	self._dying()
		#else:
		if bnc == 1:
			self._bounce()
		elif mv == 1:
			self._move(dirxy)
		elif psh == 1:
			self._push(pushspeed, pushorient)

		self._newpos()
		
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
		
		
		
			
	def _newpos(self):
		"Update speed of ball"
		currpos = np.matrix(self.rect.center)
		mean = 0
		dev = 1
		if self.cnt >= 15  and self.speed != 0:
			rand = np.random.normal(mean, dev)
			self.cnt = 0
		else:
			rand = 0
		self.cnt = self.cnt + 1
		self.orientation = self.orientation + rand
		#xy = [1, -1]
		if self.orientation <= 0:
			self.orientation = 359
		elif self.orientation >= 360:
			self.orientation = 1
		if self.orientation >= 0 and self.orientation < 90:
			angle = self.orientation
			xy = [1, -1]
			xmod = self.speed * np.sin(np.deg2rad(angle))
			ymod = self.speed * np.cos(np.deg2rad(angle))
			
		elif self.orientation >= 90 and self.orientation < 180:
			angle = self.orientation - 90
			xy = [1, 1]
			xmod = self.speed * np.cos(np.deg2rad(angle))
			ymod = self.speed * np.sin(np.deg2rad(angle))
			
		elif self.orientation >= 180 and self.orientation < 270:
			angle = self.orientation - 180
			xy = [-1, 1]
			xmod = self.speed * np.sin(np.deg2rad(angle))
			ymod = self.speed * np.cos(np.deg2rad(angle))			
			
		elif self.orientation >= 270 and self.orientation <= 360:
			angle = self.orientation - 270
			xy = [-1, -1]
			xmod = self.speed * np.cos(np.deg2rad(angle))
			ymod = self.speed * np.sin(np.deg2rad(angle))
			
#		xmod = self.speed * np.sin(np.deg2rad(angle))
#		ymod = self.speed * np.cos(np.deg2rad(angle))
		xymod = np.matrix((xmod*xy[0], ymod*xy[1]))
		#self.nextpos = currpos + xymod + 
		self.nextpos = currpos + xymod
		
		if self.nextpos[0, 0] < self.pitch.left or \
		self.nextpos[0, 0] > self.pitch.right:
			self.orientation = 360 - self.orientation
			self.speed = self.speed * CFrict
#			if xy[0] == 1:
#				self.orientation = 180 - self.orientation
#			elif xy[1] == -1:
#				self.orientation = 540 - self.orientation
		if self.nextpos[0, 1] < self.pitch.top or \
		self.nextpos[0, 1] > self.pitch.bottom:
			self.speed = self.speed * CFrict
			if xy[0] == 1:
				self.orientation = 180 - self.orientation
			elif xy[0] == -1:
				self.orientation = 540 - self.orientation
			
		self.nextpos = currpos + xymod
		
		if self.nextpos[0, 0] < self.pitch.left:
			self.nextpos[0, 0] = self.pitch.left + Margin
		if self.nextpos[0, 0] > self.pitch.right:
			self.nextpos[0, 0] = self.pitch.right - Margin
		if self.nextpos[0, 1] < self.pitch.top:
			self.nextpos[0, 1] = self.pitch.top + Margin
		if self.nextpos[0, 1] > self.pitch.bottom:
			self.nextpos[0, 1] = self.pitch.bottom - Margin		
		
		move = self.nextpos.tolist()
		self.rect.center = move[0]
		
		self.speed = self.speed * Frict
		if self.speed <= 0.8:
			self.speed = 0
		
	def _move(self, dirxy):
		"Update position of the ball"
		#currpos = self.rect.move((self.move, 0))
		currpos = np.matrix(self.rect.center)
		xymat = np.matrix(dirxy)
		self.nextpos = currpos + xymat * self.speed
		#walls = (Wallwidth, Wallwidth)
		if self.nextpos[0, 0] > self.pitch.left and \
		self.nextpos[0, 0] < self.pitch.right and \
		self.nextpos[0, 1] > self.pitch.top and \
		self.nextpos[0, 1] < self.pitch.bottom:
			move = self.nextpos.tolist()
			self.rect.center = move[0]
			
	def _bounce(self, xymat = np.matrix((1, 1))):
		"Update position of the ball"
		#currpos = self.rect.move((self.move, 0))
		currpos = np.matrix(self.rect.center)
		
		self.nextpos = currpos + xymat * self.speed
		if self.nextpos[0, 0] < self.pitch.left or \
		self.nextpos[0, 0] > self.pitch.right:
			xymat[0, 0] = xymat[0, 0] * -1 
		if self.nextpos[0, 1] < self.pitch.top or \
		self.nextpos[0, 1] > self.pitch.bottom:
			xymat[0, 1] = xymat[0, 1] * -1
		self.nextpos = currpos + xymat * self.speed	
		move = self.nextpos.tolist()
		self.rect.center = move[0]
		
	def _push(self, sp, theta):
		"Updates position of the ball given speed and orientation"
		self.speed = sp
		self.orientation = theta
		

#class Hero(pygame.sprite.Sprite):
#	"""moves a clenched fist on the screen, following the mouse"""
#	def __init__(self):
#		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
#		self.image, self.rect = load_image('boy.png', -1)
#		screen = pygame.display.get_surface()
#		self.area = screen.get_rect()
#		self.rect.topleft = (10, 10)
#		self.speed = 20
#		self.touching = 0
#		self.dying = 0
#
#	def update(self,dirxy):
#		"Move Hero character based on key presses or change appearance"
#		#pos = pygame.mouse.get_pos()
#		#self.rect.midtop = pos
#		#if self.punching:
#			#self.rect.move_ip(5, 10)
#		if self.dying:
#			self._dying()
#		else:
#			self._move(dirxy)
#
#	def touch(self, target):
#		"Returns true if Ball collides with a target"
#		if not self.touching:
#			self.touching = 1
#			hitbox = self.rect.inflate(-5, -5)
#			return hitbox.colliderect(target.rect)
#
#	def _move(self, dirxy):
#		"Update position of the ball"
#		#currpos = self.rect.move((self.move, 0))
#		currpos = np.matrix(self.rect.center)
#		xymat = np.matrix(dirxy)
#		nextpos = currpos + xymat * self.speed
#		if nextpos[0, 0] > self.area.left and \
#		nextpos[0, 0] < self.area.right and \
#		nextpos[0, 1] > self.area.top and \
#		nextpos[0, 1] < self.area.bottom:
#			move = nextpos.tolist()
#			self.rect.center = move[0]
#
#	def _dying(self):
#		"Add sprite animations of character death = Explosions!"
#
#	def dead(self):
#		"Hero has been struck!"
#		self.dying = 1


#Im2 = load_image('hyptosis_tile2.png', -1)

#class Rock(pygame.sprite.Sprite):
#	"""Produces a Rock"""
#	def __init__(self, posxy):
#		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
#		#self.image, self.rect = load_image('Rock.png', -1)
#		#Im2.image, Im2.Rect = load_image('hyptosis_tile2.png', -1)
#		Im = pygame.image.load('Resources\hyptosis_tile2.png')
#		self.rect = pygame.Rect(196, 356, 60, 60)
#		self.image = Im.subsurface(self.rect)
#		screen = pygame.display.get_surface()
#		self.area = screen.get_rect()
#		self.rect.topleft = posxy
#		self.touching = 0

#==============================================================================



#  fpsClock = pygame.time.Clock()



def main():
	"""this function is called when the program starts. It initializes everything it needs, then runs in a loop until the function returns."""

	# Initialize Everything
	pygame.init()
	screen = pygame.display.set_mode((Res), 0)
	pygame.display.set_caption('Foosball Match')
	pygame.mouse.set_visible(1)

	# self.gamestate = 1  # 1 - run, 0 - exit

	# Create Background
	#TODO Implement Full (Tiled/Object) Background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(WALL)
	outlinebox = pygame.Rect(Wallwidth, Wallwidth, Pitch[0] - 2*Wallwidth, Pitch[1] - 2*Wallwidth)
	pitchbox = pygame.Rect(Edge, Edge, Pitch[0] - 2*Edge, Pitch[1] - 2*Edge)
	titlebox = pygame.Rect(0, Pitch[1], Xres, Yres)
	line1box = pygame.Rect(Pitch[0]*1/4-Linewidth/2, Wallwidth, Linewidth, Pitch[1]-2*Wallwidth)
	line2box = pygame.Rect(Pitch[0]*2/4-Linewidth/2, Wallwidth, Linewidth, Pitch[1]-2*Wallwidth)
	line3box = pygame.Rect(Pitch[0]*3/4-Linewidth/2, Wallwidth, Linewidth, Pitch[1]-2*Wallwidth)
	goalyellow=pygame.Rect(Wallwidth/2, Pitch[1]/2 - Goalwidth/2, Goaldepth, Goalwidth)
	goalblue=pygame.Rect(Pitch[0] - Wallwidth, Pitch[1]/2 - Goalwidth/2, Goaldepth, Goalwidth)

	pygame.draw.rect(background, TAPE, outlinebox, 0)
	pygame.draw.rect(background, GRASS, pitchbox, 0)
	pygame.draw.rect(background, TITLEBACK, titlebox, 0)
	pygame.draw.rect(background, TAPE, line1box, 0)
	pygame.draw.rect(background, TAPE, line2box, 0)
	pygame.draw.rect(background, TAPE, line3box, 0)
	pygame.draw.rect(background, YELLOW, goalyellow, 0)
	pygame.draw.rect(background, BLUE, goalblue, 0)
	pygame.draw.line(background, LINE, (Pitch[0]*1/4, Wallwidth), (Pitch[0]*1/4, Pitch[1]-Wallwidth))
	pygame.draw.line(background, LINE, (Pitch[0]*2/4, Wallwidth), (Pitch[0]*2/4, Pitch[1]-Wallwidth))
	pygame.draw.line(background, LINE, (Pitch[0]*3/4, Wallwidth), (Pitch[0]*3/4, Pitch[1]-Wallwidth))

	#pygame.draw.circle(background, ORANGE, (Center[0], Center[1]), Ballsize/2, 0)
		
	#Put Text On The Background, Centered
	if pygame.font:
		font = pygame.font.Font(None, Fntsize)
		text = font.render("Foosball Match", 1, TITLE)
		textpos = text.get_rect(centerx=Xres/2, centery=Yres - Fntsize/2)
		background.blit(text, textpos)

	#Display The Background
	screen.blit(background, (0, 0))
	pygame.display.flip()

#Prepare Game Objects
	clock = pygame.time.Clock()
	#hero = Hero()
	#rock1 = Rock((100, 100))
	#rock2 = Rock((200, 200))
	#blob = Blob()
	ball = Ball()
	ballsprite = pygame.sprite.RenderPlain(ball)
	#herosprite = pygame.sprite.RenderPlain((hero))
	#rocksprite = pygame.sprite.RenderPlain(rock1, rock2)
	#allsprites = pygame.sprite.RenderPlain((hero, rock, tree, gem, blob))

	## Loading Resources

	#numrocks = 3
	#tilecomp2 = pygame.image.load('Resources\hyptosis_tile2.png')
	#
	#self.catImg = pygame.image.load('cat.png')
	#self.boyImg = pygame.image.load('boy.png')
	#self.gemImg = pygame.image.load('gem1.png'), pygame.image.load('gem5.png'), pygame.image.load('gem3.png'), pygame.image.load('gem4.png')
	#self.treeImg = pygame.image.load('Tree_Short.png'), pygame.image.load('Tree_Tall.png'), pygame.image.load('Tree_Ugly.png')
	#
	#rock_rect = pygame.Rect(196, 357, 59, 59)
	#self.rockImg = tilecomp2.subsurface(rock_rect)
	## self.rockImg = [pygame.image.load('Rock.png')] * numrocks
	#
	#self.squirrImg = pygame.image.load('squirrel.png')
	#self.deadImg = pygame.image.load('inkspillspot.png')

	## FIELD OBJECT VARIABLES

	# Cat Variables

	#self.catx = Xres // 2		# Initial xpos for the cat agent
	#self.caty = Yres // 2		# Initial ypos for the cat agent
	#self.cat = Res // 2
	#self.cstep = 4				# Size of cat step
	#self.catmoves = 0			# Number of cat moves per second
	#self.catxoff, catyoff = catImg.get_size()
	#self.catwait = 30			# Reset value for catmoves
	#self.catspeed = 1			# How quickly to renew movement

	# Boy Variables

	#self.boyx = Xres // 4
	#self.boyy = Yres // 4
	#self.bstep = 10
	#self.boymoves = 0
	#self.boymovetimer = 0
	#self.boyspeed = 1
	#self.boywait = 4
	#self.boyxoff, boyyoff = boyImg.get_size()
	#self.bmrg = 10				# Boy Margin on edge of screen


	# Randomizing Gem & Tree locations

	#self.gem = numpy.random.random_integers(10, Xres - 100, 8).reshape((4, 2))
	#self.gemc = numpy.random.random_integers(10, Xres - 100, 8).reshape((4, 2))
	#self.tree = numpy.random.random_integers(10, 500, 6).reshape((3, 2))
	#self.rock = numpy.random.random_integers(10, 500, numrocks * 2).reshape((numrocks, 2))


	# Check if gems are still in play (1 Yes, 0 No)
	#gemobt = [1, 1, 1, 1]
	#
	## Calculate gem offset for collision detection
	#gemoff = gemImg[0].get_size()

	# Other variables

	frame = 0				# Current Frame
	#gembound = 30			# Collision boundary around gems
	#catboundx = 60			# Collision boundary around catx
	##catboundy = 35			# Collision boundary around caty
	#dead = 0				# Dead flag = Game Over!

	#self.loop()

	def fpsshow(name, x, fr=None):
		''' Show current frame on screen '''
		myfont = pygame.font.SysFont("monospace", 15)
		if fr != None:
			text = myfont.render(name + ':' + str(fr), 1, (255, 255, 0))
			screen.blit(text, (x * 15, Pitch[1] - Wallwidth + 10))
		else:
			text = myfont.render(name, 1, (255, 255, 0))
			screen.blit(text, (x * 15, Pitch[1] - Wallwidth + 10))

	#def game_exit(self):
		#exit()
	dirxy = [0, 0]
	once = 1
	bnc = 0
	mv = 0
	psh = 1
	going = True
	while going:			# Main game loop
		clock.tick(60)
		## GEMS UPDATE

		#for i in range(0,4):
			#if gemobt[i]:
				#self.surface.blit(gemImg[i], (gem[i,0], gem[i,1]))

		## BOY UPDATE

		#boymovetimer += 1

		#if boymovetimer == FPS // boymoves and dead == 0:
		#if not dead:
			#boymovetimer = 0

		# Handle Input Events
		#dirxy = [0, 0]
#		for event in pygame.event.get():
#			if event.type == QUIT:
#				going = False
#			elif event.type == KEYDOWN and event.key == K_ESCAPE:
#				going = False
#				print('User quit the game')
#			elif event.type == KEYDOWN:
#				keys = pygame.key.get_pressed()
#				if keys[K_LEFT]:
#					dirxy[0] = dirxy[0] - 1
#				if keys[K_RIGHT]:
#					dirxy[0] = dirxy[0] + 1
#				if keys[K_UP]:
#					dirxy[1] = dirxy[1] - 1
#				if keys[K_DOWN]:
#					dirxy[1] = dirxy[1] + 1
					
		#if ball.nextpos 

		#self.surface.blit(boyImg, (boyx, boyy))
	#
		#if dead == 1:
			#self.surface.blit(deadImg, (boyx - 10, boyy + 10))

	## CAT UPDATE
		#if catmoves <= 0:
			#catmoves = catwait
			#catran = random.randrange(1, 5)
			#if catran == 1:				# 'right':
				#catx += cstep
				#if catx >= Xres - 150:
					#catx -= cstep * 2
			#elif catran == 2:			# 'down':
				#caty += cstep
				#if caty >= Yres - 100:
					#caty -= cstep * 2
			#elif catran == 3:			# 'left':
				#catx -= cstep
				#if catx <= 10:
					#catx += cstep * 2
			#elif catran == 4:			# 'up':
				#caty -= cstep
				#if caty <= 10:
					#caty += cstep * 2

		#self.surface.blit(catImg, (catx, caty))

		## COLLISION Detector

		# Update Collision Positions
	#
		#boyc = (boyx + (boyxoff // 2), boyy + (boyyoff // 2))
		#catc = (catx + (catxoff // 2), caty + (catyoff // 2))
		##gemc[0,0] = (gem[0,0] + gemoff[0]//2)
	#
		#for i in range(0, 4):
			#gemc[i, 0] = (gem[i, 0] + gemoff[0] // 2)
			#gemc[i, 1] = (gem[i, 1] + gemoff[1] // 2)

		# Collision Time!

		#if (catc[0] + catboundx > boyc[0] > catc[0] - catboundx) and (catc[1] + catboundy > boyc[1] > catc[1] - catboundy):
			#dead = 1
	#
		#for i in range(0, 4):
			#if (gemc[i, 0] + gembound > boyc[0] > gemc[i, 0] - gembound) and (gemc[i, 1] + gembound > boyc[1] > gemc[i, 1] - gembound):
				#gemobt[i] = 0

		## GAME EVOLUTION
	#
		#if not gemobt[0]:
			#self.smth = 0
		#if not gemobt[1]:
			#if cstep >= 49:
				#cstep = 49
			#cstep += 1
		#if not gemobt[2]:
			#if catspeed >= 9:
				#catspeed = 9
			#catspeed += 1
		#if not gemobt[3]:
			#self.smth = 3

		## FPS & Other UPDATE



		# Update movement ticker
		#if boymoves > 0:
			#boymoves -= boyspeed
		#if catmoves > 0:
			#catmoves -= catspeed

		# End Game

		## Exit cases
		#for event in pygame.event.get():
			#if event.type == QUIT:
				#pygame.quit()
				#sys.exit()

		# Run update and tick
		#pygame.display.update()
		#fpsClock.tick(FPS)

		
		#herosprite.update(dirxy)
		#rocksprite.update()
		if once == 1:
			once = 0
			pushspeed = np.random.randint(10, 26)
			pushorient = np.random.randint(0, 360)	

		ballsprite.update(dirxy, pushspeed, pushorient, bnc, mv, psh)
		
		if psh == 1:
			psh = 0
		
		#Draw Everything
		screen.blit(background, (0, 0))
		ballsprite.draw(screen)
		#rocksprite.draw(screen)
		#herosprite.draw(screen)
		
		frame += 1
		fpsshow('Frame', 5, "%02d" % frame)
		fpsshow('Pos', 15, ball.rect.center)
		fpsshow('Speed', 25, np.around(ball.speed, 3))
		fpsshow('Theta', 35, np.around(ball.orientation, 2))

		if frame == 30:
			frame = 0		
		
		pygame.display.flip()
		
		if pygame.event.peek (QUIT):
			going = False  # Be IDLE friendly

	pygame.quit()
	sys.exit()

#==============================================================================
	# Run if called

if __name__ == '__main__':
	main()
	
#==============================================================================