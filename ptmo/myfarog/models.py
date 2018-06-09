# -*- coding: utf-8 -*-
import re
import math

from django.contrib.auth.models import User
from django.db import models

from source_framework.core.models import SourceUser
from source_framework.core.utils.model import (
    ValidatorMixin, PaginationMixin, SourceModelMixin

)

from myfarog.constants.model import *
from myfarog.utils.model import (
    attr_mod,
    attr_mod_label,
    Dice
)
from myfarog import spells as myfarog_spells


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


class RolePrerequisites(models.Model):
    type    = models.CharField(max_length=100, choices=ROLE_PREREQ_TYPES)
    value   = models.CharField(max_length=100)

    def __str__(self):
        return "{}: {}".format(self.type, self.value)

    class Meta:
        verbose_name = "Role Prerequisites"
        verbose_name_plural = "Role Prerequisites"


class Species(models.Model):
    name    = models.CharField(max_length=100)
    gender  = models.CharField(max_length=16, choices=GENDER)
    height  = models.CharField(max_length=16)   # Lets make this a special dice format 57+4D6
    CHA     = models.IntegerField()
    CON     = models.IntegerField()
    DEX     = models.IntegerField()
    INT     = models.IntegerField()
    STR     = models.IntegerField()
    WIL     = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.name, self.gender)

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"


class Role(models.Model):
    name            = models.CharField(max_length=100)
    prerequisites   = models.ManyToManyField(
        RolePrerequisites,
        blank=True,
        related_name="roles",
        related_query_name="role",
    )

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
    talent  = models.ForeignKey(Talent, on_delete=models.DO_NOTHING)
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


class CharacterQuerySet(models.QuerySet, PaginationMixin):
    pass

class CharacterManager(models.Manager):
    use_in_migrations = True

    def get_queryset(self):
        return CharacterQuerySet(self.model, using=self._db)    

