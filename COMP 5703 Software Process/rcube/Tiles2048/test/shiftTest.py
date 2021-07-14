import unittest
import Tiles2048.create as create
import Tiles2048.shift as shift
import hashlib

class ShiftTest(unittest.TestCase):

#--------------------------------------------------------------
#The following tests all test negative outcomes (error messages)
#--------------------------------------------------------------
    
#Tests to make sure that the correct error is returned when there is a missing grid value
    def test_shift_missing_grid_value(self):
       
        userParmsCreate = {'op': 'create', 'size': '4'}
        
        grid = create._create(userParmsCreate)
        
        integrityKey = 'integrity'
        
        userParmsShift = {'op': 'shift', 'grid': None, 'score': '0', 'direction': 'down', \
                     'integrity': grid.get(integrityKey, '')}
        
        expectedErrorMessage = {'status': 'error: missing grid'}
        
        actualErrorMessage = shift._shift(userParmsShift)
        self.assertEqual(actualErrorMessage, expectedErrorMessage, 'Shift does not display correct error for missing grid input')

#Tests to make sure the correct error is returned when there an invalid character in the grid    
    def test_shift_invalid_grid_value1(self):
        
        userParmsCreate = {'op': 'create', 'size': '4'}
        
        grid = create._create(userParmsCreate)
        
        integrityKey = 'integrity'
        gridKey = 'grid'
        
        userParmsShift = {'op': 'shift', 'grid': grid.get(gridKey, '') + 'a', 'score': '0', 'direction': 'down', \
                    'integrity': grid.get(integrityKey, '')}
        
        expectedErrorMessage = {'status': 'error: invalid grid - contains invalid character'}
        
        actualErrorMessage = shift._shift(userParmsShift)
        self.assertEqual(actualErrorMessage, expectedErrorMessage, \
                    'Shift does not display correct error for invalid grid input (added invalid character)')
        
#Tests to make sure the grid contains only valid numbers (powers of 2)
    def test_shift_invalid_grid_value2(self):
        
        integrityString = '00002481600001280361' + "." + '0'        
        myHash = hashlib.sha256()
        myHash.update(integrityString.encode())
        integrity = myHash.hexdigest().upper()
               
        userParmsShift = {'op': 'shift', 'grid': '00002481600001280361', 'score': '0', 'direction': 'down', \
                    'integrity': integrity}
        
        expectedErrorMessage = {'status': 'error: missing grid'}
        
        actualErrorMessage = shift._shift(userParmsShift)
        self.assertEqual(actualErrorMessage, expectedErrorMessage, \
                    'Shift does not display correct error for invalid grid input (invalid number in grid)')
        
#Tests to make sure that the grid is of the proper length of characters
    def test_shift_invalid_grid_value3(self):

        integrityString = '000024816' + "." + '0'        
        myHash = hashlib.sha256()
        myHash.update(integrityString.encode())
        integrity = myHash.hexdigest().upper()

        userParmsShift = {'op': 'shift', 'grid': '000024816', 'score': '0', 'direction': 'down', \
                    'integrity': integrity}
        
        expectedErrorMessage = {'status': 'error: invalid grid - not enough characters'}
        
        actualErrorMessage = shift._shift(userParmsShift)
        self.assertEqual(actualErrorMessage, expectedErrorMessage, \
                    'Shift does not display correct error for invalid grid input (grid does not have proper amount of characters)')
        
#Tests to make sure the score is a valid number (i.e. a multiply of 2)
    def test_shift_invalid_score_value(self):
        
        userParmsShift = {'op': 'shift', 'grid': '000024816000024816', 'score': '33', 'direction': 'down', \
                    'integrity': ''}
        
        expectedErrorMessage = {'status': 'error: invalid score - not divisible by 2'}
        
        actualErrorMessage = shift._shift(userParmsShift)
        self.assertEqual(actualErrorMessage, expectedErrorMessage, \
                    'Shift does not display correct error for invalid score input')
        
#Tests to make sure the integrity value is correct
    def test_shift_invalid_integrity_value(self):
        
        
        userParmsShift = {'op': 'shift', 'grid': '2020202020202020', 'score': '0', 'direction': 'down', \
                     'integrity': 'B942E8D41B4'}
        
        expectedErrorMessage = {'status': 'error: bad integrity value'}
        
        actualErrorMessage = shift._shift(userParmsShift) 
        
        self.assertEqual(actualErrorMessage, expectedErrorMessage, 'Shift does not display correct error for invalid integrity value')
        
#Tests to make sure direction value is valid
    def test_shift_invalid_direction_value(self):
        
        integrityString = '00002481600001280361' + "." + '0'        
        myHash = hashlib.sha256()
        myHash.update(integrityString.encode())
        integrity = myHash.hexdigest().upper()
    
        userParmsShift = {'op': 'shift', 'grid': '00002481600001280361', 'score': '0', 'direction': 'back', \
                     'integrity': integrity}
        
        expectedErrorMessage = {'status': 'error: invalid direction'}
        
        actualErrorMessage = shift._shift(userParmsShift) 
        
        self.assertEqual(actualErrorMessage, expectedErrorMessage, 'Shift does not display correct error for invalid direction value')
        
