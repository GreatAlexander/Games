# -*- coding: utf-8 -*-

#==============================================================================
# FOOSBALL - by Alejandro Bordallo and Andrew Robinson
# Details: Foozball game sim for autonomous agents, simple ai, path planning
#==============================================================================
import PygameWrapper as pygw
import sys
import numpy as np
from Display import Display
from Ball import Ball
from Agent import Agent
from Global import *
	
def main():
	"""This is the main function called when the program starts. It initializes 
	everything it needs, then runs in a loop until exited. """

	display = Display()
	
	background = display.drawBackground()
	display.drawPitch(background)
	display.centreTitleOnBackground(background)

	# Prepare Game Objects
#	clock = pygame.time.Clock()
	clock = pygw.clock()
	ball = Ball()
	blue1 = Agent(BLUE1_START, 1)
	red2 = Agent(RED2_START, 4)
	
	
#	ballSprite = pygame.sprite.RenderPlain(ball)
	ballSprite = pygw.renderplainsprite(ball)
	blue1Sprite = pygw.renderplainsprite(blue1)
#	blue2Sprite = pygw.renderplainsprite(blue2)
#	red1Sprite = pygw.renderplainsprite(red1)
	red2Sprite = pygw.renderplainsprite(red2)

	frame = 0
	going = True
	
	# Main game loop
	while going:			
		clock.tick(60)
		
		#Update Everything
		ballSprite.update()
		blue1Sprite.update()
		ball.setPushValue(0)
		frame += 1
		
		#Draw Everything
		display.drawEverything(background, ballSprite, blue1Sprite, red2Sprite)
		display.updateFeaturesOnScreen(frame, ball)

		if frame == 30:
			frame = 0
			
		if ball.speed == 0:
			ball.setPushValue(1)
			ball.setPushOrientation(np.random.randint(0, 360))
			ball.setPushSpeed(15)
		
#		pygame.display.flip()
		pygw.updatefulldisplay()
		
#		for event in pygame.event.get():
		for event in pygw.getIOevent():
			if event.type == pygw.QUIT or event.type == pygw.KEYDOWN and event.key == pygw.K_ESCAPE:
				going = False
				print('User quit the game')

#	pygame.quit()
	pygw.quitgame()
	sys.exit()

if __name__ == '__main__':
	main()