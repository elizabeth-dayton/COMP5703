import unittest
import Assignment.primesInRange as primesInRange

class PrimeInRangeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

# Sample happy path test
    def test100_100_ShouldDeterminePrimesInNominalRange(self):
        lowBound = 2
        highBound = 10
        expectedResult = [2, 3, 5, 7]
        actualResult = primesInRange.primesInRange(lowBound, highBound)
        self.assertListEqual(expectedResult, actualResult)
     
#Test to make sure values of low bound that are below 1 and greater
#than 1000 are not accepted   
    def test2_checkLowerBounds(self):
        lowbound_1 = 1001
        lowbound_2 = 0
        highbound_dummy = 5
        result_1 = primesInRange.primesInRange(lowbound_1, highbound_dummy)
        result_2 = primesInRange.primesInRange(lowbound_2, highbound_dummy)
        self.assertIsNone(result_1)
        self.assertIsNone(result_2)
        
#Test to make sure values of high bound that are below 1 and greater
#than 1000 are not accepted             
    def test3_checkHigherBounds(self):
        highbound_1 = 1001
        highbound_2 = 0
        lowbound_dummy = 5
        result_1 = primesInRange.primesInRange(lowbound_dummy, highbound_1)
        result_2 = primesInRange.primesInRange(lowbound_dummy, highbound_2)
        self.assertIsNone(result_1)
        self.assertIsNone(result_2)
        
#Test to make sure that an input with low bound being larger than high bound 
#is not accepted           
    def test4_checkLowBoundIsSmallerThanHighBound(self):
        lowbound = 4
        highbound = 3
        result = primesInRange.primesInRange(lowbound, highbound)
        self.assertIsNone(result)
        
#Tests to make sure that both low bound and high bound are of type int
    def test5_checkForTypeInt(self):
        lowbound_1 = 'a'
        highbound_1 = 1
        lowbound_2 = 2
        highbound_2 = 'b'   
        result_1 = primesInRange.primesInRange(lowbound_1, highbound_1)
        result_2 = primesInRange.primesInRange(lowbound_2, highbound_2)   
        self.assertIsNone(result_1)
        self.assertIsNone(result_2)
        
#Tests to make sure that neither input is None
    def test6_checkForNoneTypeInputs(self):
        lowbound_1 = None
        highbound_1 = 1
        lowbound_2 = 2
        highbound_2 = None   
        result_1 = primesInRange.primesInRange(lowbound_1, highbound_1)
        result_2 = primesInRange.primesInRange(lowbound_2, highbound_2)   
        self.assertIsNone(result_1)
        self.assertIsNone(result_2) 
        
#Another happy path test
    def test7_checkWorkingPrimesInRange_1(self):
        lowBound = 950
        highBound = 1000
        expectedResult = [953, 967, 971, 977, 983, 991, 997]
        actualResult = primesInRange.primesInRange(lowBound, highBound)
        self.assertListEqual(expectedResult, actualResult)
        
#Yet another happy path test
    def test8_checkWorkingPrimesInRange_2(self):
        expectedResult = [953, 967, 971, 977, 983, 991, 997]
        actualResult = primesInRange.primesInRange(lowBound=950, highBound=1000)
        self.assertListEqual(expectedResult, actualResult)
        
#And yet another happy path test
    def test9_checkWorkingPrimesInRange_3(self):
        lowBound = 11
        highBound = 11
        expectedResult = [11]
        actualResult = primesInRange.primesInRange(lowBound, highBound)
        self.assertListEqual(expectedResult, actualResult)
        
#And somehow yet another happy path test
    def test10_checkWorkingPrimesInRange_4(self):
        lowBound = 34
        highBound = 35
        expectedResult = []
        actualResult = primesInRange.primesInRange(lowBound, highBound)
        self.assertListEqual(expectedResult, actualResult)
        
        
        
        
        
        
        
        
        
        