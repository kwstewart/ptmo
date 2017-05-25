from random import randint

class DiceFormat(object):
    number_of_dice  = 1
    number_of_sides = 6
    base_value      = 0
    def __init__(self, dice_string):
        parts = re.split('D', dice_string)
        parts2 = re.split('\+|\-', parts[1])
        self.number_of_dice = int(parts[0])
        if len(parts2) == 2:
            self.number_of_sides = int(parts2[0])
            self.base_value = int(parts2[1])
            if '-' in dice_string:
                self.base_value *= -1
        else:
            self.number_of_sides = int(parts[1])


def roll(dice, verbose = False):
    if type(dice) != DiceFormat:
        raise ValueError
    rolls = []
    total = dice.base_value
    for r in range(0, dice.number_of_dice):
        ri = randint(1,dice.number_of_sides)
        rolls.append(ri)
        total = total + ri
    if verbose:
        return total, dict(base_value=dice.base_value, rolls=rolls)
    else:
        return total

