import pygame
from copy import copy

class MovingObject(pygame.sprite.Sprite):
    
    def __init__(self, name="", speed=0, orientation=0, frameCount=0):
        pygame.sprite.Sprite.__init__(self)
        self.setName(name)
        self.setSpeed(speed)
        self.setOrientation(orientation)
        self.setFrameCount(frameCount)
         
    def setName(self, name):
        self.name = name
    
    def setSpeed(self, speed):
        self.speed = speed

    def setOrientation(self, orientation):
        self.orientation = orientation
 
    def setFrameCount(self, frameCount):
        self.frameCount = frameCount
    
    def updateCurrentWorld(self, currentWorld):
        try:
            currentWorld[self.name] = copy(self) #may need deepcopy but deepcopy is slow
        except KeyError:
            raise MovingObjectHasNoNameError("Object has no name so can not make a key in the world model dictionary for it.")
        


class MovingObjectHasNoNameError(Exception):
    pass
    
    
    
    
    
    



