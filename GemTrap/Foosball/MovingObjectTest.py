import unittest
from MovingObject import MovingObject
import CommonTest

class MovingObjectTest(CommonTest.CommonTest):
    def setUp(self):
        self.testMovingObject = MovingObject()
        self.testName = "testName"
        self.testSpeed = 1
        self.testOrientation = 0
        self.testFrameCount = 0
        
    def testCanSetMovingObjectName(self):
        self.setAttribute(self.testMovingObject, MovingObject.setName, self.testName, "name")
        
    def testCanSetMovingObjectSpeed(self):
        self.setAttribute(self.testMovingObject, MovingObject.setSpeed, self.testSpeed, "speed")

    def testCanSetMovingObjectOrientation(self):
        self.setAttribute(self.testMovingObject, MovingObject.setOrientation, self.testOrientation, "orientation")
        
    def testCanSetMovingObjectFrameCount(self):
        self.setAttribute(self.testMovingObject, MovingObject.setFrameCount, self.testFrameCount, "frameCount")
        
if __name__ == "__main__":
    unittest.main()