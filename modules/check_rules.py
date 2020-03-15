# This file is responsible for validating if a action is valid

def how_may_of(dices):
    # Find out how many values there are for a number
    out = {1:dices.count(1), 2:dices.count(2), 3:dices.count(3), 4:dices.count(4), 
           5:dices.count(5), 6:dices.count(6)}
    return out

def check(dices):
    dices = sorted(dices)
    amount_of = how_may_of(dices) # Amount of times a certain number appears

    validation = {"aces": False, "twos": False, "threes": False, "fours": False, "fives": False, 
                  "sixes": False, "toak": False, "foak": False, "fh": False, "smstraight": False, 
                  "lgstraight": False, "kniffel": False,  "chance":  False}

    if amount_of[1]:
        validation["aces"] = amount_of[1]*1
    if amount_of[2]:
        validation["twos"] = amount_of[2]*2
    if amount_of[3]:
        validation["threes"] = amount_of[3]*3
    if amount_of[4]:
        validation["fours"] = amount_of[4]*4
    if amount_of[5]:
        validation["fives"] = amount_of[5]*5
    if amount_of[6]:
        validation["sixes"] = amount_of[6]*6

    # Three of a kind
    for x in amount_of:
        if amount_of[x] >= 3:
            validation["toak"] = x*amount_of[x]

    # Four of a kind
    for x in amount_of:
        if amount_of[x] >= 4:
            validation["foak"] = x*amount_of[x]


    return validation
    import IPython;IPython.embed();import sys;sys.exit()
