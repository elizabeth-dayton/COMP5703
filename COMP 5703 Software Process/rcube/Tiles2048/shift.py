import math
import hashlib
import random

def _shift(userParms):

    #keys to pull values from input parameters    
    gridKey = 'grid'
    integrityKey = 'integrity'
    scoreKey = 'score'
    directionKey = 'direction'
    
    #Values pulled from the input parameters
    gridString = userParms.get(gridKey,'')
    score = userParms.get(scoreKey, '')
    integrity = userParms.get(integrityKey, '')
    direction = (userParms.get(directionKey, '')).lower()
    
    #populates a 4x4 matrix with the values from the input grid string
    
#--------------------------------    
#Checking for invalid grid inputs
#--------------------------------

    #checks if the grid input value is empty
    if gridString == None:
        status = 'error: missing grid'
        return {'status': status}
    
    #checks if the score input value is empty
    if score == None or score == '':
        status = 'error: missing score'
        return {'status': status}
    
    #checks if the direction input value is empty
    if direction == None or direction == '':
        direction = 'down'

    #checks to make sure there are no letters in the grid value    
    if gridString.isdigit() == False:
        status = 'error: invalid grid - contains invalid character'
        return {'status': status}
        
     #checks to make sure there are no letters in the score value and it's not less than zero    
    if score.isdigit() == False or int(score) < 0:
        status = 'error: invalid score - score negative or contains invalid character'
        return {'status': status}
 
    #makes sure the score is of a proper format (multiple of 2)   
    if int(score) % 2 != 0:
        status = 'error: invalid score - not divisible by 2'
        return {'status': status}
    
    #checks to make sure the incoming integrity value is correct
    initialIntegrityString = gridString + "." + score        
    myHash = hashlib.sha256()
    myHash.update(initialIntegrityString.encode())
    expectedIntegrity = myHash.hexdigest().upper()
    
    if expectedIntegrity != integrity:
        status = 'error: bad integrity value'
        return {'status': status}
    
    #checks to make direction value is one of the 4 valid options
    if direction != 'up' and direction != 'down' and direction != 'right' and direction != 'left':
        status = 'error: invalid direction'
        return {'status': status}

#-----------------------------------------------------------------------
#parse the grid to put it into a matrix for further checks before shift!
#-----------------------------------------------------------------------
    grid = parseGridStringInitial(gridString)
 
    #checks if the grid contains valid numbers after the parse that are of a power of 2
    if grid == None:
        status = 'error: missing grid'  
        return {'status': status} 
    
    #checks to make sure the grid is 4x4 and no rows or columns are missing an element
    numOfElements = 0
    for row in grid:
        numOfElements += len(row)
    
    if numOfElements != 16:
        status = 'error: invalid grid - not enough characters'
        return {'status': status}
    
#---------------------------------------
#Now begins the actual shift of the grid
#---------------------------------------

    if direction == 'up':
        return shiftUp(grid, score, gridString, integrity)
        
    elif direction == 'down':
        return shiftDown(grid, score, gridString, integrity)
        
    elif direction == 'right':
        return shiftRight(grid, score, gridString, integrity)
        
    elif direction == 'left':
        return shiftLeft(grid, score, gridString, integrity)

#-----------------------------------------------------
#These are supporting functions for the shift function
#-----------------------------------------------------

#This is used to populate the matrix by checking the values being entered are a power of 2
def checkNumPowerOfTwo(num):

    #zero is a valid value even though it's technically not a power of 2
    if num == '0':
        return True
    
    #even though 1 is technically a power of 2, we don't want to include it (our values start at 2)
    if num == '1':
        return False
    
    x = (math.log10(int(num)) / math.log10(2))
    return (math.ceil(x) == math.floor(x))
    
