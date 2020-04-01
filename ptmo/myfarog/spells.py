from myfarog.utils.model import Dice

class Spell(object):

    power_levels = []

    def __init__(self):
        pass

    def cast(self, caster, power_level, target):
        raise ValueError('You should be overriding this in your extension class.')


class Alarm_Bell(Spell):
    pass


class Awakening(Spell):
    pass


class Bear_Hug(Spell):
    pass


class Calm_Creature(Spell):
    pass


class Charm(Spell):
    pass


class Clairvoyance(Spell):
    pass


class Conscience(Spell):
    pass


class Courage(Spell):
    pass


class Create_Hulda(Spell):
    pass


class Creatue_Stone_Guardian(Spell):
    pass


class Create_Nar(Spell):
    pass


class Create_Wight(Spell):
    pass


class Cure_Malaria(Spell):
    pass


class Cure_Trama(Spell):
    pass


class Curse(Spell):
    pass


class Disclose_Observation(Spell):
    pass


class Discover_Posion(Spell):
    pass


class Dispel(Spell):
    pass


class Divine_Language(Spell):
    pass


class Divine_Senses(Spell):
    pass


class Eternal_Flame(Spell):
    pass


class Ettin_Eyes(Spell):
    pass


class False_Sound(Spell):
    pass


class Fear(Spell):

    power_levels = [1]
    
    def cast(self, caster, power_level, target):
        log = dict(
            labels=dict(),
            stats=dict(target_starting_morale_status=target.morale_status)
        )
        dice_3d6 = Dice("3D6")

        # TODO(Keith): Check for immunity

        log['labels']['action'] = "{} casts Fear on {} ".format(caster.name, target.name)
        import pdb; pdb.set_trace()
        base                = log['stats']['base']                  = 12
        target_fortitude    = log['stats']['target_fortitude']      = target.skills['Fortitude']
        caster_proficiency  = log['stats']['caster_proficiency']    = caster.skills['Fortitude']
        roll                = log['stats']['roll']                  = dice_3d6.roll()
        attempt_result      = log['stats']['attempt_result']        = (target_fortitude + roll) - 12 + caster_proficiency
        duration            = dice_3d6.roll()

        if roll < 5:
            save_result     = "Critical Failure"
            morale_status   = "Terrified"
        elif roll < 0:
            save_result     = "Failure"
            morale_status   = "Fearful"
        elif roll == 0:
            save_result     = "Semi-Success"
            morale_status   = "Nervous"
        else:
            save_result     = "Success"
            morale_status   = None

        if morale_status:
            target.morale_status         = log['stats']['new_morale_status'] = morale_status
            log['stats']['duration']     = duration
            log['labels']['cast_result'] = "{}'s save is a {} and is {} for {} rounds".format(target.name, save_result, morale_status, duration)
        else:
            log['labels']['cast_result'] = "{}'s save is a Success and is still {}".format(target.name, target.morale_status)

        return log


class Fireball(Spell):
    pass


class Fire_Bolt(Spell):
    pass


class Flight(Spell):
    pass


class Fog(Spell):
    pass


class Fruit_of_Nature(Spell):
    pass


class Fulgjon(Spell):
    pass


class Fumble_Foe(Spell):
    pass


class Ghost_Feet(Spell):
    pass


class Grace_of_NurpuR(Spell):
    pass


class Hammer(Spell):
    pass


class Heal(Spell):
    pass


class Heat_Signature(Spell):
    pass


class Hood_of_HadnuR(Spell):
    pass


class Hostility(Spell):
    pass


class Hunt(Spell):
    pass


class Ice_Heart(Spell):
    pass


class Illusion(Spell):
    pass


class Initiate(Spell):
    pass


class Levitation(Spell):
    pass


class Light(Spell):
    def cast(self, caster, power_level, target):
        print("You cast light!")


class Lightning(Spell):

    power_levels = [1]
    
    def cast(self, caster, power_level, target):
        pass


class Lung_of_NerpuR(Spell):
    pass


class Magenerpi(Spell):
    pass


class Malaria(Spell):
    pass


class Manipulate_Water(Spell):
    pass


class Manipulate_Weather(Spell):
    pass


class Manipulate_Wind(Spell):
    pass


class Mask(Spell):
    pass


class Mind_Control(Spell):
    pass


class Mind_Reading(Spell):
    pass


class Mistletoe(Spell):
    pass


class Moss_Mask(Spell):
    pass


class Neutalise_Posion(Spell):
    pass


class Night_Vision(Spell):
    pass


class Observation(Spell):
    pass


class Paralyse(Spell):
    pass


class Petrifacation(Spell):
    pass


class Poison(Spell):
    pass


class Purify_Nutrition(Spell):
    pass


class Remove_Curse(Spell):
    pass


class Remove_Paralysis(Spell):
    pass


class Resist_Disease(Spell):
    pass


class Resist_Poison(Spell):
    pass


class Restoration(Spell):
    pass


class Resurrection(Spell):
    pass


class Reverse_Petrification(Spell):
    pass


class Sanctuary(Spell):
    pass


class Sacred_Ground(Spell):
    pass


class Seven_Mile_Boots(Spell):
    pass


class Silence(Spell):
    pass


class Snowflake(Spell):
    pass


class Sorcerous_Shape(Spell):
    pass


class Sorcerous_Sleep(Spell):
    pass


class Spirit_Voice(Spell):
    pass


class Summon_Creature(Spell):
    pass


class Telekinesis(Spell):
    pass


class Telepathy(Spell):
    pass


class Teleportation(Spell):
    pass


class Totem_Animal(Spell):
    pass


class Trojan_Fortress(Spell):
    pass


class Troll_Fear(Spell):
    pass


class Veil(Spell):
    pass


class Void_Travel(Spell):
    pass


class Wall_of_Thorns(Spell):
    pass


class Whirlwind(Spell):
    pass


class Wind_Gust(Spell):
    pass

