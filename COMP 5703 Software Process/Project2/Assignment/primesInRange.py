def primesInRange(lowBound, highBound):   
    
#Check to make sure inputs are of type int
    if type(lowBound) is not int:  
        return None
    if type(highBound) is not int:
        return None 
    
#Check to make sure neither input is of type None
    if type(lowBound) is None:
        return None 
    if type(highBound) is None:
        return None 
    
#Check to make sure inputs are within the range 1 to 1000    
    if lowBound < 1 or lowBound > 1000:
        return None
    if highBound < 1 or highBound > 1000:
        return None 

#Check to make sure low bound is smaller than high bound        
    if lowBound > highBound:
        return None 
    
    
    result = []

    for num in range(lowBound, highBound + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                result.append(num)
                
    return result   