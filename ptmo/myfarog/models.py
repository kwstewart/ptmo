# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .objects import *

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

class Race(models.Model):
    name    = models.CharField(max_length=16)
    race    = models.CharField(max_length=16)
    gender  = models.CharField(max_length=16, choices=GENDER)
    height  = models.CharField(max_length=16)   # Lets make this a special dice format 57+4D6
    CHA     = models.IntegerField()
    CON     = models.IntegerField()
    DEX     = models.IntegerField()
    INT     = models.IntegerField()
    STR     = models.IntegerField()
    WIL     = models.IntegerField()

    class Meta:
        verbose_name = "Race"
        verbose_name_plural = "Races"


class Species(models.Model):
    name    = models.CharField(max_length=16)
    race    = models.CharField(max_length=16)
    gender  = models.CharField(max_length=16, choices=GENDER)
    height  = models.CharField(max_length=16)   # Lets make this a special dice format 57+4D6
    CHA     = models.IntegerField()
    CON     = models.IntegerField()
    DEX     = models.IntegerField()
    INT     = models.IntegerField()
    STR     = models.IntegerField()
    WIL     = models.IntegerField()

    class Meta:
        verbose_name = "Race"
        verbose_name_plural = "Races"


class Role(models.Model):
    name    = models.CharField(max_length=16)
    height  = models.CharField(max_length=16)   # Lets make this a special dice format 57+4D6
    CHA     = models.IntegerField()
    CON     = models.IntegerField()
    DEX     = models.IntegerField()
    INT     = models.IntegerField()
    STR     = models.IntegerField()
    WIL     = models.IntegerField()

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"


# Create your models here.
class Character(models.Model):
    name    = models.CharField(max_length=16)
    gender  = models.CharField(max_length=16, choices=GENDER)
    race    = models.ForeignKey(Race)
    role    = models.ForeignKey(Role)
    age     = models.IntegerField()
    CHA     = models.IntegerField()
    CON     = models.IntegerField()
    DEX     = models.IntegerField()
    INT     = models.IntegerField()
    STR     = models.IntegerField()
    WIL     = models.IntegerField()

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def attribute_modifier(self, attribute):

        attr = getattr(self, attribute)
        if attr <= 1:
            mod = -5
        elif attr == 2:
            mod = -4
        elif attr == 3:
            mod = -3
        elif attr >= 4 and attr <= 5:
            mod = -2
        elif attr >= 6 and attr <= 8:
            mod = -1
        elif attr >= 9 and attr <= 12:
            mod = 0
        elif attr >= 13 and attr <= 15:
            mod = 1
        elif attr >= 16 and attr <= 17:
            mod = 2
        elif attr == 18:
            mod = 3
        elif attr == 19:
            mod = 4
        elif attr >= 20:
            mod = 5

        race_mod = getattr(self.race,attribute)

        return mod + race_mod