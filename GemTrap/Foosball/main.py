# -*- coding: utf-8 -*-
"""
#==============================================================================
# FOOSBALL - by Alejandro Bordallo and Andrew Robinson
# Details: Foozball game sim for autonomous agents, simple ai, path planning
#==============================================================================
"""
import PygameWrapper as pygw
import sys
import numpy as np
from Display import Display
from Ball import Ball
from Agent import Agent
from WorldModel import WorldModel
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
	WM = WorldModel()
	ball = Ball()
	blue1 = Agent(BLUE1_START_POS, 1, BLUE_START_ANGLE, WM)
	blue2 = Agent(BLUE2_START_POS, 2, BLUE_START_ANGLE, WM)
	red1 = Agent(RED1_START_POS, 3, RED_START_ANGLE, WM)
	red2 = Agent(RED2_START_POS, 4, RED_START_ANGLE, WM)


#	ballSprite = pygame.sprite.RenderPlain(ball)
	ballSprite = pygw.renderplainsprite(ball)
	blue1Sprite = pygw.renderplainsprite(blue1)
	blue2Sprite = pygw.renderplainsprite(blue2)
	red1Sprite = pygw.renderplainsprite(red1)
	red2Sprite = pygw.renderplainsprite(red2)

	frame = 0
	going = True

	# Main game loop
	while going:
		clock.tick(60)

		if frame >= 30:
			frame = 0
		else:
			frame += 1

		if (frame % WORLD_MODEL_UPDATE) == 0:
			WM.update_info(ball.center, ball.speed, ball.orientation, \
			blue1.pos, blue1.angle, blue2.pos, blue2.angle, red1.pos, \
			red1.angle, red2.pos, red2.angle)

		#Update Sprites
		ballSprite.update()
		blue1Sprite.update()
		blue2Sprite.update()
		red1Sprite.update()
		red2Sprite.update()

		#Draw Everything
		display.drawEverything(background, ballSprite, blue1Sprite, blue2Sprite, red1Sprite, red2Sprite)
		display.updateFeaturesOnScreen(frame, ball, blue1, blue2, red1, red2)

		ball.setPushValue(0)

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