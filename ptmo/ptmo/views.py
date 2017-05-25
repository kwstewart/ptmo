import datetime
import pytz
import requests
import json
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from urllib import urlencode
from slackclient import SlackClient

class SlackButtonApi(APIView):

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.data['payload'])
        if payload['actions'][0]['name'].startswith('room'):
            slack_message = load_room(payload)
        elif payload['actions'][0]['name'].startswith('item'):
            slack_message = load_item(payload)
        else:
            slack_message = invalid_button(payload)
        return Response(slack_message)



def invalid_button(payload):
    slack_message = dict(
        channel = payload['channel'],
        text = "nope"
    )
    return slack_message

def load_room(payload):
    room_parts = payload['actions'][0]['name'].split("__")
    action = room_parts[0]
    location = room_parts[1]
    current_room = room_parts[2]
    target = room_parts[3]
    if target == "ballroom":
        slack_message = payload['original_message']
        slack_message['attachments'][0]['actions']=[]
        slack_message['attachments'].append(dict(text=" ",footer=target))
        new_slack_message = dict(
            channel=payload['channel']['id'],
            text="You enter a large ballroom with tapestry lined walls, yada yada, *large chest* on west wall below yada yada, blah blah.\n\nA door to the West heads to the *Hall Door*.  Behind the stage to the North a *Musician's Closet Door* can be seen.",
            attachments=[dict(
                text="What do you do?",
                callback_id="email",
                actions=[
                    dict(
                        name="room__manor__ballroom__hallway",
                        type="button",
                        text="Hallway Door",
                        value=True
                    ),
                    dict(
                        name="room__manor__ballroom__musicans_closet",
                        type="button",
                        text="Musician's closet",
                        value=True
                    ),
                    dict(
                        name="item__manor__ballroom__chest",
                        type="button",
                        text="Open Chest",
                        value=True
                    )
                ]
            )]
        )
    elif target == "musicans_closet":
        slack_message = payload['original_message']
        slack_message['attachments'][0]['actions']=[]
        slack_message['attachments'].append(dict(text=" ",footer=target))
        new_slack_message = dict(
            channel=payload['channel']['id'],
            text="Oh shit!  There are skeletons in the closet",
            attachments=[dict(
                text="What do you do?",
                callback_id="email",
                actions=[
                    dict(
                        name="room__manor__musicans_closet__ballroom",
                        type="button",
                        text="Ballroom",
                        value=True
                    )
                ]
            )]
        )
    sc = SlackClient(settings.bot_token)
    sc.api_call("chat.postMessage",**new_slack_message)
    return slack_message

def load_item(payload):
    room_parts = payload['actions'][0]['name'].split("__")
    action = room_parts[0]
    location = room_parts[1]
    current_room = room_parts[2]
    target = room_parts[3]
    if current_room == "ballroom":
        if target == "chest":
            slack_message = payload['original_message']
            slack_message['attachments'][0]['actions'][2]['style']='danger'
            slack_message['attachments'][0]['actions'][2]['confirm']={"title":"You can't do that","text":"The chest is locked.","ok_text":"Try again","dismiss_text":"Got it"}
            slack_message['attachments'].append(dict(text=" ",footer="Open Chest - The chest is locked"))
    return slack_message