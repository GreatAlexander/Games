# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 12:32:45 2014

@author: AlexBEAST
"""

#==============================================================================
# PyGame Wrapper library - by Alejandro Bordallo
# Details: This is a simple wrapper library to make the rest of the code 
# 		portable if we ever use something else instead of PyGame
#==============================================================================

import pygame
from pygame.locals import *

def imageload(name):
	return pygame.image.load(name)

def rectangle(x1, y1, x2, y2):
	return pygame.Rect(x1, y1, x2, y2)
	
def transform(image, scale):
	"""Resize Surface to new resolution"""
	return pygame.transform.scale(image, scale)
	
def clock():
	return pygame.time.Clock()
	
def renderplainsprite(sprite):
	return pygame.sprite.RenderPlain(sprite)
	
def updatefulldisplay():
	"""Update the full display Surface to the screen"""
	return pygame.display.flip()
	
def getIOevent():
	return pygame.event.get()
	
def catcherror():
	return pygame.error
	
def quitgame():
	return pygame.quit()