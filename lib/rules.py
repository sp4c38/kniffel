# This file is responsible for validating if a action is valid

def how_may_of(dices):
    # Find out how many values there are for a number
    out = {1:dices.count(1), 2:dices.count(2), 3:dices.count(3), 4:dices.count(4),
           5:dices.count(5), 6:dices.count(6)}
    return out

def check(dices, settings):
    dices = sorted(dices)
    amount_of = how_may_of(dices) # Amount of times a certain number appears

    validation = {"aces": False, "twos": False, "threes": False, "fours": False, "fives": False,
                  "sixes": False, "toak": False, "foak": False, "fh": False, "smstraight": False,
                  "lgstraight": False, "kniffel": False,  "chance":  False}

    if amount_of[1] > 0:
        validation["aces"] = amount_of[1]*1
    else:
        validation["aces"] = 0
    if amount_of[2] > 0:
        validation["twos"] = amount_of[2]*2
    else:
        validation["twos"] = 0
    if amount_of[3] > 0:
        validation["threes"] = amount_of[3]*3
    else:
        validation["threes"] = 0
    if amount_of[4] > 0:
        validation["fours"] = amount_of[4]*4
    else:
        validation["fours"] = 0
    if amount_of[5] > 0:
        validation["fives"] = amount_of[5]*5
    else:
        validation["fives"] = 0
    if amount_of[6] > 0:
        validation["sixes"] = amount_of[6]*6
    else:
        validation["sixes"] = 0

    # Three of a kind
    for num in amount_of:
        if amount_of[num] >= 3:
            validation["toak"] = num * amount_of[num]

    # Four of a kind
    for num in amount_of:
        if amount_of[num] >= 4:
            validation["foak"] = num*amount_of[num]

    # Full house
    full_house_waypoints = {"three_of":False, "two_of":False}
    for x in amount_of:
        if amount_of[x] == 3:
            full_house_waypoints["three_of"] = True
        elif amount_of[x] == 2:
            full_house_waypoints["two_of"] = True

    if full_house_waypoints["three_of"] and full_house_waypoints["two_of"]:
        validation["fh"] = settings["point_distribution"]["fh"]

    # Small Straight
    if amount_of[1] and amount_of[2] and amount_of[3] and amount_of[4]:
        validation["smstraight"] = settings["point_distribution"]["smstraight"]
    elif amount_of[2] and amount_of[3] and amount_of[4] and amount_of[5]:
        validation["smstraight"] = settings["point_distribution"]["smstraight"]
    elif amount_of[3] and amount_of[4] and amount_of[5] and amount_of[6]:
        validation["smstraight"] = settings["point_distribution"]["smstraight"]

    # Long Straight
    if amount_of[1] and amount_of[2] and amount_of[3] and amount_of[4] and amount_of[5]:
        validation["lgstraight"] = settings["point_distribution"]["lgstraight"]
    elif amount_of[2] and amount_of[3] and amount_of[4] and amount_of[5] and amount_of[6]:
        validation["lgstraight"] = settings["point_distribution"]["lgstraight"]

    # Kniffel
    for number in amount_of:
        if amount_of[number] == 5:
            validation["kniffel"] = settings["point_distribution"]["kniffel"]
            break

    # Chance
    chance_points = 0
    for num in amount_of:
        chance_points += num * amount_of[num]
        
    if chance_points:
        validation["chance"] = chance_points

    return validation