#Tests to make sure that it catches that a shift is not possible
#This test isn't really necessary since if a shift isn't possible, it just means the game is lost
#     def test_shift_no_shift_possible(self):
#         
#         integrityString = '24816168422481616842' + "." + '0'        
#         myHash = hashlib.sha256()
#         myHash.update(integrityString.encode())
#         integrity = myHash.hexdigest().upper()
#         
#         userParmsShift = {'op': 'shift', 'grid': '24816168422481616842', 'score': '0', 'direction': 'down', \
#                      'integrity': integrity}
#         
#         expectedErrorMessage = {'status': 'error: no shift possible'}
#         
#         actualErrorMessage = shift._shift(userParmsShift) 
#         
#         self.assertEqual(actualErrorMessage, expectedErrorMessage, 'Shift does not display correct error for no shift possible')
        
#--------------------------------------------------------------
#The following tests all test positive outcomes (no error messages)
#--------------------------------------------------------------

#Tests to make sure the movement of tiles is correctly implemented in all directions
    def test_shift_all_directional_shifts(self):
        
        #all of the valid shift values are left, right, down, and up
        grid1 = '0020000000002000'
        grid2 = '2022440482801616164'
        
        hashString = grid1 + "." + '0'
        myHash = hashlib.sha256()
        myHash.update(hashString.encode())
        integrity1 = myHash.hexdigest().upper()
        
        hashString = grid2 + "." + '0'
        myHash = hashlib.sha256()
        myHash.update(hashString.encode())
        integrity2 = myHash.hexdigest().upper()
        
        userParmsShiftLeft1 = {'op': 'shift', 'grid': grid1, 'score': '0', 'direction': 'left', \
                     'integrity': integrity1}
        userParmsShiftRight1 = {'op': 'shift', 'grid': grid1, 'score': '0', 'direction': 'right', \
                     'integrity': integrity1}
        userParmsShiftDown1 = {'op': 'shift', 'grid': grid1, 'score': '0', 'direction': 'down', \
                     'integrity': integrity1} 
        userParmsShiftUp1 = {'op': 'shift', 'grid': grid1, 'score': '0', 'direction': 'up', \
                     'integrity': integrity1}
        
        userParmsShiftLeft2 = {'op': 'shift', 'grid': grid2, 'score': '0', 'direction': 'left', \
                     'integrity': integrity2}
        userParmsShiftRight2 = {'op': 'shift', 'grid': grid2, 'score': '0', 'direction': 'right', \
                     'integrity': integrity2}
        
        gridKey = 'grid'
        
        leftShiftOutput1 = shift._shift(userParmsShiftLeft1)
        actualGridLeft1 = leftShiftOutput1.get(gridKey, '')
        expectedGridLeft1 = '2000000000002000'
        self.assertEqual(actualGridLeft1[0], expectedGridLeft1[0], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft1[12], expectedGridLeft1[12], 'Shift does not shift to the left correctly')
         
        leftShiftOutput2 = shift._shift(userParmsShiftLeft2)
        actualGridLeft2 = leftShiftOutput2.get(gridKey, '')
        expectedGridLeft2 = '420084008280321640'
        self.assertEqual(actualGridLeft2[0], expectedGridLeft2[0], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[1], expectedGridLeft2[1], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[4], expectedGridLeft2[4], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[5], expectedGridLeft2[5], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[8], expectedGridLeft2[8], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[9], expectedGridLeft2[9], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[10], expectedGridLeft2[10], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[12], expectedGridLeft2[12], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[13], expectedGridLeft2[13], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[14], expectedGridLeft2[14], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[15], expectedGridLeft2[15], 'Shift does not shift to the left correctly')
        self.assertEqual(actualGridLeft2[16], expectedGridLeft2[16], 'Shift does not shift to the left correctly')
        
        
        rightShiftOutput1 = shift._shift(userParmsShiftRight1)
        actualGridRight1 = rightShiftOutput1.get(gridKey, '')
        expectedGridRight1 = '0002000000000002'
        self.assertEqual(actualGridRight1[3], expectedGridRight1[3], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight1[15], expectedGridRight1[15], 'Shift does not shift to the right correctly')
        
        rightShiftOutput2 = shift._shift(userParmsShiftRight2)
        actualGridRight2 = rightShiftOutput2.get(gridKey, '')
        expectedGridRight2 = '002400480828016324'
        self.assertEqual(actualGridRight2[2], expectedGridRight2[2], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[3], expectedGridRight2[3], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[6], expectedGridRight2[6], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[7], expectedGridRight2[7], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[9], expectedGridRight2[9], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[10], expectedGridRight2[10], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[11], expectedGridRight2[11], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[13], expectedGridRight2[13], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[14], expectedGridRight2[14], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[15], expectedGridRight2[15], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[16], expectedGridRight2[16], 'Shift does not shift to the right correctly')
        self.assertEqual(actualGridRight2[17], expectedGridRight2[17], 'Shift does not shift to the right correctly')
        
        downShiftOutput = shift._shift(userParmsShiftDown1)
        actualGridDown = downShiftOutput.get(gridKey, '')
        expectedGridDown = '0000000000002020'
        self.assertEqual(actualGridDown[12], expectedGridDown[12], 'Shift does not shift to the down correctly')
        self.assertEqual(actualGridDown[14], expectedGridDown[14], 'Shift does not shift to the down correctly')
        
        upShiftOutput = shift._shift(userParmsShiftUp1)
        actualGridUp = upShiftOutput.get(gridKey, '')
        expectedGridUp = '2020000000000000'
        self.assertEqual(actualGridUp[0], expectedGridUp[0], 'Shift does not shift to the up correctly')
        self.assertEqual(actualGridUp[2], expectedGridUp[2], 'Shift does not shift to the up correctly')
        