#this parses through the grid string and puts the values into a matrix
#this parse is done after the grid has been shifted (i.e. 2048 is a valid number)
def parseGridStringAfterShift(gridString):
    
    #start with an empty grid
    grid = []
    row = []
    i = 0
    #parse through each number to see if it is a power of 2
    #if not, we continue concatenating that number until we get a number that is 4 characters long (2048 is largest possible)
    #if that's a valid number, great we continue! if not, we have an invalid grid (contains number that's not a power of 2) 
    #the numbers 256, 1024, and 2048 are special cases because parts of them are a power of 2 and they may not
    #be processed correctly
    #---------------------------------------------------------------------------------------
    #this is a LARGE nested if/else statement mess. I may need to refactor and clean this up
    #---------------------------------------------------------------------------------------  
    while (i <= (len(gridString) - 1)):
        num = gridString[i]
        if checkNumPowerOfTwo(num):
            if(num != '0' and (i + 1) <= (len(gridString) - 1) and checkNumPowerOfTwo((num + gridString[i + 1]))):
                row.append(num + gridString[i + 1])
                i += 2
            elif(num != '0' and (i + 1) <= (len(gridString) - 1) and (i + 2) <= (len(gridString) - 1) \
                     and checkNumPowerOfTwo((num + gridString[i + 1] + gridString[i + 2]))):
                row.append(num + gridString[i + 1] + gridString[i + 2])
                i += 3
            elif(num != '0' and (i + 1) <= (len(gridString) - 1) and (i + 2) <= (len(gridString) - 1) \
                    and (i + 3) <= (len(gridString) - 1) \
                    and checkNumPowerOfTwo((num + gridString[i + 1] + gridString[i + 2] + gridString[i + 3]))):
                row.append(num + gridString[i + 1] + gridString[i + 2] + gridString[i + 3])
                i += 4
            else:
                row.append(num)
                i += 1
            if len(row) == 4:
                grid.append(row)
                row = []
        else:
            if (i + 1) <= (len(gridString) - 1):
                i += 1
                num = num + gridString[i]
            else:
                grid = None
                break
                
            if checkNumPowerOfTwo(num):
                row.append(num)
                i += 1
                if len(row) == 4:
                    grid.append(row)
                    row = []
            else:
                if (i + 1) <= (len(gridString) - 1):
                    i += 1
                    num = num + gridString[i]
                    
                else:
                    grid = None
                    break
                    
                if checkNumPowerOfTwo(num):
                    row.append(num)
                    i += 1
                    if len(row) == 4:
                        grid.append(row)
                        row = []
                        
                else:
                    if (i + 1) <= (len(gridString) - 1):
                        i += 1
                        num = num + gridString[i]
                    
                    else:
                        grid = None
                        break
                        
                    if checkNumPowerOfTwo(num):
                        row.append(num)
                        i += 1
                        if len(row) == 4:
                            grid.append(row)
                            row = []
                            
                    else:
                        grid = None
                        break                
    return grid

def parseGridStringInitial(gridString):
    
    #start with an empty grid
    grid = []
    row = []
    i = 0
    #parse through each number to see if it is a power of 2
    #if not, we continue concatenating that number until we get a number that is 4 characters long (2048 is largest possible)
    #if that's a valid number, great we continue! if not, we have an invalid grid (contains number that's not a power of 2) 
    #the numbers 256, 1024, and 2048 are special cases because parts of them are a power of 2 and they may not
    #be processed correctly
    #---------------------------------------------------------------------------------------
    #this is a LARGE nested if/else statement mess. I may need to refactor and clean this up
    #---------------------------------------------------------------------------------------  
    while (i <= (len(gridString) - 1)):
        num = gridString[i]
        if checkNumPowerOfTwo(num):
            if(num != '0' and (i + 1) <= (len(gridString) - 1) and checkNumPowerOfTwo((num + gridString[i + 1]))):
                row.append(num + gridString[i + 1])
                i += 2
            elif(num != '0' and (i + 1) <= (len(gridString) - 1) and (i + 2) <= (len(gridString) - 1) \
                     and checkNumPowerOfTwo((num + gridString[i + 1] + gridString[i + 2]))):
                row.append(num + gridString[i + 1] + gridString[i + 2])
                i += 3
            elif(num != '0' and (i + 1) <= (len(gridString) - 1) and (i + 2) <= (len(gridString) - 1) \
                    and (i + 3) <= (len(gridString) - 1) \
                    and checkNumPowerOfTwo((num + gridString[i + 1] + gridString[i + 2] + gridString[i + 3]))) \
                    and (num + gridString[i + 1] + gridString[i + 2] + gridString[i + 3]) != '2048':
                row.append(num + gridString[i + 1] + gridString[i + 2] + gridString[i + 3])
                i += 4
            else:
                row.append(num)
                i += 1
            if len(row) == 4:
                grid.append(row)
                row = []
        else:
            if (i + 1) <= (len(gridString) - 1):
                i += 1
                num = num + gridString[i]
            else:
                grid = None
                break
                
            if checkNumPowerOfTwo(num):
                row.append(num)
                i += 1
                if len(row) == 4:
                    grid.append(row)
                    row = []
            else:
                if (i + 1) <= (len(gridString) - 1):
                    i += 1
                    num = num + gridString[i]
                    
                else:
                    grid = None
                    break
                    
                if checkNumPowerOfTwo(num):
                    row.append(num)
                    i += 1
                    if len(row) == 4:
                        grid.append(row)
                        row = []
                        
                else:
                    if (i + 1) <= (len(gridString) - 1):
                        i += 1
                        num = num + gridString[i]
                    
                    else:
                        grid = None
                        break
                        
                    if checkNumPowerOfTwo(num):
                        row.append(num)
                        i += 1
                        if len(row) == 4:
                            grid.append(row)
                            row = []
                            
                    else:
                        grid = None
                        break                
    return grid
 
