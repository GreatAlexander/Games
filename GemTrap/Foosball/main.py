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
	#pygame.draw.circle(background, ORANGE, (CENTRE[0], CENTRE[1]), BALL_SIZE/2, 0)
	display.centreTitleOnBackground(background)

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
		display.drawEverything(background, ballSprite)
		
		frame += 1
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