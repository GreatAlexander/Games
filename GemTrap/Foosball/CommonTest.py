import unittest

class CommonTest(unittest.TestCase):
    
    def setAttribute(self, objectGettingSet, setterFunction, value, valueName):
        setterFunction(objectGettingSet, value)
        self.assertEqual(objectGettingSet.__getattribute__(valueName), value, "object."+str(value)+" is not equal to "+str(value))    
        
if __name__ == "__main__":
    unittest.main()