#this function adds a random 2 or 4 to and empty space in the grid (each with equal chance)          
def insertNewNumber(grid):
    
    values= ['2', '4']
    
    #need to randomize an index number between 0 and 15
    randomColumnIndex = random.randint(0, 3)
    randomRowIndex = random.randint(0, 3)
    
    #we need to input this value in an empty space 
    #we need to first check there is an empty space or we'll be here forever
    
    if emptySpace(grid):
            while grid[randomRowIndex][randomColumnIndex] != '0':
                randomColumnIndex = random.randint(0, 3)
                randomRowIndex = random.randint(0, 3)
            grid[randomRowIndex][randomColumnIndex] = random.choice(values)
        
    else:
        _shift.status = 'lose'

#this function will parse the matrix to determine if there are any empty spaces (with value '0')    
def emptySpace(grid):
    
    for row in grid:
        for num in row:
            if num == '0':
                return True
    return False

#-----------------------------------------
#below are the methods that shift the grid
#-----------------------------------------

#this method shifts the grid left and handles any resulting collisions        
def shiftLeft(grid, score, gridString, integrity):
    
    score = int(score)

    i = 0
    #need to shift all values to the left as well as merge and update score
    for row in grid:
          
    #first we handle collisions
    #order is very important!
        
        if row[i] == row [i + 1] and row[i] != '0' and row [i + 1] != '0':
            
            row[i] = str(int(row[i]) + int(row [i + 1]))
            row[i + 1] = '0'
            score += int(row[i])
            
        elif row[i] == row[i + 2] and row[i] != '0' and row[i + 2] != '0' and row[i + 1] == '0':
                
            row[i] = str(int(row[i]) + int(row [i + 2]))
            row[i + 2] = '0'
            score += int(row[i])
                
        elif row[i] == row[i + 3] and row[i] != '0' and row[i + 3] != '0' and row[i + 1] == '0' and row[i + 2] == '0':
                
            row[i] = str(int(row[i]) + int(row [i + 3]))
            row[i + 3] = '0'
            score += int(row[i])
            
        if row[i + 1] == row[i + 2] and row[i + 1] != '0' and row[i + 2] != '0':
            
            row[i + 1] = str(int(row[i + 1]) + int(row [i + 2]))
            row[i + 2] = '0'
            score += int(row[i + 1])
            
        elif row[i + 1] == row[i + 3] and row[i + 1] != '0' and row[i + 3] != '0' and row[i + 2] == '0':
            row[i + 1] = str(int(row[i + 1]) + int(row [i + 3]))
            row[i + 3] = '0'
            score += int(row[i + 1])
                  
        if row[i + 2] == row[i + 3] and row[i + 2] != '0' and row[i + 3] != '0':
                
            row[i + 2] = str(int(row[i + 2]) + int(row [i + 3]))
            row[i + 3] = '0'
            score += int(row[i + 2])      
              
    #Everything now needs to be shifted over so there's no rogue 0's
    for row in grid:
        if row[i] == '0' and row [i + 1] != '0':
            row [i] = row[i + 1]
            row[i + 1] = '0'
        elif row[i] == '0' and row [i + 2] != '0':
            row[i] = row[i + 2]
            row[i + 2] = '0'
        elif row[i] == '0' and row[i + 3] != '0':
            row[i] = row[i + 3]
            row[i + 3] = '0'
            
        if row[i + 1] == '0' and row [i + 2] != '0':
            row [i + 1] = row[i + 2]
            row[i + 2] = '0'
        elif row[i + 1] == '0' and row [i + 3] != '0':
            row[i + 1] = row[i + 3]
            row[i + 3] = '0'
            
        if row[i + 2] == '0' and row [i + 3] != '0':
            row [i + 2] = row[i + 3]
            row[i + 3] = '0'         
 
    #if one of the slots is 2048, the game is won
    status = ''
    for row in grid:
        for num in row:
            if num == '2048':
                status = 'win'
                result = {'grid': gridString, 'score': score, 'integrity': integrity, 'status': status}
                return result 
                          
    #now we need to insert a new random 2 or 4           
    insertNewNumber(grid)
    
    #now we need to turn the matrix back into a string so we can calculate integrity
    newGridString = ''
    
    for row in grid:
        for num in row:
            newGridString += str(num)
            
    score = str(score)        
    #calculate new integrity value      
    newIntegrityString = newGridString + "." + score        
    myHash = hashlib.sha256()
    myHash.update(newIntegrityString.encode())
    newIntegrity = myHash.hexdigest().upper()
    
    #need to update the status of the game
                
    #there is still and empty space so the game is not over
    if emptySpace(grid):
        status = 'ok'   
            
    if newGridString == gridString:
        status = 'lose'

    #return shifted grid
    result = {'grid': newGridString, 'score': score, 'integrity': newIntegrity, 'status': status}
    return result     

