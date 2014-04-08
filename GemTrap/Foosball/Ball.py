import pygame
import numpy as np
from Global import *
from Loader import load_image

class Ball(pygame.sprite.Sprite):
    """Sprite for ball on the pitch"""
    def __init__(self, posx = CENTRE[0]-BALL_RADIUS, posy = CENTRE[1]-BALL_RADIUS):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        #self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        #self.image.fill(ORANGE)
        self.image, self.rect = load_image('ball.png', -1)
        self.image = pygame.transform.scale(self.image, (25, 25))
        #self.rect = self.image.get_rect()
        
        #screen = pygame.display.get_surface()
        #self.area = screen.get_rect()
        self.pitch = pygame.Rect(WALL_WIDTH, WALL_WIDTH, Field[0], Field[1])
        self.pitch.center = CENTRE
        #self.area = (PITCH[0], PITCH[1])

        self.rect.topleft = (posx, posy)
        self.speed = 0
        self.orientation = 0
        self.count = 0
        #self.touching = 0

    
    def update(self, dirxy, pushSpeed, pushOrient, bounce = 0, move = 0, push = 0):
        '''Update ball position.
        '''
        if bounce == 1:
            self._bounce()
        elif move == 1:
            self._move(dirxy)
        elif push == 1:
            self._push(pushSpeed, pushOrient)
												
        self._updatePosition()
        
#    def calcangle(oldpos, newpos):
#        "Calculate angle from 2 x,y cordinates"
#        xneg = 0
#        yneg = 0
#        xdif = oldpos[0] - newpos [0]        
#        ydif = oldpos[1] - newpos[1]
#        
#        if xdif < 0:
#            xneg = 1
#            xdif = abs(xdif)
#        if ydif < 0:
#            yneg = 1
#            ydif = abs(ydif)                
        
    def _updatePosition(self):
        "Update speed and position of ball."
        self.changeDirectionSlightlyAfterNSteps(60)
        xymod, xy = self.computeDynamics()
        
        self.getNextPosition(xymod)    
        if self.hasHitWall():
            self.bounceOffWall(xy)
            self.moveBallToBeWithinPitch()
            
        move = self.nextPosition.tolist()
        self.rect.center = move[0]
        
        self.slowDownDueToTableFriction()
        self.stopIfSlowEnough(0.8)

    def changeDirectionSlightlyAfterNSteps(self, steps):
        self.count += 1
        if self.count >= steps  and self.speed != 0:
            self.count = 0
            self.orientation +=  np.random.normal(0, 1)
    
    def computeDynamics(self):
        angle = self.orientation % 90
        if self.orientation >= 0 and self.orientation < 90 or self.orientation >= 180 and self.orientation < 270:
            xmod = self.speed * np.sin(np.deg2rad(angle))
            ymod = self.speed * np.cos(np.deg2rad(angle))
        if self.orientation >= 90 and self.orientation < 180 or self.orientation >= 270 and self.orientation <= 360:
            xmod = self.speed * np.cos(np.deg2rad(angle))
            ymod = self.speed * np.sin(np.deg2rad(angle))
        xy = self.getXY()
        return np.matrix((xmod*xy[0], ymod*xy[1])), xy
    
    def getXY(self):
        self.orientation %= 360
        if self.orientation >= 0 and self.orientation < 90:
            return [1, -1]
        elif self.orientation >= 90 and self.orientation < 180:
            return [1, 1]    
        elif self.orientation >= 180 and self.orientation < 270:
            return [-1, 1]                
        elif self.orientation >= 270 and self.orientation <= 360:
            return [-1, -1]
    
    def getNextPosition(self, xymod):
        currentPosition = np.matrix(self.rect.center)
        self.nextPosition = currentPosition + xymod
        
    def hasHitWall(self):
        return self.hasGoneOffField()
    
    def hasGoneOffField(self):
        return self.hasGoneOffFieldSide() or self.hasGoneOffFieldEnd()
    
    def hasGoneOffFieldSide(self):
        return self.hasGoneOffFieldLeft() or self.hasGoneOffFieldRight()
    
    def hasGoneOffFieldLeft(self):
        return self.nextPosition[0, 0] < self.pitch.left
        
    def hasGoneOffFieldRight(self):
        return self.nextPosition[0, 0] > self.pitch.right
    
    def hasGoneOffFieldEnd(self):
        return self.hasGoneOffFieldTop() or self.hasGoneOffFieldBottom()
    
    def hasGoneOffFieldTop(self):
        return self.nextPosition[0, 1] < self.pitch.top
    
    def hasGoneOffFieldBottom(self):    
        return self.nextPosition[0, 1] > self.pitch.bottom
    
    def bounceOffWall(self, xy):
        if self.hasGoneOffFieldSide():
            self.orientation = 360 - self.orientation
        elif self.hasGoneOffFieldEnd():
            if xy[0] == 1:
                self.orientation = 180 - self.orientation
            elif xy[0] == -1:
                self.orientation = 540 - self.orientation
        self.slowDownDueToCollisionFriction()
#        self.speed *= COLLISION_FRICTION
        
    def moveBallToBeWithinPitch(self):
        if self.hasGoneOffFieldLeft():
            self.nextPosition[0, 0] = self.pitch.left + MARGIN
        elif self.hasGoneOffFieldRight():
            self.nextPosition[0, 0] = self.pitch.right - MARGIN
        elif self.hasGoneOffFieldTop():
            self.nextPosition[0, 1] = self.pitch.top + MARGIN
        elif self.hasGoneOffFieldBottom():
            self.nextPosition[0, 1] = self.pitch.bottom - MARGIN
            
    
    def slowDownDueToTableFriction(self):
        self.slowDownDueToFriction(TABLE_FRICTION)
        
    def slowDownDueToCollisionFriction(self):
        self.slowDownDueToFriction(COLLISION_FRICTION)
        
    def slowDownDueToFriction(self, friction):
        self.speed *= friction
                
    def stopIfSlowEnough(self, threshold):
        if self.speed <= threshold:
            self.speed = 0
        
    def _move(self, dirxy):
        '''Update position of the ball
        '''
        currentPosition = np.matrix(self.rect.center)
        xymat = np.matrix(dirxy)
        self.nextPosition = currentPosition + xymat * self.speed
        if not self.hasGoneOffField():
            move = self.nextPosition.tolist()
            self.rect.center = move[0]
            
    def _bounce(self, xymat = np.matrix((1, 1))):
        '''Update position of the ball
        '''
        self.getNextPosition(xymat*self.speed)
        
        if self.hasGoneOffFieldSide():
            xymat[0, 0] *= -1 
        if self.hasGoneOffFieldEnd():
            xymat[0, 1] *= -1
            
        self.getNextPosition(xymat*self.speed)    
        move = self.nextPosition.tolist()
        self.rect.center = move[0]
        
    def _push(self, speed, theta):
        '''Updates position of the ball given speed and orientation
        '''
        self.speed = speed
        self.orientation = theta