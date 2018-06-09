from myfarog.utils.model import Dice

class _spell(object):

    def __init__(self):
        pass

    def cast(self, caster, target):
        raise ValueError('You should be overriding this in your extension class.')


class Alarm_Bell(_spell):
    pass


class Awakening(_spell):
    pass


class Bear_Hug(_spell):
    pass


class Calm_Creature(_spell):
    pass


class Charm(_spell):
    pass


class Clairvoyance(_spell):
    pass


class Conscience(_spell):
    pass


class Courage(_spell):
    pass


class Create_Hulda(_spell):
    pass


class Creatue_Stone_Guardian(_spell):
    pass


class Create_Nar(_spell):
    pass


class Create_Wight(_spell):
    pass


class Cure_Malaria(_spell):
    pass


class Cure_Trama(_spell):
    pass


class Curse(_spell):
    pass


class Disclose_Observation(_spell):
    pass


class Discover_Posion(_spell):
    pass


class Dispel(_spell):
    pass


class Divine_Language(_spell):
    pass


class Divine_Senses(_spell):
    pass


class Eternal_Flame(_spell):
    pass


class Ettin_Eyes(_spell):
    pass


class False_Sound(_spell):
    pass


class Fear(_spell):
    
    def cast(self, caster, target):
        log = dict(
            labels=dict(),
            stats=dict(target_starting_morale_status=target.morale_status)
        )
        dice_3d6 = Dice("3D6")

        # TODO(Keith): Check for immunity

        log['labels']['action'] = "{} casts Fear on {} ".format(caster.name, target.name)

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

        


class Fireball(_spell):
    pass


class Fire_Bolt(_spell):
    pass


class Flight(_spell):
    pass


class Fog(_spell):
    pass


class Fruit_of_Nature(_spell):
    pass


class Fulgjon(_spell):
    pass


class Fumble_Foe(_spell):
    pass


class Ghost_Feet(_spell):
    pass


class Grace_of_NurpuR(_spell):
    pass


class Hammer(_spell):
    pass


class Heal(_spell):
    pass


class Heat_Signature(_spell):
    pass


class Hood_of_HadnuR(_spell):
    pass


class Hostility(_spell):
    pass


class Hunt(_spell):
    pass


class Ice_Heart(_spell):
    pass


class Illusion(_spell):
    pass


class Initiate(_spell):
    pass


class Levitation(_spell):
    pass


class Light(_spell):
    def cast(self):
        print("You cast light!")


class Lightning(_spell):
    pass


class Lung_of_NerpuR(_spell):
    pass


class Magenerpi(_spell):
    pass


class Malaria(_spell):
    pass


class Manipulate_Water(_spell):
    pass


class Manipulate_Weather(_spell):
    pass


class Manipulate_Wind(_spell):
    pass


class Mask(_spell):
    pass


class Mind_Control(_spell):
    pass


class Mind_Reading(_spell):
    pass


class Mistletoe(_spell):
    pass


class Moss_Mask(_spell):
    pass


class Neutalise_Posion(_spell):
    pass


class Night_Vision(_spell):
    pass


class Observation(_spell):
    pass


class Paralyse(_spell):
    pass


class Petrifacation(_spell):
    pass


class Poison(_spell):
    pass


class Purify_Nutrition(_spell):
    pass


class Remove_Curse(_spell):
    pass


class Remove_Paralysis(_spell):
    pass


class Resist_Disease(_spell):
    pass


class Resist_Poison(_spell):
    pass


class Restoration(_spell):
    pass


class Resurrection(_spell):
    pass


class Reverse_Petrification(_spell):
    pass


class Sanctuary(_spell):
    pass


class Sacred_Ground(_spell):
    pass


class Seven_Mile_Boots(_spell):
    pass


class Silence(_spell):
    pass


class Snowflake(_spell):
    pass


class Sorcerous_Shape(_spell):
    pass


class Sorcerous_Sleep(_spell):
    pass


class Spirit_Voice(_spell):
    pass


class Summon_Creature(_spell):
    pass


class Telekinesis(_spell):
    pass


class Telepathy(_spell):
    pass


class Teleportation(_spell):
    pass


class Totem_Animal(_spell):
    pass


class Trojan_Fortress(_spell):
    pass


class Troll_Fear(_spell):
    pass


class Veil(_spell):
    pass


class Void_Travel(_spell):
    pass


class Wall_of_Thorns(_spell):
    pass


class Whirlwind(_spell):
    pass


class Wind_Gust(_spell):
    pass