#this method shifts the grid right and handles any resulting collisions
def shiftRight(grid, score, gridString, integrity): 
    
    score = int(score)
    i = 3
    #need to shift all values to the left as well as merge and update score
    for row in grid:
            
    #first we handle collisions
    #order is very important!
            
        if row[i] == row [i - 1] and row[i] != '0' and row [i - 1] != '0':
                
                row[i - 1] = str(int(row[i]) + int(row [i - 1]))
                row[i] = '0'
                score += int(row[i - 1]) 
                
        elif row[i] == row[i - 2] and row[i] != '0' and row[i - 2] != '0' and row[i - 1] == '0':
                
                row[i - 2] = str(int(row[i]) + int(row [i - 2]))
                row[i] = '0'
                score += int(row[i - 2])
                
        elif row[i] == row[i - 3] and row[i] != '0' and row[i - 3] != '0' and row[i - 1] == '0' and row[i - 2] == '0':
                
                row[i - 3] = str(int(row[i]) + int(row [i - 3]))
                row[i] = '0'
                score += int(row[i - 3])
                    
        if row[i - 1] == row[i - 2] and row[i - 1] != '0' and row[i - 2] != '0':
                
                row[i - 2] = str(int(row[i - 1]) + int(row [i - 2]))
                row[i - 1] = '0'
                score += int(row[i - 2]) 
                    
        elif row[i - 1] == row[i - 3] and row[i - 1] != '0' and row[i - 3] != '0' and row[i - 2] == '0':
            
                row[i - 3] = str(int(row[i - 1]) + int(row [i - 3]))
                row[i - 1] = '0'
                score += int(row[i - 3])
                      
        if row[i - 2] == row[i - 3] and row[i - 2] != '0' and row[i - 3] != '0':
                
                row[i - 3] = str(int(row[i - 2]) + int(row [i - 3]))
                row[i - 2] = '0'
                score += int(row[i - 3])    
                    
    #Everything now needs to be shifted over so there's no rogue 0's
    for row in grid:
        
        if row[i] == '0' and row [i - 1] != '0':
            row [i] = row[i - 1]
            row[i - 1] = '0'
        elif row[i] == '0' and row [i - 2] != '0':
            row[i] = row[i - 2]
            row[i - 2] = '0'
        elif row[i] == '0' and row[i - 3] != '0':
            row[i] = row[i - 3]
            row[i - 3] = '0'
            
        if row[i - 1] == '0' and row [i - 2] != '0':
            row [i - 1] = row[i - 2]
            row[i - 2] = '0'
        elif row[i - 1] == '0' and row [i - 3] != '0':
            row[i - 1] = row[i - 3]
            row[i - 3] = '0'
            
        if row[i - 2] == '0' and row [i - 3] != '0':
            row [i - 2] = row[i - 3]
            row[i - 3] = '0'         
        
    #now we need to insert a new random 2 or 4           
    insertNewNumber(grid)
    
    #now we need to turn the matrix back into a string so we can calculate integrity
    newGridString = ''
    
    for row in grid:
        for num in row:
            newGridString += str(num)
            
    score = str(score)        
    #calculate new integrity value      
    newIntegrityString = newGridString + "." + score        
    myHash = hashlib.sha256()
    myHash.update(newIntegrityString.encode())
    newIntegrity = myHash.hexdigest().upper()
    
    #need to update the status of the game
    
    #if one of the slots is 2048, the game is won
    status = ''
    for row in grid:
        for num in row:
            if num == '2048':
                status = 'win'
                result = {'grid': newGridString, 'score': score, 'integrity': integrity, 'status': status}
                return result
                
    #there is still and empty space so the game is not over
    if emptySpace(grid):
        status = 'ok'   
            
    if newGridString == gridString:
        status = 'lose' 
    
    #return shifted grid
    result = {'grid': newGridString, 'score': score, 'integrity': newIntegrity, 'status': status}
    return result   

