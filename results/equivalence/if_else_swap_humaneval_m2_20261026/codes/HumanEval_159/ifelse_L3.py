from typing import *
def eat(number, need, remaining):
    if not (need <= remaining):
        return [ number + remaining , 0]
    else:
        return [ number + need , remaining-need ]
