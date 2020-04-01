import re
from random import randint

class Dice(object):
    count   = 0
    sides   = 0
    offset  = 0
    def __init__(self, count, sides = 0, offset = 0):
        # Note(Keith): If it was just passed as Dice(1), just return the 1
        if not sides and type(count) == int:
            sides = 1

        # Note(Keith): If it was passed as a string Dice("3D6"), parse it out
        elif not sides and type(count) == str:
            parts = re.split('D', count)
            parts2 = re.split('\+|\-', parts[1])
            if not parts[0]:
                parts[0] = 1
            count = int(parts[0])
            if len(parts2) == 2:
                sides = int(parts2[0])
                offset = int(parts2[1])
                if '-' in parts[1]:
                    offset *= -1
            else:
                sides = int(parts[1])
        self.count = count
        self.sides = sides
        self.offset = offset

    def roll(self, verbose=False):
        rolls = []
        total = self.offset
        for r in range(0, self.count):
            ri = randint(1, self.sides)
            rolls.append(ri)
            total = total + ri
        if verbose:
            return total, dict(base_value=self.offset, rolls=rolls)
        else:        
            return total


def attr_mod_label(attribute):
    return dict(
        CHA="Cha",
        CON="Con",
        DEX="Dex",
        INT="Int",
        STR="Str",
        WIL="Wil"
    )[attribute]


def attr_mod(value):

    if value <= 1:
        mod = -5
    elif value == 2:
        mod = -4
    elif value == 3:
        mod = -3
    elif value >= 4 and value <= 5:
        mod = -2
    elif value >= 6 and value <= 8:
        mod = -1
    elif value >= 9 and value <= 12:
        mod = 0
    elif value >= 13 and value <= 15:
        mod = 1
    elif value >= 16 and value <= 17:
        mod = 2
    elif value == 18:
        mod = 3
    elif value == 19:
        mod = 4
    elif value >= 20:
        mod = 5

    return mod