#this method shifts the grid up and handles any resulting collisions
def shiftUp(grid, score, gridString, integrity): 
    
    #shifting up is the same result if the grid is tilted on it's side so the right side becomes the bottom side
    #and then shifting right and then tilting the grid back
    
    originalGrid = grid
    score = score
    gridString = gridString
    integrity = integrity
    
    tiltedGrid = [[0] * 4 for _ in range(4)]
    
    #tilting the grid manually
    tiltedGrid[0][0] = originalGrid[3][0]; tiltedGrid[0][1] = originalGrid[2][0]; tiltedGrid[0][2] = originalGrid[1][0] 
    tiltedGrid[0][3] = originalGrid[0][0]; tiltedGrid[1][0] = originalGrid[3][1]; tiltedGrid[1][1] = originalGrid[2][1]
    tiltedGrid[1][2] = originalGrid[1][1]; tiltedGrid[1][3] = originalGrid[0][1]; tiltedGrid[2][0] = originalGrid[3][2]
    tiltedGrid[2][1] = originalGrid[2][2]; tiltedGrid[2][2] = originalGrid[1][2]; tiltedGrid[2][3] = originalGrid[0][2]
    tiltedGrid[3][0] = originalGrid[3][3]; tiltedGrid[3][1] = originalGrid[2][3]; tiltedGrid[3][2] = originalGrid[1][3]
    tiltedGrid[3][3] = originalGrid[0][3]
    
    
    #now we use the tilted grid and call shiftRight
    #we're going to pass in the gridString, but we're going to have to recalculate it anyways after we tilt the grid back
    tiltedResult = shiftRight(tiltedGrid, score, gridString, integrity)
    
    gridKey = 'grid'
    scoreKey = 'score'
    statusKey = 'status'
    
    tiltedGridString = tiltedResult.get(gridKey,'')
    finalScore = str(tiltedResult.get(scoreKey, ''))
    status = tiltedResult.get(statusKey, '')
    
    #the score can stay the same, but the gridString, status, and integrity will have to be calculate again
    #after we tilt the grid back
    
    #from here we need to first put the gridString back into a matrix and shift it back
    
    tiltedGrid = parseGridStringAfterShift(tiltedGridString)
    finalGrid = grid = [[0] * 4 for _ in range(4)]
    
    finalGrid[0][0] = tiltedGrid[0][3]; finalGrid[0][1] = tiltedGrid[1][3]; finalGrid[0][2] = tiltedGrid[2][3] 
    finalGrid[0][3] = tiltedGrid[3][3]; finalGrid[1][0] = tiltedGrid[0][2]; finalGrid[1][1] = tiltedGrid[1][2]
    finalGrid[1][2] = tiltedGrid[2][2]; finalGrid[1][3] = tiltedGrid[3][2]; finalGrid[2][0] = tiltedGrid[0][1]
    finalGrid[2][1] = tiltedGrid[1][1]; finalGrid[2][2] = tiltedGrid[2][1]; finalGrid[2][3] = tiltedGrid[3][1]
    finalGrid[3][0] = tiltedGrid[0][0]; finalGrid[3][1] = tiltedGrid[1][0]; finalGrid[3][2] = tiltedGrid[2][0]
    finalGrid[3][3] = tiltedGrid[3][0]
    
    #now we need to convert the matrix into a string and recalculate integrity
    
    finalGridString = ''
    
    for row in grid:
        for num in row:
            finalGridString += str(num)
            
    if finalGridString == gridString:
        status = 'lose'
           
    #calculate new integrity value      
    newIntegrityString = finalGridString + "." + finalScore        
    myHash = hashlib.sha256()
    myHash.update(newIntegrityString.encode())
    finalIntegrity = myHash.hexdigest().upper() 
    
    #finally, we need to return the shifted grid
    #return shifted grid
    result = {'grid': finalGridString, 'score': finalScore, 'integrity': finalIntegrity, 'status': status}
    return result
    

