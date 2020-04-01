import copy
import json
import math

from time import gmtime, strftime
che
from django.db import models

from source_framework.core.base.models import BaseSourceModel
from source_framework.core.models import SourceUser

from myfarog.models import *
from myfarog.constants.model import *
from myfarog.utils.model import (
    attr_mod,
    attr_mod_label,
    Dice
)
from myfarog import spells as myfarog_spells


class CharacterManager(models.Manager):

    def generate(self, **kwargs):
        """
        Method for generating a new Character

        It can be randomly generated completely from scratch, or you can pass in specific values for it to use.

        ***************
        * kwargs list *
        ***************

        species_id      - The id of the Species.
        gender          - The name of the Gender.
        roll_attempts   - The number of times each Attribute is rolled, taking the best roll for each
        CON             - The value for CON.
        CHA             - The value for CHA.
        DEX             - The value for DEX.
        INT             - The value for INT.
        STR             - The value for STR.
        WIL             - The value for WIL.
        social_class_id - The id of the Social Class
        birth_place_id  - The id of the Region where the Character is from.
        live_stance_id  - The id of the Life Stance.
        tribe_id        - The id of the Tribe (not sure we will use this).
        age             - The number of years old the Character is.
        role_id         - The id of the Role the Character.
        inventory       - A list of Item ids the Character starts with.
        name            - The name of the Character.

        """
        character_data = dict(skills=[])
        dice_3d6 = Dice(3,6)
        gender_mods = None

        # Step 1: Species
        if 'species_id' in kwargs:
            character_data['species'] = Species.objects.filter(id=kwargs['species_id']).first()
            if not character_data['species']:
                character_data['species'] = self.get_random_species()
        else:
            character_data['species'] = self.get_random_species()

        # Step 2: Gender
        if 'gender' in kwargs:
            character_data['gender'] = kwargs['gender']
            gender_mods = character_data['species'].gender_mods.filter(gender=character_data['gender']).first()
            if not gender_mods:
                character_data['gender'] = self.get_random_gender(species=character_data['species'])
        else:
            character_data['gender'] = self.get_random_gender(species=character_data['species'])

        if not gender_mods:
            gender_mods = character_data['species'].gender_mods.filter(gender=character_data['gender']).first()

        # Step 3: Attributes
        # NOTE(Keith): Will roll 3D6 N times for each attr, and take the best result
        # NOTE(Keith): If roll_attempts is passed, use that for N, otherwise default to 2
        roll_attempts = kwargs['roll_attempts'] if 'roll_attempts' in kwargs else 2
            
        for attr, _a in ATTRIBUTES:
            if attr in kwargs:
                character_data[attr] = kwargs[attr]
            else:
                best_attr_roll_result = 0
                for attempt in list(range(1, roll_attempts+1)):
                    roll_result = dice_3d6.roll()
                    if roll_result > best_attr_roll_result:
                        best_attr_roll_result = roll_result
                character_data[attr] = best_attr_roll_result + getattr(gender_mods, attr)

        # Step 4: Social Class
        """
        if 'social_class_id' in kwargs:
            character_data['social_class'] = SocialClass.objects.filter(id=kwargs['social_class_id']).first()
            if not character_data['social_class']:
                character_data['social_class'] = self.get_random_social_class()
        else:
            character_data['social_class'] = self.get_random_social_class()
        """

        # Step 5.1: Birthplace (Culture)
        if 'birth_place_id' in kwargs:
            character_data['birth_place'] = Culture.objects.filter(id=kwargs['birth_place_id']).first()
            if not character_data['birth_place']:
                character_data['birth_place'] = self.get_random_birth_place()
        else:
            character_data['birth_place'] = self.get_random_birth_place()

        # Step 5.2 Life Stance


        # Step 6: Apply Cultural Background Skills
        character_data['skills'] += self.get_random_culture_gender_skills(character_data['birth_place'], character_data['gender'])
        

        # Step 7: Tribe Name

        # Step 8: Age
        if 'age' in kwargs:
            character_data['age'] = kwargs['age']
        else:
            character_data['age'] = self.get_random_age(species=character_data['species'])

        # Step 9: Talents
        character_data['talents'] = []
        if 'talents' in kwargs:
            for talent_name in kwargs['talents']:
                talent = Talent.objects.filter(name=talent_name).first()
                if not talent:
                    continue
                if talent.prerequisite and talent.prerequisite not in kwargs['talents']:
                    continue
                character_data['talents'].append(talent)
        else:
            character_data['talents'] = self.get_random_talent(roll_attempts - 1)

        # Step 10: Character Role
        if 'role_id' in kwargs:
            character_data['role'] = Role.objects.filter(id=kwargs['role_id']).first()
            if not character_data['role']:
                character_data['role'] = self.get_random_role()
        else:
            character_data['role'] = self.get_random_role()        

        # Step 11: Gear

        # Step 12: Calculations & Name

        return character_data


    def get_random_species(self):
        # TODO(Keith): Add more species
        return Species.objects.all().first()

    def get_random_gender(self, species):
        gender_roll = Dice(1,100).roll()
        if gender_roll > species.gender_ratio:
            return 'male'
        else:
            return 'female'

    def get_random_age(self, species):
        age_roll = Dice(species.age).roll()
        return age_roll

    def get_random_talent(self, quantity):
        talents = []
        for k in list(range(1,quantity+1)):
            talent_query = Talent.objects.filter(prerequisite=None).exclude(id__in=[talent.id for talent in talents])
            random_index = Dice(count=1, sides=talent_query.count() - 1).roll()
            talents.append(talent_query[random_index])

        return talents

    def get_random_birth_place(self):
        culture_query = Culture.objects.all()
        random_index = Dice(count=1, sides=culture_query.count() - 1).roll()
        
        return culture_query[random_index]
        
    def get_random_culture_gender_skills(self, culture, gender):
        skills = []
        quantity = 2 if gender == 'male' else 3
        culture_gender_skills = CultureGenderSkill.objects.filter(gender=gender)
        if gender == 'male':
            culture_gender_skills = culture_gender_skills.filter(culture=culture)
    
        for k in list(range(1,quantity+1)):
            skill_query = culture_gender_skills.exclude(skill_id__in=[skill.id for skill in skills])
            random_index = Dice(count=1, sides=skill_query.count() - 1).roll()
            skills.append(skill_query[random_index].skill)
        
        return skills

    def get_random_role(self):
        pass


