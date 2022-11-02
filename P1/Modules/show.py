def show(x):                  
    x = str(x)                
    lis = []                  
    for i in range(len(x)):   
        lis.append(x[i])      
    time = len(x)//3          
    z = 0                     
    for i in range(1,time+1): 
        lis.insert(-3*i-z,',')
        z += 1                
    answer = ''               
    for i in range(len(lis)): 
        answer += str(lis[i]) 
    if answer[0] == ',':      
        answer = answer[1:]   
    return answer