#this method shifts the grid down and handles and resulting collisions
def shiftDown(grid, score, gridString, integrity): 
    
    #shifting down is the same result if the grid is tilted on it's side so the right side becomes the bottom side
    #and then shifting left and then tilting the grid back   
           
    originalGrid = grid
    score = score
    gridString = gridString
    
    tiltedGrid = [[0] * 4 for _ in range(4)]
    
    #tilting the grid manually
    tiltedGrid[0][0] = originalGrid[3][0]; tiltedGrid[0][1] = originalGrid[2][0]; tiltedGrid[0][2] = originalGrid[1][0] 
    tiltedGrid[0][3] = originalGrid[0][0]; tiltedGrid[1][0] = originalGrid[3][1]; tiltedGrid[1][1] = originalGrid[2][1]
    tiltedGrid[1][2] = originalGrid[1][1]; tiltedGrid[1][3] = originalGrid[0][1]; tiltedGrid[2][0] = originalGrid[3][2]
    tiltedGrid[2][1] = originalGrid[2][2]; tiltedGrid[2][2] = originalGrid[1][2]; tiltedGrid[2][3] = originalGrid[0][2]
    tiltedGrid[3][0] = originalGrid[3][3]; tiltedGrid[3][1] = originalGrid[2][3]; tiltedGrid[3][2] = originalGrid[1][3]
    tiltedGrid[3][3] = originalGrid[0][3]
    
    
    #now we use the tilted grid and call shiftLeft
    #we're going to pass in the gridString, but we're going to have to recalculate it anyways after we tilt the grid back
    tiltedResult = shiftLeft(tiltedGrid, score, gridString, integrity)
    
    gridKey = 'grid'
    scoreKey = 'score'
    statusKey = 'status'
    
    tiltedGridString = tiltedResult.get(gridKey,'')
    finalScore = str(tiltedResult.get(scoreKey, ''))
    status = tiltedResult.get(statusKey, '')
    
    #the score can stay the same, but the gridString, status, and integrity will have to be calculate again
    #after we tilt the grid back
    
    #from here we need to first put the gridString back into a matrix and shift it back
    
    tiltedGrid = parseGridStringAfterShift(tiltedGridString)
    finalGrid = grid = [[0] * 4 for _ in range(4)]
    
    finalGrid[0][0] = tiltedGrid[0][3]; finalGrid[0][1] = tiltedGrid[1][3]; finalGrid[0][2] = tiltedGrid[2][3] 
    finalGrid[0][3] = tiltedGrid[3][3]; finalGrid[1][0] = tiltedGrid[0][2]; finalGrid[1][1] = tiltedGrid[1][2]
    finalGrid[1][2] = tiltedGrid[2][2]; finalGrid[1][3] = tiltedGrid[3][2]; finalGrid[2][0] = tiltedGrid[0][1]
    finalGrid[2][1] = tiltedGrid[1][1]; finalGrid[2][2] = tiltedGrid[2][1]; finalGrid[2][3] = tiltedGrid[3][1]
    finalGrid[3][0] = tiltedGrid[0][0]; finalGrid[3][1] = tiltedGrid[1][0]; finalGrid[3][2] = tiltedGrid[2][0]
    finalGrid[3][3] = tiltedGrid[3][0]
    
    #now we need to convert the matrix into a string and recalculate integrity
    
    finalGridString = ''
    
    for row in grid:
        for num in row:
            finalGridString += str(num)
            
    if finalGridString == gridString:
        status = 'lose'
            
    #calculate new integrity value      
    newIntegrityString = finalGridString + "." + finalScore        
    myHash = hashlib.sha256()
    myHash.update(newIntegrityString.encode())
    finalIntegrity = myHash.hexdigest().upper() 
    
    #finally, we need to return the shifted grid
    #return shifted grid
    result = {'grid': finalGridString, 'score': finalScore, 'integrity': finalIntegrity, 'status': status}
    return result