class Character(BaseSourceModel):

    objects = CharacterManager()

    user = models.ForeignKey(SourceUser, on_delete=models.DO_NOTHING)
    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    name = models.CharField(max_length=16)
    gender = models.CharField(max_length=16, choices=GENDER)
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    age = models.IntegerField(default=0)
    handedness = models.CharField(max_length=10, choices=HANDEDNESS_CHOICES, default='right')

    CHA = models.IntegerField(default=0)
    CON = models.IntegerField(default=0)
    DEX = models.IntegerField(default=0)
    INT = models.IntegerField(default=0)
    STR = models.IntegerField(default=0)
    WIL = models.IntegerField(default=0)
    _cha = models.IntegerField(default=0)
    _con = models.IntegerField(default=0)
    _dex = models.IntegerField(default=0)
    _int = models.IntegerField(default=0)
    _str = models.IntegerField(default=0)
    _wil = models.IntegerField(default=0)

    HP = models.IntegerField(default=0)
    SP = models.IntegerField(default=0)
    MHP = models.IntegerField(default=0)
    max_HP = models.IntegerField(default=0)
    max_SP = models.IntegerField(default=0)
    max_MHP = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    size = models.IntegerField(default=0)

    OV_melee = models.IntegerField(default=0)
    OV_missile = models.IntegerField(default=0)
    DV_melee = models.IntegerField(default=0)
    DV_missile = models.IntegerField(default=0)

    shirt_equipment = models.ForeignKey(
        Shirt,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    pants_equipment = models.ForeignKey(
        Pants,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    # TODO(Keith): Jacket and Belt
    left_hand_weapon = models.ForeignKey(
        Weapon,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        related_name="left_hand",
        default=1
    )
    left_hand_shield = models.ForeignKey(
        Shield,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="left_hand"
    )
    right_hand_weapon = models.ForeignKey(
        Weapon,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        related_name="right_hand",
        default=1
    )
    right_hand_shield = models.ForeignKey(
        Shield,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="right_hand"
    )
    armor_equipment = models.ForeignKey(
        Armor,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    helmet_equipment = models.ForeignKey(
        Helmet,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    left_glove_equipment = models.ForeignKey(
        Glove,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="left_glove"
    )
    right_glove_equipment = models.ForeignKey(
        Glove,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="right_glove"
    )
    footwear_equipment = models.ForeignKey(
        Footwear,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    necklace_equipment = models.ForeignKey(
        Necklace,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    left_earring_equipment = models.ForeignKey(
        Earring,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="left_ear"
    )
    right_earring_equipment = models.ForeignKey(
        Earring,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="right_ear"
    )
    ring_equipment = models.ForeignKey(
        Ring,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    trinket_equipment = models.ForeignKey(
        Trinket,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    
    encumbrance_status = models.CharField(max_length=16, choices=ENCUMBERANCE_STATUSES, default='Light')
    encumbrance_mod = models.IntegerField(default=0)
    health_status = models.CharField(max_length=16, choices=HEALTH_STATUSES, default='Normal')
    health_mod = models.IntegerField(default=0)
    mental_health_status = models.CharField(max_length=16, choices=MENTAL_HEALTH_STATUSES, default='Normal')
    mental_health_mod = models.IntegerField(default=0)
    stamina_status = models.CharField(max_length=16, choices=STAMINA_STATUSES, default='Normal')
    stamina_mod = models.IntegerField(default=0)
    stun_status = models.CharField(max_length=16, choices=STUN_STATUSES, default='Normal')
    stun_rounds = models.IntegerField(default=0)
    morale_status = models.CharField(max_length=16, choices=MORALE_STATUSES, default='Normal')
    morale_rounds = models.IntegerField(default=0)
    morale_check_bonus = models.IntegerField(default=0)
    morale_mod = models.IntegerField(default=0)
    psychotic_count = models.IntegerField(default=0)
    trauma_count = models.IntegerField(default=0)

    fright_mod              = models.IntegerField(default=0)
    initiative_check_bonus  = models.IntegerField(default=0)
    current_battle          = models.ForeignKey("Battle", on_delete=models.DO_NOTHING, null=True, blank=True)
    spells                  = models.ManyToManyField(
        Spell,
        blank=True,
        related_name="spells",
        related_query_name="spells",
    )
    logs                    = dict()

    @property
    def skills(self):
        skills_dict = dict()
        print("Getting skills")
        my_skills = CharacterSkill.objects.filter(character=self)
        if not my_skills:
            print("{}: Setting Skills because I can't find them".format(strftime("%H:%M:%S", gmtime())))
            self.set_skills()
            return self.skills
        
        for character_skill in my_skills:
            skills_dict[character_skill.skill.name] = character_skill.mod

        return skills_dict       

    def restore(self):
        """
        Method called to restore Character to full.
        This sets HP, SP and MHP back to max, Normalizes all Status,
        removes all Cuts, etc

        """

        self.HP = self.max_HP
        self.SP = self.max_SP
        self.MHP = self.max_MHP
        self.health_status = "Normal"
        self.stamina_status = "Normal"
        self.mental_health_status = "Normal"
        self.stun_status = "Normal"
        self.stun_rounds = 0
        self.morale_status = "Normal"
        self.morale_rounds = 0
        self.psychotic_count = 0
        self.trauma_count = 0
        self.save()
        self.cuts.all().delete()
        print("Character restored")

    """
    Method called when a Character is initialized
    Sets all derived values
    """
    def init_stats(self):
        if not self.id:
            return False

        self.set_bonuses()
        self.set_cha()
        self.set_con()
        self.set_dex()
        self.set_int()
        self.set_str()
        self.set_wil()
        self.set_level(save=False)
        self.set_size()
        self.set_max_HP()
        self.set_max_SP()
        self.set_max_MHP()
        self.set_fright_mod()
        self.set_encumbrance_condition(save=False)
        self.set_health_condition(save=False)
        self.set_mental_health_condition(save=False)
        self.set_morale_condition(save=False)
        self.set_stamina_condition(save=False)
        self.set_initiative_check_bonus()
        
        self.set_combat_values()
        print("{}: Initing Stats".format(strftime("%H:%M:%S", gmtime())))
        self.set_skills()

        self.save()

        return True

    """
    ****\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/****
    *****\  Methods for setting derived values  /*****
    ******\____________________________________/******
    """
    def set_bonuses(self):
        self.set_equipment_bonuses()
        self.set_species_bonuses()

    # TODO(Keith): Get the Height for character generation
    def set_species_bonuses(self):
        bonuses = {}

        gender_mods = self.species.gender_mods.filter(gender=self.gender).first()
        if gender_mods:
             for attr, _a in ATTRIBUTES:
                mod = getattr(gender_mods, attr)
                if mod != 0:
                    bonuses[attr] = mod


    def set_equipment_bonuses(self):
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

    def set_level(self, save=True):
        self.level = int(math.sqrt(self.exp / 250))

        if save:
            self.save(update_fields=['level'])

    def set_size(self, save=True):
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

        if save:
            self.save(update_fields=['size'])

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
        mod = self.skills['Stamina'] * 4
        if 'max_SP' in self.bonuses:
            mod += self.bonuses['max_SP']
        self.max_SP = mod

    def set_max_MHP(self):
        mod = self.WIL * 3
        if 'max_MHP' in self.bonuses:
            mod += self.bonuses['max_MHP']
        self.max_MHP = mod

    def set_encumbrance_condition(self, save=True):
        # TODO(Keith): Fix this after getting inventory up
        self.encumbrance_status = "Light"
        self.encumbrance_mod = 0

        if save:
            self.save(update_fields=['encumbrance_status', 'encumbrance_mod'])
        return True
    
    def set_health_condition(self, save=True):
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

        if save:
            self.save(update_fields=['health_status', 'health_mod'])
        return True

    def set_mental_health_condition(self, save=True):
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

        if save:
            self.save(update_fields=['mental_health_status', 'mental_health_mod'])

        return True
    
    def set_morale_condition(self, save=True):

        # TODO(Keith): Morale from Supression

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

        if save:
            self.save(update_fields=['morale_status', 'morale_mod'])

        return True

    def set_stamina_condition(self, save=True):
        if self.SP > 3 * self.max_SP / 4:
            mod = 0
            status = "Normal"
        elif self.SP > 2 * self.max_SP / 4:
            mod = -1
            status = "Tired"
        elif self.SP > 1 * self.max_SP / 4:
            mod = -2
            status = "Weary"
        elif self.SP > 0:
            mod = -3
            status = "Exhausted"
        else:
            mod = -99
            status = "Unconscious"
        
        if status != self.stamina_status:
            if status == "Tired":
                self.test_mental_toughness(1)
            elif status == "Exhausted":
                self.test_mental_toughness("D4")

        self.stamina_status = status
        self.stamina_mod = mod

        if save:
            self.save(update_fields=['stamina_status', 'stamina_mod'])

        return True
         
    def set_initiative_check_bonus(self):
        character_talents = self.talents.values_list("talent", flat=True)
        ct_mod = sum(TalentExtra.objects.filter(extra='Initiative', talent__in=character_talents).values_list("mod",flat=True))
        # TODO(Keith): Add in missile weapon bonus (actually add the value in combat where this value is used)
        self.initiative_check_bonus = self._dex + ct_mod

        #if save:
        #    self.save(update_fields=['initiative_check_bonus'])

    def set_morale_check_bonus(self):
        character_talents = self.talents.values_list("talent", flat=True)
        ct_mod = sum(TalentExtra.objects.filter(extra='Morale', talent__in=character_talents).values_list("mod",flat=True))
        # TODO(Keith): Add in logging
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

    def set_skills(self, skills_to_update=[]):

        special_case_skills = ['Dodging', 'Fortitude', 'Perception', 'Tempo']

        skill_mods = {}
        skill_mods['Stamina'] = self._skills.filter(character=self, skill__name='Stamina').first().mod
        char_skills = {}

        # Check if Trained or Role Skill, skip Stamina, we already set that
        all_skills = Skill.objects.exclude(name='Stamina').order_by('name')
        character_skills = CharacterSkill.objects.filter(character=self)
        

        for cs in character_skills:
            char_skills[cs.skill.name] = dict(role_skill=cs.role_skill)

        for skill in all_skills:
            if skills_to_update and skill.name not in skills_to_update:
                continue
            print("{}: Updating {}".format(strftime("%H:%M:%S", gmtime()), skill.name))
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
                elif skill.name == 'Tempo':
                    mod = 40 + (5 * self._str)
                    logs.append(dict(label="Base", value=40))
                    logs.append(dict(label="Str * 5", value=(self._str * 5)))

            if skill.name in char_skills:
                if char_skills[skill.name]['role_skill']:
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
                if skills_to_update and skill_name not in skills_to_update:
                    continue
                if skill_name not in skill_mods:
                    oh_shit_wtf_yo()
                skill_mods[skill_name] += ts.mod
                self.logs[ts.skill.name] = self.logs[ts.skill.name] + [dict(label=ct.talent.name, value=ts.mod)]
        
        for _sn, _m in skill_mods.items():
          
            _s = Skill.objects.get(name=_sn)
            cs, created = CharacterSkill.objects.get_or_create(character=self, skill=_s)
            if cs.mod != _m:
                cs.mod = _m
                cs.save(update_fields=['mod'])
        
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
        
        cs, created = CharacterSkill.objects.get_or_create(character=self, skill="Stamina")
        cs.mod = mod
        cs.save(update_fields=['mod'])
        


    def set_combat_values(self):
        self.set_OV_melee()
        self.set_OV_missile()
        self.set_DV_melee()
        self.set_DV_missile()

    def set_OV_melee(self):
        self.logs['OV_melee'] = []
        logs = []
        mod = 0
        melee_bonus = self.skills['Melee']
        
        mod += melee_bonus
        logs.append(dict(label="Melee Skill", value=melee_bonus))

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
        missile_bonus = self.skills['Missile']

        mod += missile_bonus
        logs.append(dict(label="Missile Skill", value=missile_bonus))
        
        if self.helmet_equipment:
            mod += self.helmet_equipment.missile_mod
            logs.append(dict(label="Helmet", value=self.helmet_equipment.missile_mod))

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

        melee_bonus = self.skills['Melee']
        dodge_bonus = self.skills['Dodging']
        
        mod = 10
        logs.append(dict(label="Base", value=10))

        mod += melee_bonus
        logs.append(dict(label="Melee Skill", value=melee_bonus))

        mod += dodge_bonus
        logs.append(dict(label="Dodging Skill", value=dodge_bonus))

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
        dodge_bonus = self.skills['Dodging']

        mod = 10
        logs.append(dict(label="Base", value=10))

        mod += dodge_bonus
        logs.append(dict(label="Dodging Skill", value=dodge_bonus))

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
    ****\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/****
    *****\  Methods for testing (Skills, Morale, Initiative, etc)  /*****
    ******\_______________________________________________________/******
    """
    def test_initiative(self, ranged=False):
        # TODO(Keith): Add ranged bonus
        initiative_roll = Dice("1D6").roll()
        # TODO(Keith): Logging
        return initiative_roll + self.initiative_check_bonus

    def test_morale(self, target):
        data = dict(stats=dict())
        tmt_data = dict(stats=dict())
        dice_3d6 = Dice("3D6")
        morale_roll = data['stats']['morale_roll'] = dice_3d6.roll()
        
        # TODO(Keith): Add in bonuses for Formation

        animal_friend_bonus = 0
        if self.talents.filter(talent__name='Animal Friend') and target.species in ANIMAL_SPECIES:
            animal_friend_bonus = data['stats']['animal_friend_bonus'] = 2

        # TODO(Keith): Test if you have a level 10+ Warrior/Beserk (Inspiration) in the party
        # TODO(Keith): ... this should actually be a little more dynamic, like a party bonus is applied 
        # TODO(Keith): ... via the character with the ability

        attempt_result = morale_roll + self.morale_check_bonus + target.fright_mod + animal_friend_bonus
        data['stats']['attempt_result'] = attempt_result

        # NOTE(Keith): 17 and 18 always no consequence
        if morale_roll >= 17:
            return data

        morale_status = None

        if attempt_result <= 0:
            # TODO(Keith): Implement Flees
            morale_status = "Panic"
            rounds = Dice("2D6").roll()
            self.trauma_count += 1
            tmt_data = self.test_mental_toughness("D12")
        elif attempt_result == 1:
            morale_status = "Panic"
            rounds = Dice("1D6").roll()
            tmt_data = self.test_mental_toughness("D8")
        elif attempt_result == 2:
            morale_status = "Terrified"
            rounds = Dice("1D6").roll()
            tmt_data = self.test_mental_toughness("D6")
        elif attempt_result == 3:
            morale_status = "Fearful"
            rounds = Dice("1D6").roll()
            tmt_data = self.test_mental_toughness("D4")
        elif attempt_result <= 5:
            morale_status = "Afraid"
            rounds = Dice("1D6").roll()
            tmt_data = self.test_mental_toughness(1)
        elif attempt_result <= 8 or morale_roll <= 4:
            morale_status = "Nervous"
            rounds = Dice("1D6").roll()

        if morale_status:
            if morale_status == self.morale_status:
                if rounds > self.morale_rounds:
                    self.morale_rounds = rounds    
            else:
                self.morale_status = morale_status
                self.morale_rounds = rounds

            self.save(update_fields=['morale_status','morale_rounds'])

        data = {**data, **tmt_data}

        return data

    def test_mental_toughness(self, damage_dice, dd_target=18):
        data = dict(stats=dict())
        mental_health_roll = data['stats']['mental_health_roll'] = Dice("3D6").roll()
        data['stats']['level'] = self.level

        # TODO(Keith): Add modifiers for Flaws
        fearless_bonus = 0
        strong_minded_bonus = 0
        if self.talents.filter(talent__name='Fearless'):
            fearless_bonus = data['stats']['fearless_bonus'] = 2
        if self.talents.filter(talent__name='Strong Minded'):
            strong_minded_bonus = data['stats']['strong_minded_bonus'] = 2

        attempt_result = mental_health_roll + self.level + fearless_bonus + strong_minded_bonus

        multiplier = 0

        if mental_health_roll == 3 or attempt_result <= 13:
            multiplier = 2
        elif mental_health_roll == 4 or attempt_result <= dd_target - 1:
            multiplier = 1
        elif mental_health_roll == 17 or attempt_result == dd_target:
            multiplier = 1/2

        data['stats']['multiplier'] = multiplier

        damage_dice_result = Dice(damage_dice).roll()
        damage_result = int(damage_dice_result * multiplier)

        if damage_result > 0:
            self.MHP -= damage_result
        
        self.save(update_fields=['MHP'])

        return data

    def test_skill(self, skill, target=None):

        return 0


    """
    ****\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/****
    *****\            Methods for battle stuff            /*****
    ******\______________________________________________/******
    """

    def take_damage(self, amount, type="Physical"):
        # TODO(Keith): This needs to check against Toughness and reduce the amount then apply the -=
        # TODO(Keith): ... then need to update all existing places that deincrement HP
        pass

    def round_upkeep(self):
       self.process_morale_upkeep()
       self.process_cut_upkeep()
       self.process_stun_upkeep()
       self.process_posion_upkeep()

    def process_morale_upkeep(self):
        update_fields = []
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
            
            self.morale_status = morale_status
            self.morale_rounds =  morale_rounds
            update_fields += ['morale_status', 'morale_rounds']

        elif self.morale_rounds > 1:
            morale_rounds = self.morale_rounds - 1
            self.morale_rounds = morale_rounds
            update_fields += ['morale_rounds']

        self.save(update_fields=update_fields)

    def process_cut_upkeep(self):
        cuts = CharacterCut.objects.filter(character=self)
        HP_changed = False
        if not cuts:
            return False
        
        for cut in cuts:
            cut.rounds_active += 1
            if cut.severity == "Light":
                if cut.rounds_active % 120 == 0:
                    self.HP -= 1
                    # TODO(Keith): Log the source
                    HP_changed = True
                if cut.rounds_active == 720:
                    CharacterCut.objects.filter(id=cut.id).delete()
            elif cut.severity == "Medium":
                if cut.rounds_active % 12 == 0:
                    self.HP -= 1
                    # TODO(Keith): Log the source
                    HP_changed = True
                if cut.rounds_active == 72:
                    CharacterCut.objects.filter(id=cut.id).delete()
                    CharacterCut.objects.create(character=self, severity="Light")
            elif cut.severity == "Serious":
                self.HP -= 1
                # TODO(Keith): Log the source
                HP_changed = True
                if cut.rounds_active == 6:
                    CharacterCut.objects.filter(id=cut.id).delete()
                    CharacterCut.objects.create(character=self, severity="Medium")

        if HP_changed:
            self.save(update_fields=['HP'])
   
    def process_stun_upkeep(self):
        update_fields = []
        dice_1d6 = Dice("1D6")

        if self.stun_rounds == 1:
            if self.stun_status in ["Stunned", "Knocked Down"]:
                stun_status = "Normal"
                stun_rounds = 0
            elif self.stun_status == "Knocked Out":
                stun_status = "Stunned"
                stun_rounds = dice_1d6.roll()
            update_fields += ['stun_status', 'stun_rounds']

        elif self.stun_rounds > 1:
            stun_rounds = self.stun_rounds - 1
            self.stun_rounds = stun_rounds
            update_fields += ['stun_rounds']

        self.save(update_fields=update_fields)        
                 
    def process_posion_upkeep(self):
        # TODO(Keith): Implent Posion first
        pass
        
    def declare_action(self, battle_round, action, **kwargs):
        # TODO(Keith): Should this default to the only battle round you are in so we dont pass battle_round?
        # NOTE(Keith): If you already have an action for this round, delete it so we can create a new one
        my_action = battle_round.actions.filter(actor=self).first()
        if my_action:
            battle_round.actions.filter(actor=self).delete()

        if action == 'attack':
            parameters = dict(
                weapon      = kwargs['weapon'],
                target_id   = kwargs['target_id']
            )
        elif action == 'cast':
            parameters = dict(
                spell       = kwargs['spell'],
                power_level = kwargs['power_level'],
                target_id   = kwargs['target_id']
            )
        else:
            action_not_implemented()

        battle_round.actions.create(actor=self, action=action, parameters=json.dumps(parameters))
        message = "Action {}".format("Updated" if my_action else "Created")
        print(message)
        return message


    """
    ****\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/****
    *****\        Triggers for updating stats when others change        /*****
    ******\____________________________________________________________/******
    """

    def process_weight_change(self, original_value, new_value):
        self.set_size()
        return True

    def process_HP_change(self, original_value, new_value):
        current_status = copy.copy(self.health_status)
        
        self.set_health_condition()
        amount = original_value - new_value
        updated_status = None
        if current_status != self.health_status:
            updated_status = self.health_status
        if amount > 0:
            self.HP_damage_to_MHP_damage(amount, updated_status)
        # TODO(Keith): I think we need a pub sub event system here so we can tell the battle round there was damage

        return self.HP, updated_status

    def process_MHP_change(self, original_value, new_value):
        self.set_mental_health_condition()
        return True

    def process_SP_change(self, original_value, new_value):
        self.set_stamina_condition()
        return True

    def HP_damage_to_MHP_damage(self, hp_damage, h_status):
        damage_dice = None
        if h_status == "Seriously Injured":
            damage_dice = "D4"
        elif h_status == "Severely Injured":
            damage_dice = "D6"

        if hp_damage >= 3:
            if damage_dice:
                damage_dice += "+1"
            else:
                damage_dice = 1

        if damage_dice:
            return self.test_mental_toughness(damage_dice)
        else:
            return dict(stats=dict())

    def process_health_status_change(self, original_value, new_value):
        print("{}: Processing Health Status Change".format(strftime("%H:%M:%S", gmtime())))
        self.set_skills()
        return True

    def process_mental_health_status_change(self, original_value, new_value):
        print("{}: Processing Mental Health Status Change".format(strftime("%H:%M:%S", gmtime())))
        self.set_skills()
        return True

    def process_stamina_status_change(self, original_value, new_value):
        print("{}: Processing Stamina Status Change".format(strftime("%H:%M:%S", gmtime())))
        self.set_skills()
        return True

    def process_xp_change(self, original_value, new_value):
        self.set_level()
        return True

    def process_trauma_count_change(self, original_value, new_value):
        self.set_skills(['Perception'])
        return True

    def process_skill_change(self, original_value, new_value):
        print("{}: Processing Skill Change".format(strftime("%H:%M:%S", gmtime())))
        self.set_skills()
        return True

    def process_talent_change(self, original_value, new_value):
        print("{}: Processing Talent Change".format(strftime("%H:%M:%S", gmtime())))
        CharacterTalent.objects.all().talent.skills.filter(skill__name='World Lore')
        if new_value.talent.skills.filter(skill__name='Initiative'):
            self.set_initiative_check_bonus()
        elif new_value.talent.skills.filter(skill__name='Morale'):
            self.set_morale_check_bonus()
        elif new_value.talent.skills.filter(skill__name='Stamina'):
            self.set_stamina_mod()
        
        self.set_skills()
        return True


    """
    ****\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/****
    *****\         Methods for doing stuff?         /*****
    ******\________________________________________/******
    """

    def attack(self, weapon, target_id):
        target = None
        if target_id:
            target = Character.objects.filter(id=target_id).first()

        log = dict(logs=dict(), stats=dict())
        
        damage_points = 0
        self_updates = []
        target_updates = []

        dice_3d6 = Dice("3D6")

        # TODO(Keith): Check for limitations from Morale (ie Tactical Retreat)
        # TODO(Keith): Two handed weapons
        
        if not weapon:
            if self.handedness == "right":
                weapon = self.right_hand_weapon
            else:
                weapon = self.left_hand_weapon


        log['logs']['action'] = "{} attacks {} with {}".format(self.name, target.name, weapon.name)
        
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
        elif (attempt_result <= 0 and attack_roll < 18) or attack_roll == 4:
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
        else:
            # NOTE(Keith): I think i fixed this now
            print("*************************")
            print("**** Whoa Nelly!!!!! ****")
            print("*************************")
            import pdb; pdb.set_trace()

        log['logs']['attack_result'] = attack_result
        log['stats']['damage_points'] = damage_points

        self.SP -= 2
        self.save(update_fields=['SP'])

        if not damage_points:
            log['logs']['damage_result'] = "{} takes no damage".format(target.name)
            return log
        self.current_battle.rounds.last().damaged_characters.add(target)
        target.HP -= damage_points
        target_updates.append('HP')
        log['logs']['damage_result'] = "{} takes {} damage".format(target.name, damage_points)
        if target.HP <= 0:
            log['logs']['damage_result'] += " and is Fatally Injured"
        
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
            log['logs']['cut_result'] = cut_label

        # TODO(Keith): Check for fall damage if fall down (Acrobatics)
        if shock_result <= -1:
            # Instant Death, no ifs, ands or buts
            target.HP = 0
            shock_label = "{} has died from blunt force trauma".format(target.name)
        elif shock_result <= 2:
            target.stun_status = "Knocked Out"
            stun_rounds = Dice("3D6").roll()
            target.stun_rounds = stun_rounds
            log['stats']['stun_rounds'] = stun_rounds
            shock_label = "{} has been knocked out for {} rounds".format(target.name, stun_rounds)
            target_updates.append('stun_status')
            target_updates.append('stun_rounds')
        elif shock_result <= 5:
            target.stun_status = "Knocked Down"
            shock_label = "{} has been knocked down".format(target.name)
            target_updates.append('stun_status')
        elif shock_result <= 9:
            target.stun_status = "Stunned"
            shock_label = "{} has been stunned".format(target.name)
            target_updates.append('stun_status')
        else:
            shock_label = None
        if shock_label:
            log['logs']['shock_result'] = shock_label

        target.save(update_fields=target_updates)

        print(log)
        return log

    def cast(self, spell, power_level, target_id=None):

        target = None
        if target_id:
            target = Character.objects.filter(id=target_id).first()

        if type(spell) == str:
            spell = Spell.objects.filter(name=spell).first()
        if not spell:
            spell_does_not_exist()
        # TODO(Keith): Spell limit per day for each spell
        # TODO(Keith): Check for fumble and crits
        if spell not in self.spells.all():
            # TODO(Keith): better returning
            print("You don't know this spell")
            return False
        # TODO(Keith): Add verification that the function exists
        # TODO(Keith): This is somehow targeting self
        spell_class = getattr(myfarog_spells, spell.name)()
        if power_level not in spell_class.power_levels:
            print("This Power Level is not available for this Spell")
            return False
        max_PL = min(self._int * 2, self.level / 2)
        if power_level > max_PL:
            print("You can't cast at this power level")
            return False

        self.SP -= power_level
        spell_log = spell_class.cast(self, power_level, target)
        # TODO(Keith): store log
        return spell_log

    def use(self, item, target=None):

        pass

    def pickup(self, item, container=None):
        # TODO(Keith): Setup user defined default container
        if container == None:
            container = self.containers['backpack']


    """
    ****\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/****
    *****\  Extend default save function to check for triggers  /*****
    ******\____________________________________________________/******
    """

    def save(self, *args, **kwargs):
        # NOTE(Keith): Make a copy of the object before the save
        original_self = Character.objects.get(id=self.id)

        super(Character, self).save(*args, **kwargs)

        # NOTE(Keith): If these fields update, update these other fields
        updated_field_trigger = dict(
            weight                  = self.process_weight_change,
            MHP                     = self.process_MHP_change,
            HP                      = self.process_HP_change,
            SP                      = self.process_SP_change,
            mental_health_status    = self.process_mental_health_status_change,
            health_status           = self.process_health_status_change,
            stamina_status          = self.process_stamina_status_change,
            max_MHP                 = self.process_mental_health_status_change,
            max_HP                  = self.process_health_status_change,
            max_SP                  = self.process_stamina_status_change,
            exp                     = self.process_xp_change,
            trauma_count            = self.process_trauma_count_change,
        )
        # TODO(Keith): Bonuses/Nerfs need to trigger as well
        # TODO(Keith): External areas that need to trigger: CharacterRole, Inventory, Equipping

        for field in updated_field_trigger:
            if 'update_fields' in kwargs and field not in kwargs['update_fields']:
                continue
            if getattr(self, field) != getattr(original_self, field):
                print("{}: Running {} from {} update".format(strftime("%H:%M:%S", gmtime()), updated_field_trigger[field], field))
                updated_field_trigger[field](getattr(original_self, field), getattr(self, field))

        pubsub.trigger(MyfarogEvents.CHARACTER_CHANGE, **{})


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

# TODO(Keith): This needs to be run after the character is created initially (post_create?)
def character_post_init(sender, **kwargs):
    kwargs['instance'].init_stats()
#models.signals.post_init.connect(character_post_init, sender=Character)




# TODO(Keith): Post Save for MHP damage triggers

class CharacterSkill(BaseSourceModel):

    character   = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="_skills")
    skill       = models.ForeignKey(Skill, on_delete=models.DO_NOTHING)
    trained     = models.BooleanField(default=False)
    role_skill  = models.BooleanField(default=False)
    mod         = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        # NOTE(Keith): Make a copy of the object before the save
        original_self = CharacterSkill.objects.get(id=self.id)

        super(CharacterSkill, self).save(*args, **kwargs)

        # NOTE(Keith): This causes a near inifinite loop
        #self.character.process_skill_change(original_self, self)


    def __str__(self):
        return "{} {} {}".format(self.character, self.skill, self.mod)

    class Meta:
        verbose_name = "Character Skill"
        verbose_name_plural = "Character Skills"


class CharacterTalent(BaseSourceModel):

    character   = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="talents")
    talent      = models.ForeignKey(Talent, on_delete=models.DO_NOTHING)


    def save(self, *args, **kwargs):
        # NOTE(Keith): Make a copy of the object before the save
        original_self = CharacterTalent.objects.get(id=self.id)

        super(CharacterTalent, self).save(*args, **kwargs)

        self.character.process_talent_change(original_self, self)

    
    def __str__(self):
        return "{} {}".format(self.character, self.talent)

    class Meta:
        verbose_name = "Character Talent"
        verbose_name_plural = "Character Talent"


class CharacterCut(BaseSourceModel):

    character       = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="cuts")
    severity        = models.CharField(max_length=10, choices=CUT_SEVERITIES)
    rounds_active   = models.IntegerField(default=0)
    
    def __str__(self):
        return "{} {}".format(self.character, self.severity)

    class Meta:
        verbose_name = "Character Cut"
        verbose_name_plural = "Character Cuts"


class CharacterCompartmentItem(BaseSourceModel):
    character   = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="items")
    compartment = models.ForeignKey(Compartment, on_delete=models.DO_NOTHING)
    item        = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name        = "Character Compartment Item"
        verbose_name_plural = "Character Compartment Item"

    def __str__(self):
        return "{}'s' {} - {}".format(self.character, self.compartment, self.item)



class Party(BaseSourceModel):
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

"""
Method to keep the fright mod of the Party set to the lowest value.
"""
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


# TODO(Keith): Need some kind of PartyBonus
