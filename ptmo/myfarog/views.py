# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework.response import Response
from rest_framework.views import APIView


from source_framework.core import (
    filter_from_dict, get_limit_offset,
    source_login, source_logout, source_authenticate,
    SourceResponse, SourceResponse400, SourceResponse401,
    SourceResponse403, SourceResponse404, SourceResponse422,
    SourceResponse500
)

from myfarog.models import *
from myfarog.serializers import *

# Create your views here.
class CharacterApi(APIView):

    def get(self, request, *args, **kwargs):
        """
        If no pk is passed in the URL, a filtered list is returned
        Otherwise the record of the request id is returned
        """
        model = Character
        serializer = CharacterSerializer
        verbose_serializer = CharacterVerboseSerializer

        data_dict = request.GET.dict()
        if 'verbose' in data_dict and verbose_serializer:
            serializer = verbose_serializer
        if 'pk' in kwargs:
            data_dict['id'] = kwargs['pk']
            
        limit, offset = get_limit_offset(request)
        q_filter = filter_from_dict(model, data_dict)
        _q = model.objects.filter(q_filter)
        total = _q.count()
        _q = _q.paginate(limit=limit, offset=offset)
        data = serializer(_q, many=True).data
        
        from django.db import connection
        print(connection.queries)
        
        return SourceResponse(
            data,
            limit   = limit,
            offset  = offset,
            total   = total,
            count   = _q.count()
        )

    def post(self, request, *args, **kwargs):
        """
        If no pk is passed in the URL, a new record is created
        Otherwise the record of the request id is updated
        """
        # TODO(Keith): Implement permission checks
        if 'pk' in kwargs:
            character = Character.objects.filter(id=kwargs['pk']).first()
            if character:
                # TODO(Keith): Add validation
                #valid_data = validation(request.data)
                valid_data = request.data
                character.update_from_dict(valid_data)
                
            else:
                return SourceResponse404()
        else:
            # TODO(Keith): Implement permission checks
            # Replace with validation
            character_data = dict()
            
            # TODO(Keith): Random stat assignment if not passed
            hey_set_up_this_function_so_we_can_use_it()
            character = Character.objects.create(**character_data)
            character.save()

        character_q = Character.objects.filter(id=character.id)
        
        data = CharacterSerializer(character_q, many=True).data
        return Response(data)


class BattleApi(APIView):

    def get(self, request, *args, **kwargs):
        """
        If no pk is passed in the URL, a filtered list is returned
        Otherwise the record of the request id is returned
        """
        model = Battle
        serializer = BattleSerializer
        verbose_serializer = None

        data_dict = request.GET.dict()
        if 'verbose' in data_dict and verbose_serializer:
            serializer = verbose_serializer
        if 'pk' in kwargs:
            data_dict['id'] = kwargs['pk']
        limit, offset = get_limit_offset(request)
        q_filter = filter_from_dict(model, data_dict)
        _q = model.objects.filter(q_filter)
        total = _q.count()
        _q = _q.paginate(limit=limit, offset=offset)
        data = serializer(_q, many=True).data
        
        from django.db import connection
        print(connection.queries)
        
        return SourceResponse(
            data,
            limit   = limit,
            offset  = offset,
            total   = total,
            count   = _q.count()
        )

    def post(self, request, *args, **kwargs):
        """
        If no pk is passed in the URL, a new record is created
        Otherwise the record of the request id is updated
        """
        # TODO(Keith): Implement permission checks
        if 'pk' in kwargs:
            battle = Battle.objects.filter(id=kwargs['pk']).first()
            if battle:
                # TODO(Keith): Add validation
                #valid_data = validation(request.data)
                valid_data = request.data
                battle.update_from_dict(valid_data)
                
            else:
                return SourceResponse404()
        else:
            # TODO(Keith): Implement permission checks
            # Replace with validation
            battle_data = dict()
            
            if 'name' in request.data:
                battle_data['name'] = request.name
            if 'parties' in request.data:
                add_parties_from_a_list_of_ids()

            battle = Battle.objects.create(**battle_data)
            battle.save()

        battle_q = Battle.objects.filter(id=battle.id)
        
        data = BattleSerializer(character_q, many=True).data
        return Response(data)


def BattleView(request):

    battle = Battle.objects.filter(id=1).first()
    character = Character.objects.filter(id=1).first()

    template = loader.get_template('battle.html')
    context = dict(
        character = character,
        battle =dict(
            id      = battle.id,
            name    = battle.name,
            round   = battle.rounds.last().round,
            parties = [
                dict(
                    name=party.name, 
                    characters=party.characters.exclude(id=character.id)
                ) for party in battle.parties.all()
            ],
        ),
        test="hey yo"
    )
    return HttpResponse(template.render(context, request))


class BattleRoundApi(APIView):

    def get(self, request, *args, **kwargs):
        """
        If no pk is passed in the URL, a filtered list is returned
        Otherwise the record of the request id is returned
        """
        model = BattleRound
        serializer = BattleRoundSerializer
        verbose_serializer = None

        data_dict = request.GET.dict()
        if 'verbose' in data_dict and verbose_serializer:
            serializer = verbose_serializer
        
        if 'battle_id' in kwargs:
            data_dict['battle'] = kwargs['battle_id']

        if 'round' in kwargs:
            data_dict['round'] = kwargs['round']
        
        limit, offset = get_limit_offset(request)
        q_filter = filter_from_dict(model, data_dict)
        _q = model.objects.filter(q_filter)
        total = _q.count()
        _q = _q.paginate(limit=limit, offset=offset)
        data = serializer(_q, many=True).data
        
        from django.db import connection
        print(connection.queries)
        
        return SourceResponse(
            data,
            limit   = limit,
            offset  = offset,
            total   = total,
            count   = _q.count()
        )


class BattleRoundActionApi(APIView):

    def post(self, request, *args, **kwargs):
        """
        If no pk is passed in the URL, a new record is created
        Otherwise the record of the request id is updated
        """
        battle_round = BattleRound.objects.filter(battle_id=kwargs['battle_id'], round=kwargs['round']).first()
        if not battle_round:
            return SourceResponse404()

        # TODO(Keith): Make sure the request.user has access to this char
        # TODO(Keith): We should actually get this from a cookie or header
        character_id = request.data.get('character_id', None)
        if not character_id:
            return SourceResponse400("Invalid character_id")
        character = Character.objects.get(id=character_id)

        action = request.data.get('action', None)
        if not action:
            return SourceResponse400("Invalid action")
        
        log = character.declare_action(battle_round=battle_round, **request.data)
        return Response(dict(success=True, log=log))


