import requests
import unittest
import json
import os
import datetime
import hashlib
import sys
import re


class A5AcceptanceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testURL = os.environ["url"] + "/2048"
        cls.userID = os.environ["id"]
        cls.userName = os.environ["name"]
        cls.opString = '?op=shift'
        cls.gridKey = 'grid'
        cls.scoreKey = 'score'
        cls.directionKey = 'direction'
        cls.integrityKey = 'integrity'
        cls.statusKey = 'status'
        cls.errorValue = 'error'
      
    @classmethod  
    def tearDownClass(cls):
        pass       
     
# microservice helper methods
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
    
# 2048-specific helper methods
    def invokeMicroservice(self, inputParmDict):
        parmString = self.constructParms(inputParmDict)
        theURL = self.testURL + self.opString + '&' + '&'.join(parmString)
        actualResult = self.microservice(theURL)
        self.assertEqual(200, actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')
        return actualResult
    
    def generateHash(self, parmDict):
        expectedHashString = str(parmDict['grid']) + "." + str(parmDict['score'])
        theHash = hashlib.sha256()
        theHash.update(expectedHashString.encode())
        hashValue = theHash.hexdigest().upper()
        return hashValue  
    
    def constructParms(self, parmDict):
        parmString = []
        for key in parmDict:
            parmString.append(key + "=" + parmDict[key])
        
        return parmString
    
#-------------------------------------------------------------------------------
# -- Acceptance tests for microservice deployment
#   test 010:   intent:  to ensure microservice has been deployed 
#                 input: http://name-of-server.com/2048?op=shift 
#                 output: status code 200
    def testA5_2048_010_ShouldReturn200ResponseCode(self):
        theURL = self.testURL
        actualResult = self.microservice(theURL)
        self.assertEqual(200 , actualResult['statusCode'], f'Microservice not accessible at {theURL} [major]')

#-------------------------------------------------------------------------------
# -- Acceptance tests for op=shift
# Interface Analysis
#    input:  dictionary consisting of the following keys
#        grid -> string; 
#                digits;
#                parses into:  0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024;
#                mandatory; 
#                arrives unvalidated
#        score -> string;
#                even integer .GE. 0;
#                mandatory;
#                arrives unvalidated
#        direction -> string;
#                one of {up, down, right, left};
#                case agnostic;
#                optional, default to 'down' if missing
#                arrives unvalidated
#        integrity -> string;
#                uppercase sha256 hexdigest of grid + "."  + score
#                mandatory,
#                arrives unvalidated
#    output: dictionary consisting of the following keys:  grid, score, status, integrity
#        Happy path:
#            scenario 1:    general
#                010:    ensure return of all keys
#            scenario 2:    valid input grid
#                020:    pass grid with all possible tiles
#            scenario 3:    valid input score
#                030:    pass nominal score
#            scenario 4:    valid input direction
#                040:    pass nominal direction in lower case
#                050:    pass nominal direction in mixed case
#                060:    pass missing direction
#                070:    pass omitted direction
#            scenario 5:    valid input integrity
#                080:    pass nominal integrity
#            scenario 6:    valid output grid
#                090:    validate shift up for nominal grid
#                100:    validate shift down for nominal grid
#                110:    validate shift right for nominal grid
#                120:    validate shift left for nominal grid
#                125:    validate shift with no score change
#                130:    validate random 2/4 tiles
#            scenario 7:    valid status
#                140:    validate status = win
#                        all other status tests omitted due to requirements ambiguity
#        Sad path:
#            scenario 1:    grid
#                910:    missing grid
#                920:    unparsable grid
#            scenario 2:    score
#                930:    missing score
#                940:    nonint score
#                950:    score .LT. 0
#                960:    uneven score
#            scenario 3:    direction
#                970:    direction not one of up/down/left/right
#            scenario 4:    integrity
#                980:    invalid integrity
#
# Side-Effect Analysis
#    no side effects
#
# Acceptable level of risk:   BVA
# ------------------------------------------
# Happy Path Analysis
#   test 010:   intent:  op=shift responds with dictionary with of requisite keys 
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2200000000000000
#                            &score=0
#                            &direction=up
#                            &integrity=0C1E79CDC2D6D5FBA1A31203029C5D951EE92DBC87CB64BA80C41D58A2DE036E
#                 output: 
#                     {'grid':'do not care',
#                      'score':'do not care'
#                      'integrity':'do not care',
#                      'status': 'do not care'}
    def testA5_shift_010_ShouldReturnAllKeys(self):
        opString = '?op=shift'
        parmString = ['grid=2200000000000000',
                      'score=0',
                      'direction=down',
                      'integrity=0C1E79CDC2D6D5FBA1A31203029C5D951EE92DBC87CB64BA80C41D58A2DE036E']
        theURL = self.testURL + opString + '&' + '&'.join(parmString)
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

#   test 020:   intent:  op=shift handles a grid with all possible tiles 
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2481632641282565121024000000
#                            &score=100
#                            &direction=left
#                            &integrity=<calculated>
#                 output: 
#                     {'grid':'2481632641282565121024xxxxxx',  (where x = don't care)
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_020_ShouldHandleAllPossibleTiles(self):
        inputParmDict = {self.gridKey: '2481632641282565121024220000',
                         self.scoreKey: '100',
                         self.directionKey: 'left',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '24816326412825651210244',
                            self.scoreKey: '104',
                            self.directionKey: None,
                            self.integrityKey: None}

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualGridValue = actualResult.get(self.gridKey, "")
        self.assertTrue(actualGridValue.startswith(expectedParmDict[self.gridKey]),
                        f'Invalid return grid [major]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue)
        
        expectedParmDict[self.integrityKey] = self.generateHash(actualResult)    
        actualIntegrityValue = actualResult.get(self.integrityKey, "")
        self.assertEqual(expectedParmDict[self.integrityKey], actualIntegrityValue,
                           f'Invalid return integrity [major]')

#   test 030:   intent:  op=shift pass nominal score 
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2400000000000000
#                            &score=1234
#                            &direction=left
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': don't care,  (where x = don't care)
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_030_ShouldHandleNominalScore(self):
        inputParmDict = {self.gridKey: '2200000000000000',
                         self.scoreKey: '128',
                         self.directionKey: 'left',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '4',
                            self.scoreKey: '132',
                            self.directionKey: None,
                            self.integrityKey: None}

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')
        
        actualGridValue = actualResult.get(self.gridKey, "")
        self.assertTrue(actualGridValue.startswith(expectedParmDict[self.gridKey]),
                        f'Invalid return grid [major]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue)
        
        expectedParmDict[self.integrityKey] = self.generateHash(actualResult)    
        actualIntegrityValue = actualResult.get(self.integrityKey, "")
        self.assertEqual(expectedParmDict[self.integrityKey], actualIntegrityValue,
                           f'Invalid return integrity [major]')

#   test 040:   intent:  op=shift pass nominal direction in lower case 
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2200000000000000
#                            &score=1234
#                            &direction=left
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': don't care,  (where x = don't care)
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_040_ShouldHandleLowerCaseDirection(self):
        self.testA5_shift_030_ShouldHandleNominalScore()
        
#   test 050:   intent:  op=shift pass nominal direction in mixed case 
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2400000000000000
#                            &score=1234
#                            &direction=Left
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': don't care,  (where x = don't care)
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_050_ShouldHandleCaseAgnosticDirection(self):
        inputParmDict = {self.gridKey: '2200000000000000',
                         self.scoreKey: '128',
                         self.directionKey: 'lEft',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '4',
                            self.scoreKey: '132',
                            self.directionKey: None,
                            self.integrityKey: None}

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualGridValue = actualResult.get(self.gridKey, "")
        self.assertTrue(actualGridValue.startswith(expectedParmDict[self.gridKey]),
                        f'Invalid return grid [minor]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue,
                         f'Invalid return score [minor]')
        
        expectedParmDict[self.integrityKey] = self.generateHash(actualResult)    
        actualIntegrityValue = actualResult.get(self.integrityKey, "")
        self.assertEqual(expectedParmDict[self.integrityKey], actualIntegrityValue,
                           f'Invalid return integrity [minor]')
        
#   test 060:   intent:  op=shift pass missing direction 
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2400000000000000
#                            &score=1234
#                            &direction=
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': don't care,  (where x = don't care)
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_060_ShouldHandleMissingDirection(self):
        inputParmDict = {self.gridKey: '0000000000002222',
                         self.scoreKey: '128',
                         self.directionKey: '',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '2222',
                            self.scoreKey: '128',
                            self.statusKey: None,
                            self.integrityKey: None}

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualGridValue = actualResult.get(self.gridKey, "")
        self.assertTrue(actualGridValue.endswith(expectedParmDict[self.gridKey]),
                        f'Invalid return grid [minor]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue,
                         f'Invalid return score [minor]')
        
        expectedParmDict[self.integrityKey] = self.generateHash(actualResult)    
        actualIntegrityValue = actualResult.get(self.integrityKey, "")
        self.assertEqual(expectedParmDict[self.integrityKey], actualIntegrityValue,
                           f'Invalid return integrity [minor]')

#   test 070:   intent:  op=shift pass omitted direction 
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2400000000000000
#                            &score=1234
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': don't care,  (where x = don't care)
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_070_ShouldHandleOmittedDirection(self):
        inputParmDict = {self.gridKey: '0000000000002222',
                         self.scoreKey: '128',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '2222',
                            self.scoreKey: '128',
                            self.statusKey: None,
                            self.integrityKey: None}

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')
        
        actualGridValue = actualResult.get(self.gridKey, "")
        self.assertTrue(actualGridValue.endswith(expectedParmDict[self.gridKey]),
                        f'Invalid return grid [minor]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue,
                         f'Invalid return score [minor]')
        
        expectedParmDict[self.integrityKey] = self.generateHash(actualResult)    
        actualIntegrityValue = actualResult.get(self.integrityKey, "")
        self.assertEqual(expectedParmDict[self.integrityKey], actualIntegrityValue,
                           f'Invalid return integrity [minor]')

#   test 080:   intent:  op=shift pass nominal integrity
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2400000000000000
#                            &score=1234
#                            &direction=down
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': don't care,  (where x = don't care)
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_080_ShouldHandleNominalIntegrity(self):
        inputParmDict = {self.gridKey: '0000000000002222',
                         self.scoreKey: '128',
                         self.directionKey: 'down',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '2222',
                            self.scoreKey: '128',
                            self.statusKey: None,
                            self.integrityKey: None}

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')

#   test 090:   intent:  op=shift validate shift up
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=200162400248162480
#                            &score=1234
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': '\A48163244.*'
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_090_ShouldHandleUpShift(self):
        inputParmDict = {self.gridKey: '200162400248162480',
                         self.scoreKey: '100',
                         self.directionKey: 'up',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '\A48163244.*',
                            self.scoreKey: '164',
                            self.statusKey: None,
                            self.integrityKey: None}        

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')
        
        actualGridValue = actualResult.get(self.gridKey, "")
        actual2ExpectedMatch = re.match(expectedParmDict[self.gridKey], actualGridValue)
        self.assertIsNotNone(actual2ExpectedMatch,
                        f'Invalid return grid on shift up [major]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue,
                         f'Invalid return score on shift up [major]')
        
#   test 100:   intent:  op=shift validate shift down
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=160420482164020082
#                            &score=1234
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': '\A..........44328164'
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_100_ShouldHandleDownShift(self):
        inputParmDict = {self.gridKey: '160420482164020082',
                         self.scoreKey: '100',
                         self.directionKey: 'down',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '\A..........44328164',
                            self.scoreKey: '164',
                            self.statusKey: None,
                            self.integrityKey: None}        

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        print(actualStatusValue)
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')
        
        actualGridValue = actualResult.get(self.gridKey, "")
        actual2ExpectedMatch = re.match(expectedParmDict[self.gridKey], actualGridValue)
        self.assertIsNotNone(actual2ExpectedMatch,
                        f'Invalid return grid on shift down [major]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue,
                         f'Invalid return score on shift down [major]')
        
#   test 110:   intent:  op=shift validate shift left
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=160160044880082222
#                            &direction=left
#                            &score=1234
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': '\A..........44328164'
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_110_ShouldHandleLeftShift(self):
        inputParmDict = {self.gridKey: '160160044880082222',
                         self.scoreKey: '100',
                         self.directionKey: 'left',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '\A32...88..16...44..',
                            self.scoreKey: '164',
                            self.statusKey: None,
                            self.integrityKey: None}        

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')
        
        actualGridValue = actualResult.get(self.gridKey, "")
        actual2ExpectedMatch = re.match(expectedParmDict[self.gridKey], actualGridValue)
        self.assertIsNotNone(actual2ExpectedMatch,
                        f'Invalid return grid on shift left [major]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue,
                         f'Invalid return score on shift left [major]')
        
#   test 120:   intent:  op=shift validate shift right
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=160160044880082222
#                            &score=1234
#                            &direction=right
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': '\A..........44328164'
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_120_ShouldHandleRightShift(self):
        inputParmDict = {self.gridKey: '160160044880082222',
                         self.scoreKey: '100',
                         self.directionKey: 'right',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '\A...32..88...16..44',
                            self.scoreKey: '164',
                            self.statusKey: None,
                            self.integrityKey: None}        

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')
        
        actualGridValue = actualResult.get(self.gridKey, "")
        actual2ExpectedMatch = re.match(expectedParmDict[self.gridKey], actualGridValue)
        self.assertIsNotNone(actual2ExpectedMatch,
                        f'Invalid return grid on shift right [major]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue,
                         f'Invalid return score on shift right [major]')
        
#   test 125:   intent:  op=shift validate shift with no score change
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2200000000000000
#                            &score=04
#                            &direction=right
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': '\A4.*'
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_125_ShouldHandleShiftWithNoScoreChange(self):
        inputParmDict = {self.gridKey: '2400000000000000',
                         self.scoreKey: '0',
                         self.directionKey: 'left',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '\A24..............',
                            self.scoreKey: '0',
                            self.statusKey: None,
                            self.integrityKey: None}        

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')
        
        actualGridValue = actualResult.get(self.gridKey, "")
        actual2ExpectedMatch = re.match(expectedParmDict[self.gridKey], actualGridValue)
        self.assertIsNotNone(actual2ExpectedMatch,
                        f'Invalid return grid on shift right [major]')
        
        actualScoreValue = str(actualResult.get(self.scoreKey, 0))
        self.assertEqual(expectedParmDict[self.scoreKey], actualScoreValue,
                         f'Invalid return score on shift right [major]')
        
#   test 130:   intent:  op=shift validate random tiles
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=160160044880082222
#                            &score=1234
#                            &direction=right
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': '\A..........44328164'
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_130_ShouldHandleRandomTiles(self):
        inputParmDict = {self.gridKey: '4400000000000000',
                         self.scoreKey: '8',
                         self.directionKey: 'left',
                         self.integrityKey: None}      

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertFalse(actualStatusValue.startswith(self.errorValue),
                         f'Result inappropriately flagged as error')

        sampleSize = 32
        tolerance = 0.50
        twoTileTally = 0
        fourTileTally = 0
        for _ in range(sampleSize):
            actualResult = self.invokeMicroservice(inputParmDict)
            actualGridValue = actualResult.get(self.gridKey, '0')
            twoTileCount = actualGridValue.count('2')
            fourTileCount = actualGridValue.count('4')
            zeroTileCount = actualGridValue.count('0')
            randomTileCount = twoTileCount + fourTileCount + zeroTileCount
            self.assertEqual(15, randomTileCount,
                             f'Incorrect random tile added')
            twoTileTally += twoTileCount
            fourTileTally += fourTileCount
        tileDifference = abs(twoTileTally - fourTileTally) / sampleSize
        self.assertLessEqual(tileDifference, tolerance)
        
#   test 140:   intent:  op=shift validate status=win
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=2200000000000000
#                            &score=04
#                            &direction=right
#                            &integrity=<calculated>
#                 output: 
#                     {'grid': '\A4.*'
#                      'score':100
#                      'integrity':calculated,
#                      'status': 'ok'}
    def testA5_shift_140_ShouldHandleWinStatus(self):
        inputParmDict = {self.gridKey: '1024102400000000000000',
                         self.scoreKey: '0',
                         self.directionKey: 'left',
                         self.integrityKey: None}
        expectedParmDict = {self.gridKey: '.',
                            self.scoreKey: '0',
                            self.statusKey: None,
                            self.integrityKey: None}        

        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertEqual('win', actualStatusValue,
                         f'status should be win but is {actualStatusValue}')

# ------------------------------------------
# Sad Path Analysis        
#
#   test 910:   intent:  op=shift test for error on omitted grid
#                 input: http://name-of-server.com/2048?op=shift
#                            &score=0
#                            &direction=down
#                            &integrity=<calculated>
#                 output: 
#                     {'status': 'error'}
    def testA5_shift_910_ShouldReturnErrorOnOmittedGrid(self):
        inputParmDict = {self.scoreKey: '0',
                         self.directionKey: 'down',
                         self.integrityKey: 'B14D280E705BFB10C16285A8F744B93C79611B1D4F770E4D970D38ADEFBD0DE7'}   
               
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertTrue(actualStatusValue.startswith(self.errorValue),
                         f'Failure to detect omitted grid') 
        
#   test 920:   intent:  op=shift test for error on unparsable grid
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=000000000000001024
#                            &score=0
#                            &direction=down
#                            &integrity=<calculated>
#                 output: 
#                     {'status': 'error'}
    def testA5_shift_920_ShouldReturnErrorOnInvalidGrid(self):
        inputParmDict = {self.gridKey: '000000000000001024',
                         self.scoreKey: '0',
                         self.directionKey: 'down',
                         self.integrityKey: None}   
               
        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertTrue(actualStatusValue.startswith(self.errorValue),
                         f'Failure to detect invalid grid') 
        
#   test 930:   intent:  op=shift test for error on missing score
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=000000000000001024
#                            &score=0
#                            &direction=down
#                            &integrity=<calculated>
#                 output: 
#                     {'status': 'error'}
    def testA5_shift_930_ShouldReturnErrorOnMissingScore(self):
        inputParmDict = {self.gridKey: '4400000000000000',
                         self.scoreKey: '',
                         self.directionKey: 'down',
                         self.integrityKey: None}   
               
        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertTrue(actualStatusValue.startswith(self.errorValue),
                         f'Failure to detect missing score') 

#   test 940:   intent:  op=shift test for error on nonint score
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=000000000000001024
#                            &score=a
#                            &direction=down
#                            &integrity=<calculated>
#                 output: 
#                     {'status': 'error'}
    def testA5_shift_940_ShouldReturnErrorOnNonIntScore(self):
        inputParmDict = {self.gridKey: '4400000000000000',
                         self.scoreKey: 'a',
                         self.directionKey: 'down',
                         self.integrityKey: None}   
               
        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertTrue(actualStatusValue.startswith(self.errorValue),
                         f'Failure to detect non-int score') 
        
#   test 950:   intent:  op=shift test for error on negative score
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=000000000000001024
#                            &score=-1
#                            &direction=down
#                            &integrity=<calculated>
#                 output: 
#                     {'status': 'error'}
    def testA5_shift_950_ShouldReturnErrorOnOutOfBoundsScore(self):
        inputParmDict = {self.gridKey: '4400000000000000',
                         self.scoreKey: '-2',
                         self.directionKey: 'down',
                         self.integrityKey: None}   
               
        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertTrue(actualStatusValue.startswith(self.errorValue),
                         f'Failure to detect out-of-bounds score') 
        
#   test 960:   intent:  op=shift test for error on uneven score
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=000000000000001024
#                            &score=13
#                            &direction=down
#                            &integrity=<calculated>
#                 output: 
#                     {'status': 'error'}
    def testA5_shift_960_ShouldReturnErrorOnOddScore(self):
        inputParmDict = {self.gridKey: '4400000000000000',
                         self.scoreKey: '13',
                         self.directionKey: 'down',
                         self.integrityKey: None}   
               
        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertTrue(actualStatusValue.startswith(self.errorValue),
                         f'Failure to detect uneven score') 
        
#   test 970:   intent:  op=shift test for error on invalid direction
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=4400000000000000
#                            &score=0
#                            &direction=d
#                            &integrity=<calculated>
#                 output: 
#                     {'status': 'error'}
    def testA5_shift_970_ShouldReturnErrorOnInvalidDirection(self):
        inputParmDict = {self.gridKey: '4400000000000000',
                         self.scoreKey: '0',
                         self.directionKey: 'd',
                         self.integrityKey: None}   
               
        inputParmDict['integrity'] = self.generateHash(inputParmDict) 
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertTrue(actualStatusValue.startswith(self.errorValue),
                         f'Failure to detect invalid direction') 
        
#   test 980:   intent:  op=shift test for error on invalid integrity
#                 input: http://name-of-server.com/2048?op=shift
#                            &grid=4400000000000000
#                            &score=0
#                            &direction=down
#                            &integrity=<calculated>
#                 output: 
#                     {'status': 'error'}
    def testA5_shift_980_ShouldReturnErrorOnInvalidDirection(self):
        inputParmDict = {self.gridKey: '4400000000000000',
                         self.scoreKey: '0',
                         self.directionKey: 'down',
                         self.integrityKey: '9E3556058DD89CFF0F1F0667F2F6AD5DFB78B096A83ECD07870E1A2CEE009A71'}   
               
        actualResult = self.invokeMicroservice(inputParmDict)
        
        actualStatusValue = actualResult.get(self.statusKey, '')
        self.assertTrue(actualStatusValue.startswith(self.errorValue),
                         f'Failure to detect invalid integrity')


if __name__ == "__main__":
    try:
        print(" ")
        print("@A5  " + os.environ["id"])
        print("      " + os.environ["name"])        
        print("      " + os.environ["url"])
        print("      " + str(datetime.datetime.now()))
        print("+------------------------------------------------------------------")    
    except:
        print("@A5  -- id/url not available")
        sys.exit()
    unittest.main()  
