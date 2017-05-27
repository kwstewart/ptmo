from django.contrib.auth.models import User
from .models import UserPreference
from rest_framework.response import Response

def team_join(data):
    user = User.objects.create_user(
        username    = data['event']['user']['name'], 
        email       = data['event']['user']['profile']['email'],
        password    = data['token']
    )
    UserPreference.objects.create(
        user    = user,
        key     = "slack_user_id",
        value   = data['event']['user']['id']
    )
    return Response(dict(success=True))