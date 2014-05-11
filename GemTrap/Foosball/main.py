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

	ball.setName("ball")
	blue1.setName("blue1")
	blue2.setName("blue2")
	red1.setName("red1")
	red2.setName("red2")

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
		clock.tick(FPS)

		if frame >= 30:
			frame = 0
		else:
			frame += 1

		allData = [ball, blue1, blue2, red1, red2]
		if (frame % WORLD_MODEL_UPDATE) == 0:
			WM.update_info(allData)

		#Update Sprites
		ballSprite.update()
		blue1Sprite.update()
		blue2Sprite.update()
		red1Sprite.update()
		red2Sprite.update()

		#Draw Everything
		display.drawEverything(background, ballSprite, blue1Sprite, blue2Sprite, red1Sprite, red2Sprite)
		display.updateFeaturesOnScreen(frame, ball, blue1, blue2, red1, red2)

		#Check for kicks
		ball.setPushValue(0)
		if blue1.kicking or blue2.kicking or red1.kicking or red2.kicking:
			ball.setPushValue(1)
			ball.setPushSpeed(5)
		if blue1.kicking:
			ball.setPushOrientation(blue1.angle)
		elif blue2.kicking:
			ball.setPushOrientation(blue2.angle)
		elif red1.kicking:
			ball.setPushOrientation(red1.angle)
		elif red2.kicking:
			ball.setPushOrientation(red2.angle)
#
#		ball.setPushValue(0)
#
#		if ball.speed == 0:
#			ball.setPushValue(1)
#			ball.setPushOrientation(np.random.randint(0, 360))
#			ball.setPushSpeed(5)

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