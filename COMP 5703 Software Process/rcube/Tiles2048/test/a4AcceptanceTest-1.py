import requests
import unittest
import json
import os
import datetime
import sys
import re
import hashlib


class A4AcceptanceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testURL = os.environ["url"] + "/2048"
        cls.userID = os.environ["id"]
        cls.userName = os.environ["name"]
      
    @classmethod  
    def tearDownClass(cls):
        pass       
     
    def microservice(self, theURL):
        '''Issue HTTP/HTTPS request and capture the JSON result'''
        try:
            theResponse = requests.get(theURL)
            theBody = theResponse.text
            theResult = {'statusCode': theResponse.status_code}
        except Exception as e:
            theResult['diagnostic1'] = str(e)
            theResult['statusCode'] = 999
            return theResult
             
        '''Convert JSON string to dictionary'''
        try:
            theJsonBody = theBody.replace("'", "\"")
            theDictionaryBody = json.loads(theJsonBody)
            for element in theDictionaryBody:
                if(isinstance(theDictionaryBody[element], str)):
                    theResult[str(element)] = str(theDictionaryBody[element])
                else:
                    theResult[str(element)] = theDictionaryBody[element]
        except Exception as e:
            theResult['diagnostic2'] = str(e)
        return theResult    
    
#-------------------------------------------------------------------------------
# -- Acceptance tests for microservice deployment
#   test 010:   intent:  to ensure microservice has been deployed 
#                 input: http://name-of-server.com/2048?op=create 
#                 output: status code 200
    def testA4_2048_010_ShouldReturn200ResponseCode(self):
        theURL = self.testURL
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')

#-------------------------------------------------------------------------------
# -- Acceptance tests for op=create
# Interface Analysis
#    input:  dictionary consists of no parameter keys
#    output: dictionary consisting of the following keys:  grid, score, status, integrity
#        Happy path:
#            010:    ensure return of all keys
#            020:    ensure return of "ok" status value
#            030:    ensure return of accurate integrity value
#            040:    ensure return of 0 score value
#            050:    ensure grid has 2 '2' tiles, empty otherwise
#            060:    ensure randomness of '2' tiles 
#            grid -> two 2 tiles places at random on otherwise empty grid
#            score -> 0
#            integrity -> SHA256 hex digest of grid + . + score
#            status -> "ok"
#        Sad path:
#            N/A
#
# Side-Effect Analysis
#    no side effects
#
# Acceptable level of risk:   BVA
# Happy Path Analysis

#   test 010:   intent:  op=create responds with dictionary with of requisite keys 
#                 input: http://name-of-server.com/2048?op=create 
#                 output: 
#                     {'grid':'do not care',
#                      'score':'do not care'
#                      'integrity':'do not care',
#                      'status': 'do not care'}
    def testA4_create_010_ShouldReturnAllKeys(self):
        opString = '?op=create'
        theURL = self.testURL + opString
        expectedResult = {'grid':'',
                          'score':'',
                          'integrity':'',
                          'status': 0}
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')
        for key in expectedResult:
            self.assertIn(key, actualResult, f"key {key} is missing [major]")
        actualResultCount = len(actualResult) - 1  # decrement to account for statusCode
        expectedResultCount = len(expectedResult)
        self.assertEqual(expectedResultCount, actualResultCount, f'{actualResultCount} items returned, {expectedResultCount} expected')

#   test 020:   intent:  status = ok  
#               input: http://name-of-server.com/2048?op=create 
#               output: contains {'status':'ok')
    def testA4_create_020_ShouldReturnOkStatus(self):
        opString = '?op=create'
        theURL = self.testURL + opString
        expectedKey = 'status'
        expectedContent = 'ok'
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')
        self.assertIn(expectedKey, actualResult)
        self.assertEqual(actualResult.get(expectedKey, None), expectedContent)
        
#    test 030:  intent:  integrity is valid
#                input:  http://name-of-server.com/2048?op=create
#                output:  contains {'integrity':'xxx'}, where
#                    xxx = sha256(value of grid + "." + value of score)
    def testA4_create_030_ShouldReturnValidIntegrity(self):
        opString = '?op=create'
        theURL = self.testURL + opString
        print(theURL)
        expectedIntegrityKey = 'integrity'
        expectedGridKey = 'grid'
        expectedScoreKey = 'score'
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')
        actualGrid = actualResult.get(expectedGridKey, '')
        actualScore = str(actualResult.get(expectedScoreKey, ''))
        actualIntegrity = actualResult.get(expectedIntegrityKey, '')
        expectedHashString = actualGrid + "." + actualScore
        myHash = hashlib.sha256()
        myHash.update(expectedHashString.encode())
        expectedIntegrity = myHash.hexdigest().upper() 
        self.assertEqual(expectedIntegrity, actualIntegrity, f'Integrity values do not match for {expectedHashString} [major]')
        
