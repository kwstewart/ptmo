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

        slack_message = tutorial_intro()
        return Response(slack_message)


class SlackButtonApi(APIView):

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.data['payload'])
        if payload['actions'][0]['name'].startswith('room'):
            room_parts = payload['actions'][0]['name'].split("__")
            action = room_parts[0]
            location = room_parts[1]
            curr_room_name = room_parts[2]
            dest_room_name = room_parts[3]            
            slack_message = load_room(payload, location, dest_room_name, curr_room_name)
        elif payload['actions'][0]['name'].startswith('item'):
            slack_message = open_item(payload)
        elif payload['actions'][0]['name'].startswith('look'):
            slack_message = look(payload)
        else:
            slack_message = invalid_button(payload)
        return Response(slack_message)


def tutorial_intro():

    level = Level.objects.get(name='tutorial')
    slack_message = dict(
        channel     = "#tutorial",
        text        = level.text,
        attachments = [dict(
            callback_id = "tutorial",
            actions = [dict(
                name    = "room__tutorial_woods__blank__roadside",
                type    = "button",
                text    = "Start",
                value   = "true"

            )]
        )]
    )
    return slack_message


def invalid_button(payload):
    slack_message = dict(
        channel = payload['channel'],
        text = "nope"
    )
    return slack_message

def strip_actions(attachments):
    stripped = []
    for attachment in attachments:
        if 'callback_id' in attachment:
            continue
        stripped.append(attachment)

    return stripped


def load_room(payload, location, dest_room_name, curr_room_name = None, new_room = True, history = []):

    if not history and 'original_message' in payload:
        history = strip_actions(payload['original_message']['attachments'])

    cr_q = Room.objects.filter(location__name=location, name=curr_room_name)

    dr_q = Room.objects.filter(location__name=location, name=dest_room_name)

    if not dr_q.exists():
        return invalid_button(payload)

    dest_room = dr_q[0]

    
    if 'original_message' in payload:
        slack_message = payload['original_message']
        slack_message['attachments'] = strip_actions(payload['original_message']['attachments'])
        slack_message['attachments'].append(dict(text=" ",footer="GO -> "+dest_room.clean_name))
    else:
        slack_message = tutorial_intro()
        slack_message['attachments'].append(dict(text=' ', footer='Good luck'))
    
    d_q = Door.objects.filter(curr_room=dest_room)
    ud_q = Door.objects.filter(curr_room=dest_room)
    uri_q = RoomItem.objects.filter(room=dest_room)
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
                title       = "Act",
                callback_id = "slack_user_id",
                actions     = []
            )
        ]
    )

    # TODO: Combine these into 1 array so we can alphabetize
    for room_item in uri_q:
        item_name = "item__{}__{}__{}".format(location, dest_room, room_item.item.name)
        item_dict = dict(
            text    = room_item.item.name,
            value   = item_name
        )
        new_slack_message['attachments'][0]['actions'][0]['options'].append(item_dict)

    for door in ud_q:
        door_name = "door__{}__{}__{}".format(location, dest_room, door.dest_room.name)
        item_dict = dict(
            text    = door.button_text,
            value   = door_name
        )
        new_slack_message['attachments'][0]['actions'][0]['options'].append(item_dict)

    # TODO: Combine these into 1 array so we can alphabetize
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

    if new_room:
        sc = SlackClient(settings.BOT_TOKEN)
        sc.api_call("chat.postMessage",**new_slack_message)
        return slack_message

    else:
        for hist in history:
            new_slack_message['attachments'].append(hist)
        new_slack_message['attachments'].append(payload['original_message']['attachments'])
        return new_slack_message

def look(payload):

    room_parts = payload['actions'][0]['selected_options'][0]['value'].split("__")
    action = room_parts[0]
    location = room_parts[1]
    room = room_parts[2]
    item = room_parts[3]

    if action == "item":
        room_item = RoomItem.objects.get(room__name=room, item__name=item)
        room_item.inspected = True
        room_item.save()
        inspect_text = "{}? - {}".format(room_item.item.name, room_item.item.inspect_text)
    elif action == "door":
        door = Door.objects.get(curr_room__name=room, dest_room__name=item)
        door.inspected = True
        door.save()
        inspect_text = "{}? - {}".format(door.button_text, door.inspect_text)

    payload['original_message']['attachments'].append(dict(text=" ", footer=inspect_text, mrkdwn_in=["text","footer"]))

    return load_room(payload, location, room, history=strip_actions(payload['original_message']['attachments']), new_room=False)



def open_item(payload):
    room_parts = payload['actions'][0]['name'].split("__")
    action = room_parts[0]
    location = room_parts[1]
    room = room_parts[2]
    target = room_parts[3]

    room_item = RoomItem.objects.get(room__name=room, item__name=target)
    
    payload['original_message']['attachments'].append(dict(text=" ",footer="Open {} - {}".format(room_item.item.name, room_item.force_text)))
    
    return load_room(payload, location, room, history=strip_actions(payload['original_message']['attachments']), new_room=False)