class Character(models.Model):
    objects                 = CharacterManager()

    user                    = models.ForeignKey(SourceUser, on_delete=models.DO_NOTHING)
    exp                     = models.IntegerField(default=0)
    level                   = models.IntegerField(default=0)
    name                    = models.CharField(max_length=16)
    gender                  = models.CharField(max_length=16, choices=GENDER)
    species                 = models.ForeignKey(Species, on_delete=models.DO_NOTHING)
    role                    = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    age                     = models.IntegerField(default=0)
    handedness              = models.CharField(max_length=10, choices=HANDEDNESS_CHOICES, default='right')

    CHA                     = models.IntegerField(default=0)
    CON                     = models.IntegerField(default=0)
    DEX                     = models.IntegerField(default=0)
    INT                     = models.IntegerField(default=0)
    STR                     = models.IntegerField(default=0)
    WIL                     = models.IntegerField(default=0)
    _cha                    = models.IntegerField(default=0)
    _con                    = models.IntegerField(default=0)
    _dex                    = models.IntegerField(default=0)
    _int                    = models.IntegerField(default=0)
    _str                    = models.IntegerField(default=0)
    _wil                    = models.IntegerField(default=0)

    HP                      = models.IntegerField(default=0)
    SP                      = models.IntegerField(default=0)
    MHP                     = models.IntegerField(default=0)
    max_HP                  = models.IntegerField(default=0)
    max_SP                  = models.IntegerField(default=0)
    max_MHP                 = models.IntegerField(default=0)    
    height                  = models.IntegerField(default=0)
    weight                  = models.IntegerField(default=0)
    size                    = models.IntegerField(default=0)

    OV_melee                = models.IntegerField(default=0)
    OV_missile              = models.IntegerField(default=0)
    DV_melee                = models.IntegerField(default=0)
    DV_missile              = models.IntegerField(default=0)

    shirt_equipment         = models.ForeignKey(Shirt, on_delete=models.DO_NOTHING, null=True, blank=True)
    pants_equipment         = models.ForeignKey(Pants, on_delete=models.DO_NOTHING, null=True, blank=True)
    # TODO(Keith)           : Jacket and Belt
    left_hand_weapon        = models.ForeignKey(Weapon, on_delete=models.DO_NOTHING, null=False, blank=False, related_name="left_hand", default=1)
    left_hand_shield        = models.ForeignKey(Shield, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="left_hand")
    right_hand_weapon       = models.ForeignKey(Weapon, on_delete=models.DO_NOTHING, null=False, blank=False, related_name="right_hand", default=1)
    right_hand_shield       = models.ForeignKey(Shield, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="right_hand")
    armor_equipment         = models.ForeignKey(Armor, on_delete=models.DO_NOTHING, null=True, blank=True)
    helment_equipment       = models.ForeignKey(Helmet, on_delete=models.DO_NOTHING, null=True, blank=True)
    left_glove_equipment    = models.ForeignKey(Glove, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="left_glove")
    right_glove_equipment   = models.ForeignKey(Glove, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="right_glove")
    footwear_equipment      = models.ForeignKey(Footwear, on_delete=models.DO_NOTHING, null=True, blank=True)
    necklace_equipment      = models.ForeignKey(Necklace, on_delete=models.DO_NOTHING, null=True, blank=True)
    left_earring_equipment  = models.ForeignKey(Earring, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="left_ear")
    right_earring_equipment = models.ForeignKey(Earring, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="right_ear")
    ring_equipment          = models.ForeignKey(Ring, on_delete=models.DO_NOTHING, null=True, blank=True)
    trinket_equipment       = models.ForeignKey(Trinket, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    encumbrance_status      = models.CharField(max_length=16, choices=ENCUMBERANCE_STATUSES, default='Light')
    encumbrance_mod         = models.IntegerField(default=0)
    health_status           = models.CharField(max_length=16, choices=HEALTH_STATUSES, default='Normal')
    health_mod              = models.IntegerField(default=0)
    mental_health_status    = models.CharField(max_length=16, choices=MENTAL_HEALTH_STATUSES, default='Normal')
    mental_health_mod       = models.IntegerField(default=0)
    stamina_status          = models.CharField(max_length=16, choices=STAMINA_STATUSES, default='Normal')
    stamina_mod             = models.IntegerField(default=0)
    stun_status             = models.CharField(max_length=16, choices=STUN_STATUSES, default='Normal')
    stun_rounds             = models.IntegerField(default=0)
    morale_status           = models.CharField(max_length=16, choices=MORALE_STATUSES, default='Normal')
    morale_rounds           = models.IntegerField(default=0)
    morale_check_bonus      = models.IntegerField(default=0)
    pyschotic_count         = models.IntegerField(default=0)
    trauma_count            = models.IntegerField(default=0)

    fright_mod              = models.IntegerField(default=0)
    initiative_check_bonus  = models.IntegerField(default=0)

    bonuses                 = {}
    skills                  = {}
    talents                 = []
    spells                  = models.ManyToManyField(
        Spell,
        blank=True,
        related_name="spells",
        related_query_name="spells",
    )

    logs                    = dict()

    """
    Method called when a Character is initialized
    Sets all derived values
    """
    def init_stats(self):
        if not self.id:
            return False

        self.set_talents()
        self.set_bonuses()
        self.set_cha()
        self.set_con()
        self.set_dex()
        self.set_int()
        self.set_str()
        self.set_wil()
        self.set_level()
        self.set_size()
        self.set_stamina_mod()

        self.set_max_HP()
        self.set_max_SP()
        self.set_max_MHP()
        self.set_fright_mod()
        self.set_encumbrance_condition()
        self.set_health_condition()
        self.set_mental_health_condition()
        self.set_morale_condition()
        self.set_stamina_condition()
        self.set_initiative_check_bonus()
        self.set_skill_mods()
        self.set_combat_values()

        self.save()

    """
    Method called when a Character is updated
    Will update derived values, optionally only of a certain type
    """
    def update_stats(self, type = None):
        pass
        Character.objects(id=self.id).update(**update_dict)

    """
    ********************************************
    **** Methods for setting derived values ****
    ********************************************
    """
    def set_bonuses(self):
        bonuses = {}
        for slot in EQUIPMENT_SLOTS:
            equipment = getattr(self, slot, None)
            if equipment:
                if equipment.bonuses:
                    for bonus in equipment.bonuses.all():
                        bonus_type = bonus.type.name
                        if bonus_type not in bonuses:
                            bonuses[bonus_type] = 0
                        if bonus.type not in self.logs:
                            self.logs[bonus_type] = []
                        # TODO(Keith): make sure we are dealing with the correct data type
                        bonuses[bonus_type] += int(bonus.value)
                        self.logs[bonus_type].append(dict(label=equipment.name, value=bonus.value))

        self.bonuses = bonuses
        
    def set_cha(self):
        mod = attr_mod(self.CHA)
        if '_cha' in self.bonuses:
            mod += self.bonuses['_cha']
        self._cha = mod

    def set_con(self):
        mod = attr_mod(self.CON)
        if '_con' in self.bonuses:
            mod += self.bonuses['_con']
        self._con = mod

    def set_dex(self):
        mod = attr_mod(self.DEX)
        if '_dex' in self.bonuses:
            mod += self.bonuses['_dex']
        self._dex = mod

    def set_int(self):
        mod = attr_mod(self.INT)
        if '_int' in self.bonuses:
            mod += self.bonuses['_int']
        self._int = mod

    def set_str(self):
        mod = attr_mod(self.STR)
        if '_str' in self.bonuses:
            mod += self.bonuses['_str']
        self._str = mod

    def set_wil(self):
        mod = attr_mod(self.WIL)
        if '_wil' in self.bonuses:
            mod += self.bonuses['_wil']
        self._wil = mod

    def set_level(self):
        self.level = int(math.sqrt(self.exp / 250))

    def set_size(self):
        if self.weight   >= 1    and self.weight <= 5    : size = -10
        elif self.weight >= 6    and self.weight <= 10   : size = -9
        elif self.weight >= 11   and self.weight <= 20   : size = -8
        elif self.weight >= 21   and self.weight <= 30   : size = -7
        elif self.weight >= 31   and self.weight <= 45   : size = -6
        elif self.weight >= 46   and self.weight <= 60   : size = -5
        elif self.weight >= 61   and self.weight <= 75   : size = -4
        elif self.weight >= 76   and self.weight <= 95   : size = -3
        elif self.weight >= 96   and self.weight <= 115  : size = -2
        elif self.weight >= 116  and self.weight <= 135  : size = -1
        elif self.weight >= 136  and self.weight <= 165  : size = 0
        elif self.weight >= 166  and self.weight <= 205  : size = 1
        elif self.weight >= 206  and self.weight <= 255  : size = 2
        elif self.weight >= 256  and self.weight <= 320  : size = 3
        elif self.weight >= 321  and self.weight <= 400  : size = 4
        elif self.weight >= 401  and self.weight <= 500  : size = 5
        elif self.weight >= 501  and self.weight <= 650  : size = 6
        elif self.weight >= 651  and self.weight <= 850  : size = 7
        elif self.weight >= 851  and self.weight <= 1100 : size = 8
        elif self.weight >= 1101 and self.weight <= 1400 : size = 9
        elif self.weight >= 1401                         : size = 10

        self.size = size

    def set_max_HP(self):
        if self.role.name in ['Warrior', 'Beserk']:
            level_mod = self.level * 2
        else:
            level_mod = self.level

        bonus = 0
        if 'max_HP' in self.bonuses:
            bonus = self.bonuses['max_HP']
        self.max_HP = self.CON + self._str + self.size + level_mod + bonus
    
    def set_max_SP(self):
        mod = self.skills['Stamina'] * 3
        if 'max_SP' in self.bonuses:
            mod += self.bonuses['max_SP']
        self.max_SP = mod

    def set_max_MHP(self):
        mod = self.WIL * 3
        if 'max_MHP' in self.bonuses:
            mod += self.bonuses['max_MHP']
        self.max_MHP = mod

    def set_talents(self):
        self.talents = CharacterTalent.objects.filter(character=self).order_by('talent__name')

    def set_encumbrance_condition(self):
        # TODO(Keith): Fix this after getting inventory up
        self.encumbrance_status = "Light"
        self.encumbrance_mod = 0
        
    def set_health_condition(self):
        if self.HP >= self.max_HP / 2:
            status = "Normal"
            mod = 0
        elif self.HP > self.max_HP / 4:
            status = "Seriously Injured"
            mod = -2
        elif self.HP > 0:
            status = "Severely Injured"
            mod = -4
        else:
            status = "Fatally Injured"
            mod = -99

        self.health_status = status
        self.health_mod = mod

    def set_mental_health_condition(self):
        if self.MHP >= 3 * self.max_MHP / 4:
            status = "Normal"
            mod = 0
        elif self.MHP >= self.max_MHP / 2:
            status = "Stressed"
            mod = -1
        elif self.MHP > self.max_MHP / 4:
            status = "Agitated"
            mod = -2
        elif self.MHP > 0:
            status = "Deranged"
            mod = -3
        else:
            status = "Pyschotic"
            mod = -99

        self.mental_health_status = status
        self.mental_health_mod = mod
    
    def set_morale_condition(self):
        if self.morale_status == "Normal":
            mod = 0
        elif self.morale_status == "Nervous":
            mod = -1
        elif self.morale_status == "Afraid":
            mod = -2
        elif self.morale_status == "Fearful":
            mod = -3
        elif self.morale_status == "Terrified":
            mod = -4
        elif self.morale_status == "Panic":
            mod = +1

        self.morale_mod = mod

    def set_stamina_condition(self):
        if self.SP > self.max_SP / 3:
            mod = 0
            status = "Normal"
        elif self.SP > 2 * self.max_SP / 3:
            mod = -1
            status = "Tired"
        elif self.SP > 0:
            mod = -4
            status = "Exhausted"
        else:
            mod = -99
            status = "Unconscious"
        
        self.stamina_status = status
        self. stamina_mod = mod
        
    def set_initiative_check_bonus(self):
        character_talents = self.talents.values_list("talent", flat=True)
        ct_mod = sum(TalentExtra.objects.filter(extra='Initiative', talent__in=character_talents).values_list("mod",flat=True))
        # TODO(Keith): Add in missile weapon bonus
        self.initiative_check_bonus = self._dex + ct_mod

    def set_morale_check_bonus(self):
        character_talents = self.talents.values_list("talent", flat=True)
        ct_mod = sum(TalentExtra.objects.filter(extra='Morale', talent__in=character_talents).values_list("mod",flat=True))
        # TODO(Keith): Add in loggin
        # TODO(Keith): Add in class bonuses and spell effects
        self.morale_check_bonus = self._wil + ct_mod

    def set_fright_mod(self):
        if self.role.name == "Sorcerer":
            mod = -4
        elif self.role.name == "Bard":
            mod = -2
        elif self.role.name == "Beserk":
            mod = -1
        else:
            mod = 0
        
        self.fright_mod = mod

    def set_stamina_mod(self):
        logs = []
        self.logs['Stamina'] = []

        mod = 12 + self._con
        logs.append(dict(label="base", value=12))
        logs.append(dict(label="Con", value=self._con))

        stamina_talents = TalentSkill.objects.filter(skill__name='Stamina').values_list('talent',flat=True)
        character_talents = CharacterTalent.objects.filter(character=self, talent__in=stamina_talents)
        
        for ct in character_talents:
            talent_skills = TalentSkill.objects.filter(talent=ct.talent)
            for ts in talent_skills:
                mod += ts.mod
                logs.append(dict(label=ct.talent.name, value=ts.mod))
        self.skills['Stamina'] = mod
        self.logs['Stamina'].append(logs)

    def set_skill_mods(self):
        special_case_skills = ['Dodging', 'Fortitude', 'Perception', 'Tempo']

        # Check if Trained or Role Skill, skip Stamina, we already set that
        all_skills = Skill.objects.exclude(name='Stamina').order_by('name')
        character_skills = CharacterSkill.objects.filter(character=self)
        skill_mods = {}

        for skill in all_skills:
            mod = 0
            logs = []
            self.logs[skill.name] = []

            if skill.name in special_case_skills:
                if skill.name == 'Dodging':
                    mod = 2 + self._dex
                    logs.append(dict(label="Base", value=2))
                    logs.append(dict(label="Dex", value=self._dex))
                elif skill.name == 'Fortitude':
                    mod = self.trauma_count * -1
                    logs.append(dict(label="Traumas", value=self.trauma_count * -1))
                elif skill.name == 'Perception':
                    mod = self._int
                    logs.append(dict(label="Int", value=self._int))

                    logs.append(dict(label="Base", value=12))
                    logs.append(dict(label="Con", value=self._con))
                elif skill.name == 'Tempo':
                    mod = 40 + (5 * self._str)
                    logs.append(dict(label="Base", value=40))
                    logs.append(dict(label="Str * 5", value=(self._str * 5)))

            # TODO(Keith): This makes another query each time; seems like there is a better way
            char_skill = character_skills.filter(skill=skill).first()
            if char_skill:
                if char_skill.role_skill:
                    half_level = math.floor(self.level / 2)
                    if half_level < 15:
                        mod = mod + half_level
                        logs.append(dict(label="Role Skill - Level ÷ 2", value=half_level))
                    else:
                        mod = mod + 15
                        logs.append(dict(label="Role Skill - Max", value=15))
                    
                else:
                    quarter_level = math.floor(self.level / 4)
                    if quarter_level < 15:
                        mod = mod + quarter_level
                        logs.append(dict(label="Trained Skill - Level ÷ 4", value=quarter_level))
                    else:
                        mod = mod + 15
                        logs.append(dict(label="Trained Skill - Max", value=15))
                
                _am = attr_mod(getattr(self, skill.attribute))
                mod += _am
                logs.append(dict(label=attr_mod_label(skill.attribute), value=_am))

            elif skill.name not in special_case_skills:
                mod = skill.untrained
                logs.append(dict(label="Untrained Skill", value=skill.untrained))
            
            # Add mods from abnormal statuses
            if self.health_mod:
                mod = mod + self.health_mod
                logs.append(dict(label=self.health_status, value=self.health_mod))

            if self.morale_mod:
                mod = mod + self.morale_mod
                logs.append(dict(label=self.morale_status, value=self.morale_mod))

            if self.stamina_mod:
                mod = mod + self.stamina_mod
                logs.append(dict(label=self.stamina_status, value=self.stamina_mod))

            # Movement skills are affected by Encumberance
            if skill.type == 'MS' and self.encumbrance_mod:
                mod = mod + self.encumbrance_mod
                logs.append(dict(label=self.encumbrance_status, value=self.encumbrance_mod))

            # Int based skills are affected by Mental Health Conditions
            if skill.attribute == 'INT' and self.mental_health_mod:
                mod = mod + self.mental_health_mod
                logs.append(dict(label=self.mental_health_status, value=self.mental_health_mod))

            skill_mods[skill.name] = mod
            self.logs[skill.name] = self.logs[skill.name] + logs

        # Check for Talents
        character_talents = CharacterTalent.objects.filter(character=self)
        for ct in character_talents:
            talent_skills = TalentSkill.objects.filter(talent=ct.talent).exclude(skill__name='Stamina')
            for ts in talent_skills:
                skill_name = ts.skill.name
                if skill_name not in skill_mods:
                    oh_shit_wtf_yo()
                skill_mods[skill_name] += ts.mod
                self.logs[ts.skill.name] = self.logs[ts.skill.name] + [dict(label=ct.talent.name, value=ts.mod)]

        self.skills = skill_mods
    
    def set_combat_values(self):
        self.set_OV_melee()
        self.set_OV_missile()
        self.set_DV_melee()
        self.set_DV_missile()

    def set_OV_melee(self):
        self.logs['OV_melee'] = []
        logs = []
        mod = 0
        
        mod += self.skills['Melee']
        logs.append(dict(label="Melee Skill", value=self.skills['Melee']))

        if self.left_hand_weapon and self.right_hand_weapon:
            mod += 1
            logs.append(dict(label="Dual Weapons", value=1))

        if self.left_hand_shield:
            mod += 1
            logs.append(dict(label="Left-hand Shield", value=1))

        if self.right_hand_shield:
            mod += 1
            logs.append(dict(label="Right-hand Shield", value=1))
            
        if self.left_hand_weapon and self.left_hand_weapon.weapon_type == "melee" and self.left_hand_weapon.OV_mod != 0:
            mod += self.left_hand_weapon.OV_mod
            logs.append(dict(label="Left-hand Weapon", value=self.left_hand_weapon.OV_mod))

        if self.right_hand_weapon and self.right_hand_weapon.weapon_type == "melee" and self.right_hand_weapon.OV_mod != 0:
            mod += self.right_hand_weapon.OV_mod
            logs.append(dict(label="Right-hand Weapon", value=self.right_hand_weapon.OV_mod))

        # TODO(Keith): Add unarmed stats
        # TODO(Keith): Combat mods

        self.OV_melee = mod
        self.logs['OV_melee'] += logs

    def set_OV_missile(self):
        self.logs['OV_missile'] = []
        mod = 0
        logs = []

        mod += self.skills['Missile']
        logs.append(dict(label="Missile Skill", value=self.skills['Missile']))
        
        if self.helment_equipment:
            mod += self.helment_equipment.missile_mod
            logs.append(dict(label="Helmet", value=self.helment_equipment.missile_mod))

        # TODO(Keith): Make sure weapon is a missile type
        if self.left_hand_weapon and self.left_hand_weapon.weapon_type == "missile" and self.left_hand_weapon.OV_mod != 0:
            mod += self.left_hand_weapon.OV_mod
            logs.append(dict(label="Left hand Weapon", value=self.left_hand_weapon.OV_mod))
        if self.right_hand_weapon and self.right_hand_weapon.weapon_type == "missile" and self.right_hand_weapon.OV_mod != 0:
            mod += self.right_hand_weapon.OV_mod
            logs.append(dict(label="Right hand Weapon", value=self.right_hand_weapon.OV_mod))

        # TODO(Keith): Combat mods

        self.OV_missile = mod
        self.logs['OV_missile'] += logs

    def set_DV_melee(self):
        self.logs['DV_melee'] = []
        logs = []
        
        mod = 10
        logs.append(dict(label="Base", value=10))

        mod += self.skills['Melee']
        logs.append(dict(label="Melee Skill", value=self.skills['Melee']))

        mod += self.skills['Dodging']
        logs.append(dict(label="Dodging Skill", value=self.skills['Dodging']))

        if self.left_hand_shield:
            mod += self.left_hand_shield.ME
            logs.append(dict(label="Left-hand Shield", value=self.left_hand_shield.ME))

        if self.right_hand_shield:
            mod += self.right_hand_shield.ME
            logs.append(dict(label="Right-hand Shield", value=self.right_hand_shield.ME))

        # TODO(Keith): Combat mods

        self.DV_melee = mod
        self.logs['DV_melee'] += logs

    def set_DV_missile(self):
        self.logs['DV_missile'] = []
        logs = []

        mod = 10
        logs.append(dict(label="Base", value=10))

        mod += self.skills['Dodging']
        logs.append(dict(label="Dodging Skill", value=self.skills['Dodging']))

        if self.left_hand_shield:
            mod += self.left_hand_shield.MI
            logs.append(dict(label="Left-hand Shield", value=self.left_hand_shield.ME))

        if self.right_hand_shield:
            mod += self.right_hand_shield.MI
            logs.append(dict(label="Right-hand Shield", value=self.right_hand_shield.ME))
        
        size_mod = int(self.size / 2)
        if size_mod != 0:
            mod -= size_mod
            logs.append(dict(label="Size / 2", value=-size_mod))

        # TODO(Keith): Combat mods

        self.DV_missile = mod
        self.logs['DV_missile'] += logs


    """
    ***************************************************************
    **** Methods for testing (Skills, Morale, Initiative, etc) ****
    ***************************************************************
    """
    def test_initiative(self, ranged=False):
        # TODO(Keith): Add ranged bonus
        initiative_roll = Dice("1D6")
        # TODO(Keith): Logging
        return initiative_roll + self.initiative_check_bonus

    def test_morale(self, target):
        log = dict(morale_status=self.morale_status)
        dice_3d6 = Dice("3D6")
        morale_roll = log['morale_roll'] = dice_3d6.roll()
        
        # TODO(Keith): Add in bonuses for Formation

        animal_friend_bonus = 0
        if 'Animal Friend' in self.talents and target.species in ANIMAL_SPECIES:
            animal_friend_bonus = log['animal_friend_bonus'] = 2

        # TODO(Keith): Test if you have a level 10+ Warrior/Beserk (Inspiration) in the party

        attempt_result = morale_roll + self.morale_check_bonus + target.fright_mod + animal_friend_bonus
        log['attempt_result'] = attempt_result

        # NOTE(Keith): 17 and 18 always no consequence
        if morale_roll >= 17:
            return log

        morale_status = None

        if attempt_result <= 0:
            # TODO(Keith): Implement Flees
            morale_status = "Panic"
            rounds = Dice("2D6").roll()
            character.trauma_count += 1
        elif attempt_result == 1:
            morale_status = "Panic"
            rounds = Dice("1D6").roll()
        elif attempt_result == 2:
            morale_status = "Terrified"
            rounds = Dice("1D6").roll()
        elif attempt_result == 3:
            morale_status = "Fearful"
            rounds = Dice("1D6").roll()
        elif attempt_result <= 5:
            morale_status = "Afraid"
            rounds = Dice("1D6").roll()
        elif attempt_result <= 8 or morale_roll <= 4:
            morale_status = "Nervous"
            rounds = Dice("1D6").roll()

        if morale_status:
            if morale_status == self.morale_status:
                if rounds > self.morale_rounds:
                    self.morale_rounds = log['morale_rounds'] = rounds    
            else:
                self.morale_status = log['morale_status'] = morale_status
                self.morale_rounds = log['morale_rounds'] = rounds
            self.save()

        return log

    def test_skill(self, skill, target=None):

        return 0


    """
    **********************************
    **** Methods for doing stuff? ****
    **********************************
    """

    def attack(self, target, weapon=None):
        log = dict(labels=dict(),stats=dict(target_starting_HP=target.HP))
        damage_points = 0
        self_updates = []
        target_updates = []

        dice_3d6 = Dice("3D6")

        # TODO(Keith): Make unarmed work
        # TODO(Keith): Two handed weapons
        if not weapon:
            if self.handedness == "right":
                weapon = self.right_hand_weapon
            else:
                weapon = self.left_hand_weapon


        log['labels']['action'] = "{} attacks {} with {}".format(self.name, target.name, weapon.name)
        
        if weapon.weapon_type == "melee":
            attacker_OV = self.OV_melee
            target_DV = target.DV_melee
        else:
            attacker_OV = self.OV_missile
            target_DV = target.DV_missile

        log['stats']['DV'] = target_DV
        log['stats']['OV'] = attacker_OV

        attack_roll = dice_3d6.roll()
        shockack_roll = dice_3d6.roll()
        damage_roll = Dice(weapon.damage).roll()
        log['stats']['attack_roll'] = attack_roll
        log['stats']['damage_roll'] = damage_roll

        # TODO(Keith): Crits and Fumbles
        if attack_roll == 3:
            pass
        elif attack_roll == 4:
            pass
        elif attack_roll == 17:
            pass
        elif attack_roll == 18:
            pass

        attempt_result = (attack_roll + attacker_OV) - target_DV
        log['stats']['attempt_result'] = attempt_result

        # Miss
        if (attempt_result < 0 and attack_roll < 17) or attack_roll == 3:
            attack_result = "Miss"
            damage_points = 0
        # Near miss
        elif (attempt_result == 0 and attack_roll < 18) or attack_roll == 4:
            attack_result = "Near Miss"
            damage_points = int(damage_roll / 2)
        # Hit
        elif attempt_result in [1,2] and attack_roll < 19:
            damage_points = damage_roll
            attack_result = "Hit"
        # Rather good hit
        elif attempt_result in [3,4]:
            damage_points = damage_roll + 1
            attack_result = "Rather good Hit"
        # Good Hit
        elif attempt_result in [5,6]:
            damage_points = damage_roll + 2
            attack_result = "Good Hit"
        # Very Good Hit
        elif attempt_result  == 7:
            damage_points = damage_roll + 4
            attack_result = "Very Good Hit"
        # Excellent Hit
        elif attempt_result  == 8:
            damage_points = damage_roll + 8
            attack_result = "Excellent Hit"
        # Exceptional Hit
        elif attempt_result  == 9:
            damage_points = damage_roll + 16
            attack_result = "Exceptional Hit"
        # Perfect Hit
        elif attempt_result  >= 10:
            damage_points = damage_roll + 24
            attack_result = "Perfect Hit"

        log['labels']['attack_result'] = attack_result
        log['stats']['damage_points'] = damage_points

        if not damage_points:
            log['labels']['damage_result'] = "{} takes no damage".format(target.name)
            return log

        target.HP -= damage_points
        target_updates.append("HP")

        log['stats']['target_HP'] = target.HP
        log['labels']['damage_result'] = "{} takes {} damage".format(target.name, damage_points)
        
        # Cut & Shock
        cut_roll = dice_3d6.roll()
        shock_roll = dice_3d6.roll()
        log['stats']['cut_roll'] = cut_roll
        log['stats']['shock_roll'] = shock_roll

        cut_result = cut_roll - int(damage_points / 2) + weapon.cut
        shock_result = shock_roll - int(damage_points / 2) + weapon.shock + target.size
        
        log['stats']['weapon_cut'] = weapon.cut
        log['stats']['weapon_shock'] = weapon.shock
        log['stats']['target_size'] = target.size
        log['stats']['cut_result'] = cut_result
        log['stats']['shock_result'] = shock_result

        save_roll = Dice("1D12")
            
        if cut_result <= -1 and save_roll > target.size:
            target.HP = 0
            log['stats']['save_roll'] = save_roll
            cut_label = "{} has died from a cut to a vital organ"
        elif cut_result <= 2:
            CharacterCut.objects.create(character=target, severity="Serious")
            cut_label = "{} has been cut and has Serious Bleeding".format(target.name)
        elif cut_result <= 5:
            CharacterCut.objects.create(character=target, severity="Medium")
            cut_label = "{} has been cut and has Medium Bleeding".format(target.name)
        elif cut_result <= 9:
            CharacterCut.objects.create(character=target, severity="Light")
            cut_label = "{} has been cut and has Light Bleeding".format(target.name)
        else:
            cut_label = None
        if cut_label:
            log['labels']['cut_result'] = cut_label

        # TODO(Keith): Check for fall damage
        if shock_result <= -1:
            # Instant Death, no ifs, ands or buts
            target.HP = 0
            shock_label = "{} has died from blunt force trauma".format(target.name)
        elif shock_result <= 2:
            stun_status = "Knocked Out"
            stun_rounds = Dice("3D6").roll()
            target.stun_rounds = stun_rounds
            log['stats']['stun_rounds'] = stun_rounds
            shock_label = "{} has been knocked out for {} rounds".format(target.name, stun_rounds)
        elif shock_result <= 5:
            stun_status = "Knocked Down"
            shock_label = "{} has been knocked down".format(target.name)
        elif shock_result <= 9:
            stun_status = "Stunned"
            shock_label = "{} has been stunned".format(target.name)
        else:
            shock_label = None
        if shock_label:
            log['labels']['shock_result'] = shock_label

        print(log)

    def cast(self, spell, target=None):
        # TODO(Keith): Spell limit per day for each spell
        # TODO(Keith): Check for fumble and crits
        if spell not in self.spells.all():
            # TODO(Keith): better returning
            return "You don't know this spell"
        # TODO(Keith): Add verification that the function exists
        spell_class = getattr(myfarog_spells, spell.name)()
        spell_log = spell_class.cast(self, target)
        # TODO(Keith): store log
        return spell_log

    def use(self, item, target=None):

        pass

    def pickup(self, item, container=None):
        # TODO(Keith): Setup user defined default container
        if container == None:
            container = self.containers['backpack']


    """
    **********************************
    **** Miscellanous some stuff? ****
    **********************************
    """

    def round_upkeep(self):
        log = dict()
        dice_1d6 = Dice("1D6")

        if self.morale_rounds == 1:
            if self.morale_status == "Nervous":
                morale_status = "Normal"
                morale_rounds = 0
            elif self.morale_status == "Afraid":
                morale_status = "Nervous"
                morale_rounds = dice_1d6.roll()
            elif self.morale_status == "Fearful":
                morale_status = "Afraid"
                morale_rounds = dice_1d6.roll()
            elif self.morale_status == "Terrified":
                morale_status = "Fearful"
                morale_rounds = dice_1d6.roll()
            elif self.morale_status == "Panic":
                morale_status = "Terrified"
                morale_rounds = dice_1d6.roll()
            
            self.morale_status = log['morale_status'] = morale_status
            self.morale_rounds = log['morale_rounds'] = morale_rounds
            self.save(update_fields=['morale_status', 'morale_rounds'])

        elif self.morale_rounds > 1:
            morale_rounds = self.morale_rounds - 1
            self.morale_rounds = log['morale_rounds'] = morale_rounds
            self.save(update_fields=['morale_rounds'])

        if self.stun_rounds == 1:
            if self.stun_status in ["Stunned", "Knocked Down"]:
                stun_status = "Normal"
                stun_rounds = 0
            elif self.stun_status == "Knocked Out":
                stun_status = "Stunned"
                stun_rounds = dice_1d6.roll()
            self.save(update_fields=['stun_status', 'stun_rounds'])
        elif self.stun_rounds > 1:
            stun_rounds = self.stun_rounds - 1
            self.stun_rounds = log['stun_rounds'] = stun_rounds
            self.save(update_fields=['stun_rounds'])

        return log
        

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

# TODO(Keith): I dont think this needs to be done every time
def character_post_init(sender, **kwargs):
   kwargs['instance'].init_stats()
models.signals.post_init.connect(character_post_init, sender=Character)

# TODO(Keith): Post Save for MHP damage triggers

class CharacterSkill(models.Model):

    character   = models.ForeignKey(Character, on_delete=models.DO_NOTHING)
    skill       = models.ForeignKey(Skill, on_delete=models.DO_NOTHING)
    trained     = models.BooleanField(default=False)
    role_skill  = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.character, self.skill)

    class Meta:
        verbose_name = "Character Skill"
        verbose_name_plural = "Character Skills"