#    test 040:  intent:  score is an integer 0
#                input:  http://name-of-server.com/2048?op=create
#                output:  contains {'score':0}
#
    def testA4_create_040_ShouldReturnIntZeroScore(self): 
        opString = '?op=create'
        theURL = self.testURL + opString
        expectedKey = 'score'
        expectedContent = '0'
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')
        self.assertIn(expectedKey, actualResult, f'score is missing')
        actualContent = str(actualResult.get(expectedKey, None))
        self.assertEqual(expectedContent, actualContent, f'Score is not set to 0')
        
#    test 050:  intent:  ensure grid has correct syntax
#                input:  http://name-of-server.com/2048?op=create
#                output:  'grid' consists of 14 '0' and 2 '2'
#                method:  run 16 times; the results should be consistent
#   
    def testA4_create_050_ShouldReturnCorrectGridSyntax(self): 
        opString = '?op=create'
        theURL = self.testURL + opString
        expectedKey = 'grid'
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')
        
        sampleSize = 31
        for _ in range(sampleSize):
            actualResult = self.microservice(theURL)
            actualGrid = actualResult.get(expectedKey, '')
            zeroCount = actualGrid.count('0')
            self.assertEqual(zeroCount, 14, f'{zeroCount} zero tiles discovered')
            twoCount = actualGrid.count('2')
            self.assertEqual(twoCount, 2, f'{twoCount} zero tiles discovered')
            
#    test 060:  intent:  ensure grid has random placement of '2' tiles
#                input:  http://name-of-server.com/2048?op=create
#                output:  'grid' consists of 14 '0' and 2 '2'
#                method:  run 16 times; the results should be consistent
#   
    def testA4_create_060_ShouldReturnCorrectGridSyntax(self): 
        GRID_SIZE = 16
        TWO_TILE_VALUE = 2
        TWO_TILES_ON_GRID = 2
        ZERO_TILE = 0
        SAMPLE_SIZE = 32
        P = 18.2  # Chi-Squared   df=15; alpha=0.75
        
        def uniformTest():
            population = [0 for _ in range(GRID_SIZE)]
            for _ in range(SAMPLE_SIZE):
                actualResult = self.microservice(theURL)
                actualStringGrid = actualResult.get(expectedKey, ZERO_TILE * GRID_SIZE)
                actualNumericGrid = [int(int(char) / TWO_TILE_VALUE) for char in actualStringGrid]
                for index in range(len(population)):
                    population[index] += actualNumericGrid[index]
        
            expected = TWO_TILES_ON_GRID / GRID_SIZE * SAMPLE_SIZE 
            chiSquared = 0.0
            for cell in population:
                chiSquared += ((cell - expected) ** 2) / expected
            return chiSquared
        
        opString = '?op=create'
        theURL = self.testURL + opString
        expectedKey = 'grid'
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')
        
        uniformity = P ** 2
        for _ in range(5):
            try:
                chiSquared = uniformTest()
                if(P > chiSquared):
                    uniformity = chiSquared
                    break
                else:
                    uniformity = min(uniformity, chiSquared)
            except:
                uniformity = P ** 2
        self.assertGreater(P, uniformity, f'2s not uniformly distributed across grid')

#-------------------------------------------------------------------------------
# -- Acceptance tests for op=info
# Interface Analysis
#    input:  dictionary consists of no parameter keys
#    output: dictionary consisting of the userid key
#        Happy path:
#            userid -> username
#        Sad path:
#            N/A
#
# Side-Effect Analysis
#    no side effects
#
# Acceptable level of risk:   BVA
    def testA4_info_010_ShouldReturnUserid(self):
        opString = '?op=info'
        theURL = self.testURL + opString
        expectedResult = {'user': self.userID}
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')
        for key in expectedResult:
            self.assertIn(key, actualResult, f"key {key} is missing [major]")
        actualUserId = actualResult.get('user', None)
        self.assertEqual(actualUserId, self.userID)
        actualResultCount = len(actualResult) - 1  # decrement to account for statusCode
        expectedResultCount = len(expectedResult)
        self.assertEqual(expectedResultCount, actualResultCount, f'{actualResultCount} items returned, {expectedResultCount} expected')


if __name__ == "__main__":
    try:
        print(" ")
        print("@A4  " + os.environ["id"])
        print("      " + os.environ["name"])        
        print("      " + os.environ["url"])
        print("      " + str(datetime.datetime.now()))
        print("+------------------------------------------------------------------")    
    except:
        print("@A4  -- id/url not available")
        sys.exit()
    unittest.main()  
