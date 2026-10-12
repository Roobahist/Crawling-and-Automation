def bounded(base_price , price):
    upper = 0
    lower = 0
    delta = 0

    base_price = int(base_price)
    price = int(price)

    if base_price > 0 and base_price < 25000000:
        delta = 1000000
    elif base_price > 25000000 and base_price < 50000000:
        delta = 2000000
    elif base_price > 50000000 and base_price < 75000000:
        delta = 3000000
    elif base_price > 75000000 and base_price < 100000000:
        delta = 4000000
    elif base_price >= 100000000 and base_price < 200000000:
        delta = 5000000 
    elif base_price >= 200000000 and base_price < 300000000 :
        delta = 7000000 
    elif base_price >= 300000000 and base_price < 400000000 :
        delta = 10000000 
    elif base_price >= 400000000 and base_price < 500000000 :
        delta = 15000000 
    elif base_price >= 500000000 and base_price < 600000000 :
        delta = 20000000 
    elif base_price >= 600000000 and base_price < 700000000 :
        delta = 25000000 
    elif base_price >= 700000000 and base_price < 800000000 :
        delta = 30000000 
    elif base_price >= 800000000 and base_price < 900000000 :
        delta = 35000000 
    elif base_price >= 900000000 and base_price < 1000000000 :
        delta = 40000000 
    elif base_price >= 1000000000 and base_price < 2000000000 :
        delta = 50000000 
    elif base_price >= 2000000000 and base_price < 3600000000 :
        delta = 100000000 
    elif base_price >= 3600000000 and base_price < 4000000000 :
        delta = 150000000 
    elif base_price >= 4000000000 :
        delta = 200000000 

    upper = price + delta
    lower = price - delta

    return upper , lower

# upper , lower = bounded(150000000 , 149800000)
# print(upper)
# out = 154800000
# print(lower)
# out = 144800000
    