class CharacterTalent(models.Model):

    character   = models.ForeignKey(Character, on_delete=models.DO_NOTHING)
    talent      = models.ForeignKey(Talent, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return "{} {}".format(self.character, self.talent)

    class Meta:
        verbose_name = "Character Talent"
        verbose_name_plural = "Character Talent"


class CharacterCut(models.Model):

    character       = models.ForeignKey(Character, on_delete=models.DO_NOTHING)
    severity        = models.CharField(max_length=10, choices=CUT_SEVERITIES)
    rounds_active   = models.IntegerField(default=0)
    
    def __str__(self):
        return "{} {}".format(self.character, self.severity)

    class Meta:
        verbose_name = "Character Cut"
        verbose_name_plural = "Character Cuts"


class CharacterCompartmentItem(models.Model):
    character   = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="items")
    compartment = models.ForeignKey(Compartment, on_delete=models.DO_NOTHING)
    item        = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name        = "Character Compartment Item"
        verbose_name_plural = "Character Compartment Item"

    def __str__(self):
        return "{}'s' {} - {}".format(self.character, self.compartment, self.item)


class Party(models.Model):
    name        = models.CharField(max_length=100, blank=True, null=True)
    characters  = models.ManyToManyField(
        Character,
        blank=True,
        related_name="parties",
        related_query_name="parties",
    )
    frightener  = models.ForeignKey(Character, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="party_frightener")

    class Meta:
        verbose_name        = "Party"
        verbose_name_plural = "Parties"

