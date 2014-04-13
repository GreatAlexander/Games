import pygame

class MovingObject(pygame.sprite.Sprite):
    
    def __init__(self, name="name", speed=0, orientation=0, frameCount=0):
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
    
    
    
    
    
    
    
    



