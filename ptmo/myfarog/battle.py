import django_rq
import json
import requests

from django.conf import settings
from django.db import models

from source_framework.core import BaseSourceModel

from myfarog.models import *
from myfarog.constants.model import *
from myfarog.character import (
    Character,
    Party
)


class Battle(BaseSourceModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)
    parties = models.ManyToManyField(
        Party,
        blank=True,
        related_name="battles",
        related_query_name="battles"
    )
    # location  = models.ForeignKey(Location, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Battle"
        verbose_name_plural = "Battles"

    def __str__(self):
        return self.name

    def emit_message(self, msg, character_id=None):

        endpoint = "{}://{}:{}/api/myfarog/battle/update/".format(
            settings.NODE_URL_PROTOCOL,
            settings.NODE_URL,
            settings.NODE_PORT
        )

        payload = dict(msg=msg, battle_id=self.id)
        if character_id:
            payload['character_id'] = character_id
        result = requests.post(endpoint, headers={'content-type': 'application/json'}, data=json.dumps(payload))
        return result


class BattleRound(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.DO_NOTHING, related_name="rounds")
    round = models.IntegerField(default=1)
    step = models.IntegerField(default=0)
    pending_actions = models.IntegerField(default=0)
    damaged_characters = models.ManyToManyField(
        Character,
        blank=True,
        related_name="damaged_rounds",
        related_query_name="damaged_rounds",
    )

    step_list = [
        'round_upkeep',
        'test_morale', 
        'declare_actions',
        'check_for_falling',
        'test_riding',
        'check_for_random_movement',
        'test_initiative',
        'perform_actions',
        'check_for_random_item_damage',
        'end_round'
    ]

    class Meta:
        verbose_name        = "Battle Round"
        verbose_name_plural = "Battle Rounds"

    def __str__(self):
        return "{} - Round {}".format(self.battle, self.round)

    # Start the Round
    def start(self):
        pending_actions = 0

        for party in self.battle.parties.all():
            for character in party.characters.all():
                pending_actions += 1

        self.step = 0
        self.pending_actions = pending_actions
        self.save(update_fields=['step', 'pending_actions'])

        self.process_round()

    def process_round(self):
        step_log = getattr(self,self.step_list[self.step])()
        step_log['step']        = self.step
        step_log['step_label']  = self.step_list[self.step]
        self.battle.emit_message(step_log)
        self.step += 1
        self.save(update_fields=['step'])
        
        # NOTE(Keith) End the round after step 8
        if self.step not in [3,10]:
            django_rq.enqueue(self.process_round)
        

    """
    Step 0: Process statuses on round timers
    """
    def round_upkeep(self):
        data = dict(round=self.round)

        for party in self.battle.parties.all():
            for character in party.characters.all():
                character.round_upkeep()

        return data
        
    """
    Step 1: Check for Morale
    """
    def test_morale(self):
        data = dict()

        # TODO(Keith): Right now this only supports 2 party battles
        party1 = self.battle.parties.all().first()
        party2 = self.battle.parties.all().last()

        # NOTE(Keith): Check for characters damaged last round
        if self.round == 1:
            party1_testees = party1.characters.all()
            party2_testees = party2.characters.all()
        else:
            damaged_characters = self.battle.rounds.get(round=self.round - 1).damaged_characters.all().values_list('id', flat=True)
            if not damaged_characters:
                return data
            party1_testees = party1.characters.filter(id__in=damaged_characters)
            party2_testees = party2.characters.filter(id__in=damaged_characters)
        
        for character in party1_testees:
            morale_data = character.test_morale(party2.frightener)
            #TODO(Keith): Can include morale_data['stats'] as well

        for character in party2_testees:
            morale_data = character.test_morale(party1.frightener)

        return data

    """
    Step 2: Declare Actions
    """
    def declare_actions(self):
        data = dict()
        print("Waiting for users to input their actions ...")

        return data
        
    """
    Step 3: Check for falling
    """
    def check_for_falling(self):
        data = dict(logs=dict())
        #data['logs']['check_for_falling'] = "Not implemented"
        
        return data

    """
    Step 4: Riders test riding skill
    """
    def test_riding(self):
        data = dict(logs=dict())
        #data['logs']['test_riding'] = "Not implemented"
        
        return data

    """
    Step 5: Check for Random Movement
    """
    def check_for_random_movement(self):
        data = dict(logs=dict())
        #data['logs']['check_for_random_movement'] = "Not implemented"
        
        return data
    
    """
    Step 6: Check for Initiative
    """
    def test_initiative(self):
        data = dict(stats=dict())
        for party in self.battle.parties.all():
            for character in party.characters.all():
                # TODO(Keith): Check if declared a ranged attack action
                character_initiative = character.test_initiative()
                self.initiatives.create(battle_round=self, character=character, value=character_initiative)
                data['stats'][character.id] = character_initiative
        return data

    """
    Step 7: Perform Actions
    """
    def perform_actions(self):
        data = dict()
        # TODO(Keith): This way makes way too many calls, rework so it only pulls 2
        # TODO(Keith): Make sure Character hasn't become incapacitated before their turn to act
        for battle_round_initiative in self.initiatives.all().order_by('-value'):
            action = self.actions.filter(actor=battle_round_initiative.character).first()
            action_function = getattr(action.actor, action.action)
            action_parameters = json.loads(action.parameters)
            action_data = action_function(**action_parameters)
            self.battle.emit_message({'step': 7, 'logs': action_data['logs']})

        return data
        
    """
    Step 8: Check for Random Item Damage
    """
    def check_for_random_item_damage(self):
        data = dict(logs=dict())
        #data['logs']['check_for_random_item_damage'] = "Not implemented"
        
        return data


    def end_round(self):
        data = dict()

        # TODO(Keith): Check if there is a need to create another round
        br = BattleRound.objects.create(battle=self.battle, round=self.round+1)
        data['new_battle_round_id'] = br.id

        django_rq.enqueue(br.start)
        
        return data