def party_m2m_changed(sender, **kwargs):
    updated = False
    fright_mod = 100
    if kwargs['action'] == 'post_add':
        if kwargs['instance'].frightener:
            fright_mod = kwargs['instance'].frightener.fright_mod
        for character in Character.objects.filter(id__in=list(kwargs['pk_set'])):
            if character.fright_mod < fright_mod:
                kwargs['instance'].frightener = character
                updated = True
    elif kwargs['action'] == 'post_remove':
        frightener = None
        for character in kwargs['instance'].characters.all():
            if character.fright_mod < fright_mod:
                frightener = character
        if frightener != kwargs['instance'].frightener:
            kwargs['instance'].frightener = frightener
            updated = True

    if updated:
        kwargs['instance'].save()
models.signals.m2m_changed.connect(party_m2m_changed, sender=Party.characters.through)


class Battle(models.Model):
    name        = models.CharField(max_length=100, blank=True, null=True)
    parties     = models.ManyToManyField(
        Party,
        blank=True,
        related_name="battles",
        related_query_name="battles"
    )
    # location  = models.ForeignKey(Location, on_delete=models.DO_NOTHING)


class BattleRound(models.Model):
    battle      = models.ForeignKey(Battle, on_delete=models.DO_NOTHING, related_name="rounds")
    round       = models.IntegerField()
    step        = models.IntegerField()

    step_list   = [
        'round_upkeep',
        'test_morale', 
        'declare_actions',
        'check_for_falling',
        'test_riding',
        'check_for_random_movement',
        'test_initiative',
        'perform_actions',
        'check_for_random_item_damage'
    ]

    class Meta:
        verbose_name        = "Battle Round"
        verbose_name_plural = "Battle Rounds"

    def __str__(self):
        return "{} - Round {}".format(self.battle, self.round)

    # Start the Round
    def start(self):
        log = dict(labels=dict(), stats=dict())

        # TODO(Keith): RQ Worker proccesses the round
        print(log)

    def process_round(self):
        # TODO(Keith): Everything should be queued up, so kick off the next step
        pass


    """
    Step 0: Process statuses on round timers
    """
    def round_upkeep(self):
        log = dict()
        
        party1 = self.battle.parties.all().first()
        party2 = self.battle.parties.all().last()
        
        for character in party1.characters.all():
            log[character.id] = character.round_upkeep()

        for character in party2.characters.all():
            log[character.id] = character.round_upkeep()

        print(log)
        
    """
    Step 1: Check for Morale
    """
    def test_morale(self):
        # TODO(Keith): Need to know which Characters were damaged last round
        # TODO(Keith): Right now this only supports 2 parties
        party1 = self.battle.parties.all().first()
        party2 = self.battle.parties.all().last()
        
        for character in party1.characters.all():
            log['stats'][character.id] = character.test_morale(party2.frightener)

        for character in party2.characters.all():
            log['stats'][character.id] = character.test_morale(party1.frightener)



    """
    Step 2: Declare Actions
    """
    def declare_actions(self):
        # Requires input
        pass

        
    """
    Step 3: Check for falling
    """
    def check_for_falling(self):
        pass

    """
    Step 4: Riders test riding skill
    """
    def test_riding(self, riders):
        pass

    """
    Step 5: Check for Random Movement
    """
    def check_for_random_movement(self):
        pass

    """
    Step 6: Check for Initiative
    """
    def test_initiative(self):
        for party in self.battle.parties.all():
            for character in party:
                # TODO(Keith): Check if declared a ranged attack action
                log['stats'][character.id] = character.test_initiative()

    
    """
    Step 7: Perform Actions
    """
    def perform_actions(self):
        pass
        
    """
    Step 8: Check for Random Item Damage
    """
    def check_for_random_item_damage(self):
        pass


class BattleRoundAction(models.Model):
    battle_round    = models.ForeignKey(BattleRound, on_delete=models.DO_NOTHING, related_name="actions")
    actor           = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="actor_actions")
    # TODO(Keith)   : I'm not sure about this, should these be choices or a table pointer?
    action          = models.CharField(max_length=100)
    target          = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="target_actions")

    class Meta:
        verbose_name = "Battle Round Action"
        verbose_name_plural = "Battle Round Actions"

    def __str__(self):
        return "{} - {} - {} - {}".format(self.actor, self.action, self.target)


class BattleRoundLog(models.Model):
    battle_round    = models.ForeignKey(BattleRound, on_delete=models.DO_NOTHING, related_name="logs")
    actor           = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="actor_logs")
    action          = models.CharField(max_length=100, choices=BATTLE_ROUND_LOG_ACTIONS)
    target          = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="target_logs")
    statement       = models.CharField(max_length=500)
    results         = models.CharField(max_length=1000)

    class Meta:
        verbose_name        = "Battle Round Log"
        verbose_name_plural = "Battle Round Logs"


