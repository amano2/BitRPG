import random

def randint(a,b):
    return random.randint(a,b)

def dmg(STR,DEF):
    value = random.randint(95,105)
    dmg = ((value*STR) - (DEF*50))/100
    if dmg <= 0:
        dmg = 0
    return int(dmg)
