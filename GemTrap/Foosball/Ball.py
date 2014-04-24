import PygameWrapper as pygw
import numpy as np
from Global import *
import Loader
import MovingObject

class Ball(MovingObject.MovingObject):
    """Sprite for ball on the pitch"""
    def __init__(self, posx = CENTRE[0], 
                 posy = CENTRE[1], bounceValue=0, 
                 pushValue=0, moveValue=0, pushSpeed = 0, pushOrientation = 0,
                 dirXY = [0,0]):
        
        MovingObject.MovingObject.__init__(self)
        self.load_image()
        
        self.setBounceValue(bounceValue)
        self.setPushValue(pushValue)
        self.setMoveValue(moveValue)
        self.setPushSpeed(pushSpeed)
        self.setPushOrientation(pushOrientation)
        self.setDirXY(dirXY)
#        self.pitch = pygame.Rect(WALL_WIDTH, WALL_WIDTH, FIELD[0], FIELD[1])
        self.pitch = pygw.rectangle(WALL_WIDTH, WALL_WIDTH, FIELD[0], FIELD[1])
        self.pitch.center = CENTRE

        self.rect.center = (posx, posy)

    def setBounceValue(self, bounceValue):
        self.bounceValue = bounceValue 
    
    def setPushValue(self, pushValue):
        self.pushValue = pushValue

    def setMoveValue(self, moveValue):
        self.moveValue = moveValue

    def setPushSpeed(self, pushSpeed):
        self.pushSpeed = pushSpeed
    
    def setPushOrientation(self, pushOrientation):
        self.pushOrientation = pushOrientation
    
    def setDirXY(self, dirXY):
        self.dirXY = dirXY
        
    def load_image(self):
        self.image, self.rect = Loader.load_image('ball.png', -1)
#        self.image = pygame.transform.scale(self.image, (25, 25))
        self.image = pygw.transform(self.image, (25,25))
        
    def update(self):
        '''Update ball position.
        '''
        if self.bounceValue == 1:
            self._bounce()
        elif self.moveValue == 1:
            self._move()
        elif self.pushValue == 1:
            self._push()
            
        self._updatePosition()
        
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
       
    def _move(self):
        '''Update position of the ball
        '''
        currentPosition = np.matrix(self.rect.center)
        xymat = np.matrix(self.dirXY)
        self.nextPosition = currentPosition + xymat * self.speed
        if not self.hasGoneOffField():
            move = self.nextPosition.tolist()
            self.rect.center = move[0]
        
    def _push(self):
        '''Updates position of the ball given speed and orientation
        '''
        self.setSpeed(self.pushSpeed)
        self.setOrientation(self.pushOrientation)           
        
    def _updatePosition(self):
        "Update speed and position of ball."
        self.changeDirectionSlightlyAfterNSteps(1)
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
        self.frameCount += 1
        if self.frameCount >= steps  and self.speed != 0:
            self.frameCount = 0
            self.orientation +=  RANDOM_DEVIATION * np.random.normal(0, 1)
    
    def computeDynamics(self):
        self.orientation %= 360
        angle = self.orientation % 90
        if self.orientation >= 0 and self.orientation < 90 or self.orientation >= 180 and self.orientation < 270:
            xmod = self.speed * np.sin(np.deg2rad(angle))
            ymod = self.speed * np.cos(np.deg2rad(angle))
        elif self.orientation >= 90 and self.orientation < 180 or self.orientation >= 270 and self.orientation <= 360:
            xmod = self.speed * np.cos(np.deg2rad(angle))
            ymod = self.speed * np.sin(np.deg2rad(angle))
        xy = self.getXY()
        return np.matrix((xmod*xy[0], ymod*xy[1])), xy
    
    def getXY(self):
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
        return self.nextPosition[0, 0] < self.pitch.left + MARGIN
        
    def hasGoneOffFieldRight(self):
        return self.nextPosition[0, 0] > self.pitch.right - MARGIN + BALL_SIZE
    
    def hasGoneOffFieldEnd(self):
        return self.hasGoneOffFieldTop() or self.hasGoneOffFieldBottom()
    
    def hasGoneOffFieldTop(self):
        return self.nextPosition[0, 1] < self.pitch.top + MARGIN
    
    def hasGoneOffFieldBottom(self):    
        return self.nextPosition[0, 1] > self.pitch.bottom - MARGIN + BALL_SIZE
    
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
            self.nextPosition[0, 0] = self.pitch.right - MARGIN + BALL_SIZE
        elif self.hasGoneOffFieldTop():
            self.nextPosition[0, 1] = self.pitch.top + MARGIN
        elif self.hasGoneOffFieldBottom():
            self.nextPosition[0, 1] = self.pitch.bottom - MARGIN + BALL_SIZE
            
    
    def slowDownDueToTableFriction(self):
        self.slowDownDueToFriction(TABLE_FRICTION)
        
    def slowDownDueToCollisionFriction(self):
        self.slowDownDueToFriction(COLLISION_FRICTION)
        
    def slowDownDueToFriction(self, friction):
        self.speed *= friction
                
    def stopIfSlowEnough(self, threshold):
        if self.speed <= threshold:
            self.speed = 0

                    
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
    
    
    
    
    
    
