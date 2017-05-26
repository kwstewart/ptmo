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

from models import *

class StartTutorialApi(APIView):

    def post(self, request, *args, **kwargs):
        command = request.data['text']

        slack_message = dict(
            channel     = "#tutorial",
            text        = "Let's get started!",
            attachments = [dict(
                callback_id = "tutorial",
                actions = [dict(
                    name    = "room__tutorial__blank__roadside",
                    type    = "button",
                    text    = "Start",
                    value   = "true"

                )]
            )]
        )
        return Response(slack_message)



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
    cr = room_parts[2]
    dr = room_parts[3]

    cr_q = Room.objects.filter(location__name=location, name=cr)

    dr_q = Room.objects.filter(location__name=location, name=dr)

    if not dr_q.exists():
        return invalid_button(payload)

    dest_room = dr_q[0]

    if cr_q.exists():
        slack_message = payload['original_message']
        slack_message['attachments'] = []
        slack_message['attachments'].append(dict(text=" ",footer="-> "+dest_room.clean_name))
    else:
        slack_message = dict(text="Good luck!")

    d_q = Door.objects.filter(curr_room=dest_room)
    uri_q = RoomItem.objects.filter(room=dest_room, inspected=False)    
    iri_q = RoomItem.objects.filter(room=dest_room, inspected=True).exclude(button_text=None)

    
    new_slack_message = dict(
        channel     = payload['channel']['id'],
        text        = dest_room.text,
        attachments =[
            dict(
                title       = "Investigate",
                callback_id = "slack_user_id",
                actions     = [
                    dict(
                        name    = "look__{}__{}".format(location, dest_room),
                        type    = "select",
                        options = []
                    )
                ]
            ),
            dict(
                text        = " ",
                callback_id = "slack_user_id",
                actions     = []
            )
        ]
    )

    for room_item in uri_q:
        item_name = "item__{}__{}__{}".format(location, dest_room, room_item.item.name)
        item_dict = dict(
            text    = room_item.item.name,
            value   = item_name
        )
        new_slack_message['attachments'][0]['actions'][0]['options'].append(item_dict)

    for door in d_q:
        door_name = "room__{}__{}__{}".format(location, dest_room, door.dest_room.name)
        item_dict = dict(
            text    = door.button_text,
            value   = door_name
        )
        new_slack_message['attachments'][0]['actions'][0]['options'].append(item_dict)

    for door in d_q:
        door_name = "room__{}__{}__{}".format(location, dest_room, door.dest_room.name)
        door_dict = dict(
            name    = door_name,
            type    = "button",
            text    = door.button_text,
            value   = True
        )
        if door.locked and door.attempted:
            door_dict['style'] = 'danger'
            door_dict['confirm'] = dict(
                title           = "You can't do that",
                text            = door.lock_text,
                ok_text         = "Try again",
                dismiss_text    = "Got it"
            )
        new_slack_message['attachments'][1]['actions'].append(door_dict)

    for room_item in iri_q:
        item_name = "item__{}__{}__{}".format(location, dest_room, room_item.item.name)
        item_dict = dict(
            name    = item_name,
            type    = "button",
            text    = room_item.button_text,
            value   = True
        )

        if room_item.locked and room_item.inspected:
            item_dict['style'] = 'danger'
            item_dict['confirm'] = dict(
                title           = "You can't do that",
                text            = room_item.lock_text,
                ok_text         = "Try again",
                dismiss_text    = "Got it"
            )
        new_slack_message['attachments'][1]['actions'].append(item_dict)

    sc = SlackClient(settings.BOT_TOKEN)
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