import unittest
import Tiles2048.create as create
from random import random

class CreateTest(unittest.TestCase):

#Tests the randomness of the placement of the two 2's in 50 trails
    def test_create_randomness_50Trials(self):
        userParms = {'op': 'create', 'size': '4'}
        numOfTrials = 50
        i = 0
        trials = []
        
        #run the create function 50 times and put the results in trials
        while i < numOfTrials:
            actualResult = create._create(userParms)
            trials.append(actualResult)
            i += 1  
             
        gridString = ''
        indices = []
        #for every grid, we take the index of where the two's were placed and save them
        for grid in trials:
            gridString = grid.get('grid')
            indices += [i for i, x in enumerate(gridString) if x == "2"]
        indices = ''.join(str(e) for e in indices) 
        
        totalElementIndex = 0
         
        #we add up all the index positions for average purposes            
        for element in indices:
            totalElementIndex += int(element)
         
        #calculate the average index as there are 16 total elements in the grid        
        averageIndex = totalElementIndex/50
        
        #a perfect average would be 7.5, so this is a range that the average should fall in
        self.assertAlmostEqual(averageIndex, 7.5, delta = 1)