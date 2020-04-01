# -*- coding: utf-8 -*-
import django_rq
import math

from django.conf import settings
from django.db import models

from source_framework.core import BaseSourceModel

from myfarog.constants.model import *
from myfarog import spells as myfarog_spells


"""
ITEM STUFF

"""

class ItemMaterial(models.Model):
    name    = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item Material"
        verbose_name_plural = "Item Material"


class ItemPrerequisites(models.Model):
    type    = models.CharField(max_length=100, choices=ITEM_PREREQ_TYPES)
    value   = models.CharField(max_length=100)

    def __str__(self):
        return "{}: {}".format(self.type, self.value)

    class Meta:
        verbose_name = "Item Prerequisites"
        verbose_name_plural = "Item Prerequisites"


class ItemBonusType(models.Model):
    name    = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item Bonus Type"
        verbose_name_plural = "Item Bonus Types"


class ItemBonus(models.Model):
    type    = models.ForeignKey(ItemBonusType, on_delete=models.DO_NOTHING)
    value   = models.CharField(max_length=100)

    def __str__(self):
        return "{}: {}".format(self.type, self.value)

    class Meta:
        verbose_name = "Item Bonus"
        verbose_name_plural = "Item Bonuses"


class Item(models.Model):
    name            = models.CharField(max_length=100)
    type            = models.CharField(max_length=50, choices=ITEM_TYPES)
    description     = models.CharField(max_length=1000, blank=True, null=True)
    weight          = models.IntegerField()
    unique          = models.BooleanField(default=False)
    material        = models.ForeignKey(ItemMaterial, on_delete=models.DO_NOTHING, null=True)
    # TODO(Keith): Make this a custom field type
    # Note(Keith): passing (height, width, length) as "0.0x0.0x0.0" in inches
    dimensions      = models.CharField(max_length=100, blank=True, null=True)
    prerequisites   = models.ManyToManyField(
        ItemPrerequisites,
        blank=True,
        related_name="items",
        related_query_name="items",
    )
    bonuses         = models.ManyToManyField(
        ItemBonus,
        blank=True,
        related_name="items",
        related_query_name="items",
    )

    def get_bonuses(self):
        return ", ".join(["{} +{}".format(bonus.type, bonus.value) for bonus in self.bonuses.all()])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Container(Item):

    # TODO(Keith)       : Not sure if we will need this
    #container_type     = models.CharField(max_length=100, choices=CONTAINER_TYPES)

    class Meta:
        verbose_name = "Container"
        verbose_name_plural = "Containers"


class Compartment(models.Model):

    container   = models.ForeignKey(Container, on_delete=models.DO_NOTHING, related_name="compartments")    
    name        = models.CharField(max_length=100)
    type        = models.CharField(max_length=100, choices=COMPARTMENT_TYPES)
    hidden      = models.BooleanField(default=False)
    lockable    = models.BooleanField(default=False)
    is_locked   = models.BooleanField(default=False)

    class Meta:
        verbose_name        = "Compartment"
        verbose_name_plural = "compartments"

    def __str__(self):
        return "{} {}".format(self.container, self.name)


class Shirt(Container):

    class Meta:
        verbose_name = "Shirt"
        verbose_name_plural = "Shirts"


class Jacket(Container):

    class Meta:
        verbose_name = "Jacket"
        verbose_name_plural = "Jackets"


class Belt(Container):

    class Meta:
        verbose_name = "Belt"
        verbose_name_plural = "Belts"


class Pants(Container):

    class Meta:
        verbose_name = "Pants"
        verbose_name_plural = "Pants"


class Weapon(Item):
    damage          = models.CharField(max_length=50, default=0) # Dice format
    weapon_type     = models.CharField(max_length=50, choices=WEAPON_CLASSES)
    cut             = models.IntegerField(default=0)
    shock           = models.IntegerField(default=0)
    range           = models.IntegerField(default=0)
    OV_mod          = models.IntegerField(default=0)
    DV_mod          = models.IntegerField(default=0)
    AP              = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Weapon"
        verbose_name_plural = "Weapons"


class Armor(Item):
    AV              = models.IntegerField(default=0)
    MS_mod          = models.IntegerField(default=0)
    stealth_mod     = models.IntegerField(default=0)
    swimming_mod    = models.IntegerField(default=0)
    damage          = models.CharField(max_length=50, default=0) # Dice format
    

    class Meta:
        verbose_name = "Armor"
        verbose_name_plural = "Armor"


class Helmet(Item):
    AV              = models.IntegerField(default=0)
    perception_mod  = models.IntegerField(default=0)
    missile_mod     = models.IntegerField(default=0)
    shading_mod     = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Helmet"
        verbose_name_plural = "Helmets"


class Shield(Item):

    ME              = models.IntegerField(default=0)
    MI              = models.IntegerField(default=0)
    MS_mod          = models.IntegerField(default=0)
    damage          = models.CharField(max_length=50, default=0) # Dice format
    cut             = models.IntegerField(default=0)
    shock           = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Shield"
        verbose_name_plural = "Shields"