#Tests to make sure when blocks collide they add up correctly
    def test_shift_block_collision(self):
        
        grid = '2200000000002200'
        gridKey = 'grid'
        
        hashString = grid + "." + '0'
        myHash = hashlib.sha256()
        myHash.update(hashString.encode())
        integrity = myHash.hexdigest().upper()
        
        userParams = {'op': 'shift', 'grid': grid, 'score': '0', 'direction': 'left', \
                     'integrity': integrity}
        
        actualShiftOutput = shift._shift(userParams)
        actualGrid = actualShiftOutput.get(gridKey, '')
        
        expectedGrid = '4000000000004000'
        
        self. assertEqual(actualGrid[0], expectedGrid[0], 'Blocks do not collide correctly')
        self. assertEqual(actualGrid[12], expectedGrid[12], 'Blocks do not collide correctly')

#Tests to make sure that on block collision that the score and integrity values are updated
    def test_shift_block_collision_score_and_integrity_values(self):
        
        grid = '2200000000002200'
        integrityKey = 'integrity'
        scoreKey = 'score'
        gridKey = 'grid'
        
        hashString = grid + "." + '0'
        myHash = hashlib.sha256()
        myHash.update(hashString.encode())
        initialIntegrity = myHash.hexdigest().upper()
        
        userParams = {'op': 'shift', 'grid': grid, 'score': '0', 'direction': 'left', \
                     'integrity': initialIntegrity}
        
        actualShiftOutput = shift._shift(userParams)
        actualIntegrity = actualShiftOutput.get(integrityKey, '')
        actualScore = str(actualShiftOutput.get(scoreKey, ''))
        actualGrid = actualShiftOutput.get(gridKey, '')
        
        expectedScore = '8'
        
        hashString = actualGrid + "." + actualScore
        myHash = hashlib.sha256()
        myHash.update(hashString.encode())
        expectedIntegrity = myHash.hexdigest().upper()
        
        self. assertEqual(actualScore, expectedScore, 'Collisions do not update the score correctly')
        self. assertEqual(actualIntegrity, expectedIntegrity, 'Grid shifts and/or collisions do not update the integrity correctly')
        
#Test to make sure the status of the grid is updated correctly
    def test_shift_status_check(self):
        
        gridOk = '2000200020002000'
        gridWin = '10241024000000000000000'
        gridLose = '24816168422481616842'
        
        hashStringOk = gridOk + "." + '0'
        myHash = hashlib.sha256()
        myHash.update(hashStringOk.encode())
        okIntegrity = myHash.hexdigest().upper()
        
        hashStringWin = gridWin + "." + '0'
        myHash = hashlib.sha256()
        myHash.update(hashStringWin.encode())
        winIntegrity = myHash.hexdigest().upper()
        
        hashStringLose = gridLose + "." + '0'
        myHash = hashlib.sha256()
        myHash.update(hashStringLose.encode())
        loseIntegrity = myHash.hexdigest().upper()
        
        statusKey = 'status'
        
        userParamsOk = {'op': 'shift', 'grid': gridOk, 'score': '0', 'direction': 'left', \
                     'integrity': okIntegrity}
        userParamsWin = {'op': 'shift', 'grid': gridWin, 'score': '0', 'direction': 'left', \
                     'integrity': winIntegrity}
        userParamsLose = {'op': 'shift', 'grid': gridLose, 'score': '0', 'direction': 'left', \
                     'integrity': loseIntegrity}
        
        actualGridOkOutput = shift._shift(userParamsOk)
        actualGridWinOutput = shift._shift(userParamsWin)
        actualGridLoseOutput = shift._shift(userParamsLose)
        
        actualOkGridStatus = actualGridOkOutput.get(statusKey, '')
        actualWinGridStatus = actualGridWinOutput.get(statusKey, '')
        actualLoseGridStatus = actualGridLoseOutput.get(statusKey, '')
        
        self. assertEqual(actualOkGridStatus, 'ok', 'Status does not update or stay ok when appropriate')
        self. assertEqual(actualWinGridStatus, 'win', 'Status does not update to win when appropriate')
        self. assertEqual(actualLoseGridStatus, 'lose', 'Status does not update to lose when appropriate')
        
