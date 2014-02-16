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


#==============================================================================


#==============================================================================
	#  Game Object Classes


#==============================================================================
	# Main Process
def main():
	"""this function is called when the program starts. It initializes everything it needs, then runs in a loop until the function returns."""

	# Initialize Everything
	pygame.init()

#==============================================================================
	# Main Loop
	going = True
	while going:			# Main game loop
		clock.tick(60)
		if pygame.event.peek (QUIT):
			going = False  # Be IDLE friendly

	pygame.quit()
	sys.exit()

#==============================================================================
	#  Run if called

if __name__ == '__main__':
	main()

#==============================================================================