class Glove(Item):

    class Meta:
        verbose_name = "Glove"
        verbose_name_plural = "Gloves"


class Footwear(Item):

    class Meta:
        verbose_name = "Footwear"
        verbose_name_plural = "Footwear"


class Necklace(Item):

    class Meta:
        verbose_name = "Necklace"
        verbose_name_plural = "Necklaces"


class Earring(Item):

    class Meta:
        verbose_name = "Earring"
        verbose_name_plural = "Earrings"


class Ring(Item):

    class Meta:
        verbose_name = "Ring"
        verbose_name_plural = "Rings"


class Trinket(Item):

    class Meta:
        verbose_name = "Trinket"
        verbose_name_plural = "Trinkets"



""" 
NON ITEM STUFF
"""

class Species(models.Model):
    name            = models.CharField(max_length=100)
    gender_ratio    = models.IntegerField( 
                        help_text   = "The value used here will be the cutoff value for a 1-100 scale, where the lower portion is Female, and the higher Male",
                        default     = 50
    )
    age             = models.CharField(max_length=100, help_text="Dice Format")
    maximum_age     = models.IntegerField(default=5, help_text="This number will be multipled by the Character's CON")

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"



class SpeciesGenderMod(models.Model):
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name='gender_mods')
    gender  = models.CharField(max_length=16, choices=GENDER)
    height  = models.CharField(max_length=16)   # Lets make this a special dice format 57+4D6
    CHA     = models.IntegerField()
    CON     = models.IntegerField()
    DEX     = models.IntegerField()
    INT     = models.IntegerField()
    STR     = models.IntegerField()
    WIL     = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.species, self.gender)

    class Meta:
        verbose_name = "Species Gender Mod"
        verbose_name_plural = "Species Gender Mods"


class Role(models.Model):
    name            = models.CharField(max_length=100)
    #prerequisites   = JSONField(default=dict)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"


class Skill(models.Model):
    name            = models.CharField(max_length=100)
    type            = models.CharField(max_length=4, choices=SKILL_TYPES)
    attribute       = models.CharField(max_length=16, choices=ATTRIBUTES)
    untrained       = models.IntegerField()
    description     = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class RoleSkill(models.Model):
    role            = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    skill           = models.ForeignKey(Skill, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return "{} {}".format(self.role, self.skill)

    class Meta:
        verbose_name = "Role Skill"
        verbose_name_plural = "Role Skills"


class Talent(models.Model):
    name            = models.CharField(max_length=100)
    prerequisite    = models.ForeignKey("Talent", on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Talent"
        verbose_name_plural = "Talents"


class TalentSkill(models.Model):
    talent  = models.ForeignKey(Talent, on_delete=models.DO_NOTHING, related_name="skills")
    skill   = models.ForeignKey(Skill, on_delete=models.DO_NOTHING)
    mod     = models.IntegerField()

    def __str__(self):
        return "{} ({} +{})".format(self.talent, self.skill, self.mod)

    class Meta:
        verbose_name = "Talent Skill"
        verbose_name_plural = "Talent Skills"


class TalentExtra(models.Model):
    talent  = models.ForeignKey(Talent, on_delete=models.DO_NOTHING)
    extra   = models.CharField(max_length=50, choices=TALENT_EXTRAS)
    mod     = models.IntegerField()

    def __str__(self):
        return "{} ({} +{})".format(self.talent, self.extra, self.mod)

    class Meta:
        verbose_name = "Talent Extra"
        verbose_name_plural = "Talent Extras"    


class Culture(BaseSourceModel):
    name            = models.CharField(max_length=100)

    def __str__(self): 
        return self.name

    class Meta:
        verbose_name        = "Culture"
        verbose_name_plural = "Cultures"


class CultureGenderSkill(BaseSourceModel):
    culture = models.ForeignKey(Culture, on_delete=models.DO_NOTHING, related_name="cultures", null=True, blank=True)
    gender  = models.CharField(max_length=16, choices=GENDER)
    skill   = models.ForeignKey(Skill, on_delete=models.DO_NOTHING, related_name="skills")

    def __str__(self): 
        return "{} {}".format(self.culture, self.skill)

    class Meta:
        verbose_name        = "Culture Skill"
        verbose_name_plural = "Culture Skills"




class SpellElement(models.Model):
    name    = models.CharField(max_length=100)
    symbol  = models.CharField(max_length=10)

    def __str__(self):
        return "{} {}".format(self.name, self.symbol)

    class Meta:
        verbose_name = "Spell Element"
        verbose_name_plural = "Spell Elements"


class Spell(models.Model):
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    power_level = models.IntegerField()
    elements    = models.ManyToManyField(
        SpellElement,
        blank=True,
        related_name="spell",
        related_query_name="spell",
    )

    def __str__(self):
        return self.name

    def get_elements(self):
        return ", ".join([element.symbol for element in self.elements.all()])


    class Meta:
        verbose_name = "Spell"
        verbose_name_plural = "Spells"

