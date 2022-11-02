from show import show
from rounded100 import rounded
from random import random

def change(x):
    rand = 100 + random()-0.5
    changed_price = x*rand/100
    answer = show(rounded(int(changed_price)))
    return answer