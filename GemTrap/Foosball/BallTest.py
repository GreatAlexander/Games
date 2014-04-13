import unittest
import CommonTest
import Ball

class BallTest(CommonTest.CommonTest):
    def setUp(self):
        self.testBall = Ball.Ball()
        self.testInteger = 0
        self.dirXY = [0,0]

    def testCanSetBallBounceValue(self):
        self.setAttribute(self.testBall, Ball.Ball.setBounceValue, self.testInteger, "bounceValue")
        
    def testCanSetBallPushValue(self):
        self.setAttribute(self.testBall, Ball.Ball.setPushValue, self.testInteger, "pushValue")
        
    def testCanSetBallMoveValue(self):
        self.setAttribute(self.testBall, Ball.Ball.setMoveValue, self.testInteger, "moveValue")
        
    def testCanSetBallPushSpeed(self):
        self.setAttribute(self.testBall, Ball.Ball.setPushSpeed, self.testInteger, "pushSpeed")

    def testCanSetBallPushOrientation(self):
        self.setAttribute(self.testBall, Ball.Ball.setPushOrientation, self.testInteger, "pushOrientation")
        
    def testCanSetBallDirXY(self):
        self.setAttribute(self.testBall, Ball.Ball.setDirXY, self.dirXY, "dirXY")

if __name__ == "__main__":
    unittest.main()