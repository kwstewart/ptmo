import math
from rest_framework import serializers, response
from myfarog.models import (
    Skill
)
from myfarog.battle import (
    Battle,
    BattleRound,
    BattleRoundAction
)
from myfarog.character import (
    Character,
    CharacterCut,
    CharacterSkill,
    CharacterTalent,
    Skill
)

class BattleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Battle
        fields = ['name', 'parties', 'rounds']


class BattleRoundSerializer(serializers.ModelSerializer):

    class Meta:
        model = BattleRound
        fields = '__all__'


class BattleRoundActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BattleRoundAction
        fields = '__all__'


class CharacterSkillSerializer(serializers.ModelSerializer):

    skill_name = serializers.SerializerMethodField()
    skill_mod = serializers.SerializerMethodField()

    def get_skill_name(self, obj):
        return obj.skill.name

    def get_skill_mod(self, obj):
        #char = CharacterSerializer(obj.character).data
        
        return 0

    class Meta:
        model = CharacterSkill
        fields = ('skill_id', 'skill_name', 'skill_mod', 'trained', 'role_skill')


class CharacterTalentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacterTalent
        fields = '__all__'


class CharacterCutSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacterCut
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):

    talents = serializers.SerializerMethodField()
    role    = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    cuts    = serializers.SerializerMethodField()


    def get_role(self, obj):
        return obj.role.name

    def get_species(self, obj):
        return obj.species.name

    def get_talents(self, obj):
        return obj.talents.values_list('talent__name', flat=True)

    def get_cuts(self, obj):
        return CharacterCutSerializer(CharacterCut.objects.filter(character=obj), many=True).data

    class Meta:
        model = Character
        fields = (
            'id', 'user', 'name', 'gender', 'species', 'role', 
            'exp', 'level', 'age', 'height', 'weight', 'size',
            'CON', 'CHA', 'DEX', 'INT', 'STR', 'WIL',
            '_con', '_cha', '_dex', '_int', '_str', '_wil',
            'HP', 'SP', 'MHP', 'max_HP', 'max_SP', 'max_MHP',
            'psychotic_count', 'fright_mod', 'trauma_count',
            'morale_rounds', 'morale_check_bonus', 'morale_status',
            'encumbrance_status', 'encumbrance_mod', 'health_status',
            'health_mod', 'mental_health_status', 'mental_health_mod',
            'stamina_status', 'stamina_mod', 'initiative_check_bonus',
            'OV_melee', 'OV_missile', 'DV_melee', 'DV_missile',
            'skills', 'talents', 'cuts'

        )
        

class CharacterVerboseSerializer(CharacterSerializer):

    class Meta:
        model = Character
        fields = CharacterSerializer.Meta.fields + ('logs',)