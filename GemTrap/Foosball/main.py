# -*- coding: utf-8 -*-

#==============================================================================
# FOOSBALL - by Alejandro Bordallo and Andrew Robinson
# Details: Foozball game sim for autonomous agents, simple ai, path planning
# TODO: Fix the weird bouncing angles that came from refactoring
#==============================================================================

import pygame, sys
from pygame.locals import *
import numpy as np
from Display import Display
from Ball import Ball
from Global import *
	
def main():
	"""this function is called when the program starts. It initializes 
	everything it needs, then runs in a loop until the function returns.
	"""

	display = Display()
	#TODO Implement Full (Tiled/Object) Background
	background = display.drawBackground()
	display.drawPitch(background)
	display.centreTitleOnBackground(background)

	# Prepare Game Objects
	clock = pygame.time.Clock()
	ball = Ball(pushValue = 1, pushSpeed = 15, 
			pushOrientation = np.random.randint(0, 360), dirXY = [0, 0])
	
	ballSprite = pygame.sprite.RenderPlain(ball)

	frame = 0
	going = True
	
	# Main game loop
	while going:			
		clock.tick(60)
		
		#Update Everything
		ballSprite.update()
		ball.pushValue = 0
		frame += 1
		
		#Draw Everything
		display.drawEverything(background, ballSprite)
		display.updateFeaturesOnScreen(frame, ball)

		if frame == 30:
			frame = 0		
		
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				going = False
				print('User quit the game')

	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()