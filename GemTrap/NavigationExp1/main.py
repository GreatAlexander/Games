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

		if pygame.event.peek (QUIT):
			going = False  # Be IDLE friendly

	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()