import random
import hashlib

def _create(userParms):
    
    score = "0"
    
    #grid is 4x4 
    grid = [[0] * 4 for _ in range(4)]
    
    #randomly populate two grid places with '2'
    for pos in random.sample(range(16), 2):
        grid[pos//4][pos%4] = 2
    
    gridString = ''
    #turn grid into string; the grid is a string of strings
    for element in grid:
        for num in element:
            gridString += str(num)
    
    integrityString = gridString + "." + score        
    myHash = hashlib.sha256()
    myHash.update(integrityString.encode())
    integrity = myHash.hexdigest().upper() 
    
    result = {'grid': gridString, 'score': score, 'integrity': integrity, 'status': 'ok'}
    return result
