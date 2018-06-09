# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


from source_framework.core.utils.view import (
    filter_from_dict, get_limit_offset,
    source_login, source_logout, source_authenticate,
    SourceResponse, SourceResponse400, SourceResponse401,
    SourceResponse403, SourceResponse404, SourceResponse422,
    SourceResponse500
)

from myfarog.models import *
from myfarog.serializers import *

# Create your views here.
class CharacterView(APIView):

    def get(self, request, *args, **kwargs):
        """
        If no pk is passed in the URL, a filtered list is returned
        Otherwise the record of the request id is returned
        """
        model = Character
        serializer = CharacterSerializer

        data_dict = request.GET.dict()
        if 'verbose' in data_dict:
            serializer = CharacterVerboseSerializer
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