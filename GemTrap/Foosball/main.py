# -*- coding: utf-8 -*-

#==============================================================================
# FOOSBALL - by Alejandro Bordallo and Andrew Robinson
# Details: Foozball game sim for autonomous agents, simple ai, path planning
#==============================================================================

import pygame, sys
from pygame.locals import *
import numpy as np
from Display import Display
from Ball import Ball
from Global import *
	
def main():
	"""This is the main function called when the program starts. It initializes 
	everything it needs, then runs in a loop until exited. """

	display = Display()
	
	background = display.drawBackground()
	display.drawPitch(background)
	display.centreTitleOnBackground(background)

	# Prepare Game Objects
	clock = pygame.time.Clock()
	ball = Ball()
	
	ballSprite = pygame.sprite.RenderPlain(ball)

	frame = 0
	going = True
	
	# Main game loop
	while going:			
		clock.tick(60)
		
		#Update Everything
		ballSprite.update()
		ball.setPushValue(0)
		frame += 1
		
		#Draw Everything
		display.drawEverything(background, ballSprite)
		display.updateFeaturesOnScreen(frame, ball)

		if frame == 30:
			frame = 0
			
		if ball.speed == 0:
			ball.setPushValue(1)
			ball.setPushOrientation(np.random.randint(0, 360))
			ball.setPushSpeed(15)
		
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				going = False
				print('User quit the game')

	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()