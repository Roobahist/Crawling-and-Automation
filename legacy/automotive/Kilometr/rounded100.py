def rounded(x):
    flag = 0
    x = str(int(x))
    first = x[:-6]
    second = x[-6:]
    lower = str(second[0])+'00000'
    if second[0]=='9':
        flag = 1
        upper = '1000000'
    else:
        upper = str(int(second[0])+1)+'00000'
    upper_res = int(upper)-int(second)
    lower_res = int(second)-int(lower)
    answer = 0
    
    if second == '000000':
        answer = int(x)
    elif lower_res>upper_res:
        if flag==0:
            answer = int(first + upper)
        else:
            answer = int(first[:-1] + str(int(first[-1])+1) + '000000')
    elif lower_res<=upper_res:
        answer = int(first + lower)
    return answer