class BattleRoundAction(BaseSourceModel):
    battle_round    = models.ForeignKey(BattleRound, on_delete=models.DO_NOTHING, related_name="actions")
    actor           = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="actor_actions")
    # TODO(Keith)   : I'm not sure about this, should these be choices or a table pointer? (attack, cast, use, defend, etc)
    action          = models.CharField(max_length=100)
    # NOTE(Keith)   : The stringified parameters of the action (cast="Light", power_level=1, target_id=43), (item_id=123, target_id=22)
    parameters      = models.CharField(max_length=1000, default=None, null=True)

    class Meta:
        verbose_name = "Battle Round Action"
        verbose_name_plural = "Battle Round Actions"

    def __str__(self):
        return "{} - {}".format(self.actor, self.action)

def battle_round_action_post_save(sender, **kwargs):
    
    # NOTE(Keith): Check if this is the last action committed, if so, process the round
    battle_round = BattleRound.objects.filter(id=kwargs['instance'].battle_round_id).first()
    if not battle_round:
        the_battle_round_should_exists()
    
    battle_round.pending_actions -= 1
    battle_round.save(update_fields=['pending_actions'])
    if battle_round.pending_actions == 0:
        django_rq.enqueue(battle_round.process_round)
models.signals.post_save.connect(battle_round_action_post_save, sender=BattleRoundAction)

def battle_round_action_post_delete(sender, **kwargs):
    # NOTE(Keith): Adjust the pending count if an action is removed
    battle_round = BattleRound.objects.filter(id=kwargs['instance'].battle_round_id).first()
    if not battle_round:
        the_battle_round_should_exists()
    
    battle_round.pending_actions += 1
    battle_round.save(update_fields=['pending_actions'])
models.signals.post_delete.connect(battle_round_action_post_delete, sender=BattleRoundAction)


class BattleRoundInitiative(BaseSourceModel):
    battle_round    = models.ForeignKey(BattleRound, on_delete=models.DO_NOTHING, related_name="initiatives")
    character       = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="round_initiatives")
    value           = models.IntegerField()

    class Meta:
        verbose_name        = "Battle Round Initiative"
        verbose_name_plural = "Battle Round Initiatives"

    def __str__(self):
        return "{} - {}: {}".format(self.battle_round, self.character, self.value)


class BattleRoundLog(BaseSourceModel):
    battle_round    = models.ForeignKey(BattleRound, on_delete=models.DO_NOTHING, related_name="logs")
    actor           = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="actor_logs")
    action          = models.CharField(max_length=100, choices=BATTLE_ROUND_LOG_ACTIONS)
    target          = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name="target_logs")
    statement       = models.CharField(max_length=500)
    results         = models.CharField(max_length=1000)

    class Meta:
        verbose_name        = "Battle Round Log"
        verbose_name_plural = "Battle Round Logs"




def battle_round_character_post_save(sender, **kwargs):
    
    if not kwargs['instance'].current_battle or not kwargs['update_fields']:
        return

    # NOTE(Keith): If these fields update, alert the whole battle
    battle_update_fields = [
        'HP',               'health_status',
        'SP',               'stamina_status',
        'MHP',              'mental_health_status',
        'morale_status',    'stun_status', 
        'encumbrance_status'
    ]

    # NOTE(Keith): If these fields update, alert just the player
    self_update_fields = [
        '_cha', '_con', '_dex',
        '_int', '_str', '_wil',
        'skills'
    ]

    # NOTE(Keith): Values of updated fields grouped by character id
    battle_changed_fields = dict()

    # NOTE(Keith): Values of updated fields that only the character sees
    # TODO(Keith): Some kind of ability that allows characters to see this extra info
    self_changed_fields = dict()

    for field in kwargs['update_fields']:
        if field in battle_update_fields:
            battle_changed_fields[field] = getattr(kwargs['instance'], field)
        elif field in self_update_fields:
            self_changed_fields[field] = getattr(kwargs['instance'], field)
        
    # TODO(Keith): This logic will move when we queue up all the updates into one message
    # Note(Keith): If in a battle, send a message to update
    battle = kwargs['instance'].current_battle
    if battle_changed_fields:    
        battle_update_message = {
            'character_updates': {
                kwargs['instance'].id: battle_changed_fields
            }
        }
        battle.emit_message(battle_update_message)
    if self_changed_fields:
        self_update_message = {
            'self_updates': self_changed_fields
        }
        battle.emit_message(self_update_message, character_id=kwargs['instance'].id)        

models.signals.post_save.connect(battle_round_character_post_save, sender=Character)
