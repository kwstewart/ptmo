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
from dynamic_db_router import in_database

from models import *

class InitTutorialApi(APIView):

    def post(self, request, *args, **kwargs):
        slack_message = init_tutorial(request)
        return Response(slack_message)


class StartTutorialApi(APIView):

    def post(self, request, *args, **kwargs):
        slack_message = tutorial_intro()
        return Response(slack_message)


class SlackWebhookApi(APIView):

    def post(self, request, *args, **kwargs):
        if 'challenge' in request.data:
            return Response(dict(challenge=request.data['challenge']))
        if 'event' in request.data and 'type' in request.data['event']:
            import webhooks
            event_type = request.data['event']['type']
            if event_type == "team_join":
                return webhooks.team_join(request.data)

        return Response(dict())


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
        elif payload['actions'][0]['name'].startswith('start'):
            slack_message = tutorial_intro(request)
        elif payload['actions'][0]['name'].startswith('look'):
            slack_message = look(payload)
        else:
            slack_message = invalid_button(payload)
        return Response(slack_message)

def set_dynamic_db_config(user_id):
    db_config = dict(settings.DATABASES['default'])
    db_config['NAME'] = "ptmo_"+user_id
    return db_config

def init_tutorial(request):
    import subprocess
    from psycopg2 import connect
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    db_settings = settings.DATABASES['default']

    con = connect(
        dbname      = db_settings['NAME'], 
        user        = db_settings['USER'], 
        host        = db_settings['HOST'], 
        password    = db_settings['PASSWORD']
    )
    dbname = "{}_{}".format(db_settings['NAME'],request.data['user_id'])

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute('CREATE DATABASE ' + dbname)
    except:
        cur.execute('DROP DATABASE ' + dbname)
        cur.execute('CREATE DATABASE ' + dbname)
    
    # Import the level
    f = open('tutorial.sql', 'r')
    subprocess.call(
        "export PGPASSWORD='{}' ; /usr/lib64/pgsql95/bin/psql -h {} --username={} {} < tutorial.sql".format(
            db_settings['PASSWORD'], 
            db_settings['HOST'], 
            db_settings['USER'], 
            dbname.lower()
        ),
        shell = True
    )
    f.close()

    cur.close()
    con.close()
    
    user = UserPreference.objects.get(key='slack_user_id', value=request.data['user_id']).user
    up_q = UserPreference.objects.filter(user=user, key='tutorial_channel_id')
    if up_q.exists():
        channel = up_q[0].value
    else:
        sca = SlackClient(settings.ADMIN_TOKEN)

        resp = sca.api_call("groups.create",name="tutorial_"+request.data['user_id'])

        channel = resp['group']['id']

        UserPreference.objects.create(
            user    = user,
            key     = "tutorial_channel_id",
            value   = channel
        )

        resp = sca.api_call("groups.invite",channel=channel, user=settings.BOT_SLACK_USER_ID)
        resp = sca.api_call("groups.invite",channel=channel, user=request.data['user_id'])

    slack_message = dict(
        response_type   = "ephemeral",
        text            = "Your level has been generated.",
        attachments     = [
            dict(
                callback_id = "tutorial",
                text        = " ",
                actions     = [
                    dict(
                        name    = "start__tutorial",
                        type    = "button",
                        text    = "Begin",
                        value   = "true"
                    )
                ]
            )
        ]
    )
    return slack_message

def tutorial_intro(request):

    payload = json.loads(request.data['payload'])
    user = UserPreference.objects.filter(key='slack_user_id', value=payload['user']['id'])[0].user
    channel = UserPreference.objects.filter(user=user, key='tutorial_channel_id')[0].value
    
    # TODO: fix the channel link
    slack_message = dict(text="Head over to <#"+channel+"> Good luck")

    db_config = set_dynamic_db_config(payload['user']['id'].lower())

    with in_database(db_config):
        level = Level.objects.get(name='tutorial')

    new_slack_message = dict(
       channel     = channel,
        text        = level.text,
        attachments = [dict(
            text        = " ",
            callback_id = "tutorial",
            actions = [dict(
                name    = "room__tutorial_woods__blank__roadside",
                type    = "button",
                text    = "Let's go!",
                value   = "true"

            )]
        )]
    )
    sc = SlackClient(settings.BOT_TOKEN)
    sc.api_call("chat.postMessage",**new_slack_message)
    return slack_message


def invalid_button(payload):
    slack_message = dict(
        channel = payload['channel'],
        text = "nope"
    )
    return slack_message

def strip_actions(attachments, keep_text = False):
    stripped = []
    for attachment in attachments:
        if 'callback_id' in attachment:
            if keep_text and attachment['callback_id'] == 'keep_text':
                pass
            else:
                continue
        stripped.append(attachment)

    return stripped


def load_room(payload, location, dest_room_name, curr_room_name = None, new_room = True, history = []):

    if not history and 'original_message' in payload:
        history = strip_actions(payload['original_message']['attachments'])
    
    db_config = set_dynamic_db_config(payload['user']['id'].lower())

    with in_database(db_config):
        dr_q = Room.objects.filter(location__name=location, name=dest_room_name)

        if not dr_q.exists():
            return invalid_button(payload)

        dest_room = dr_q[0]

    
    if 'original_message' in payload:
        slack_message = payload['original_message']
        slack_message['attachments'] = strip_actions(payload['original_message']['attachments'], keep_text=True)
        slack_message['attachments'].append(
            dict(
                text        = "[:walking: *{}* ] ".format(dest_room.clean_name),
                color       = "#d6f5d6",
                mrkdwn_in   = ['text']
            )
        )
    else:
        slack_message = tutorial_intro()
        slack_message['attachments'].append(dict(text=' ', footer='Good luck'))
    
    with in_database(db_config):
        d_q = Door.objects.filter(curr_room=dest_room)
        ud_q = Door.objects.filter(curr_room=dest_room)
        uri_q = RoomItem.objects.filter(room=dest_room)
        iri_q = RoomItem.objects.filter(room=dest_room, inspected=True).exclude(button_text=None)

    
        new_slack_message = dict(
            channel     = payload['channel']['id'],
            text        = "~{border}~{line_break}*{title}*{line_break}~{border}~".format(
                title       = dest_room.clean_name, 
                border      = "-" * 40, 
                line_break  = "\n"
            ),
            attachments =[]
        )

        investigate_index = 1
        action_index = 2

        text_dict = dict(
            text            = dest_room.text,
            callback_id     = "keep_text"
        )
        if dest_room.image:
            text_dict['thumb_url'] = dest_room.image
        new_slack_message['attachments'].append(text_dict)

        new_slack_message['attachments'].append(
            dict(
                title       = "Investigate",
                callback_id = "slack_user_id",
                color       = "#66c2ff",
                actions     = [
                    dict(
                        name    = "look__{}__{}".format(location, dest_room),
                        type    = "select",
                        options = []
                    )
                ]
            )
        )
        new_slack_message['attachments'].append(
            dict(
                title       = "Act",
                color       = "#33cc33",
                callback_id = "slack_user_id",
                actions     = []
            )            
        )

        # TODO: Combine these into 1 array so we can alphabetize
        for room_item in uri_q:
            item_name = "item__{}__{}__{}".format(location, dest_room, room_item.item.name)
            item_dict = dict(
                text    = room_item.item.clean_name,
                value   = item_name
            )
            new_slack_message['attachments'][investigate_index]['actions'][0]['options'].append(item_dict)

        for door in ud_q:
            door_name = "door__{}__{}__{}".format(location, dest_room, door.dest_room.name)
            item_dict = dict(
                text    = door.button_text,
                value   = door_name
            )
            new_slack_message['attachments'][investigate_index]['actions'][0]['options'].append(item_dict)

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
            new_slack_message['attachments'][action_index]['actions'].append(door_dict)

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
            new_slack_message['attachments'][action_index]['actions'].append(item_dict)

    if new_room:
        sc = SlackClient(settings.BOT_TOKEN)
        sc.api_call("chat.postMessage",**new_slack_message)
        return slack_message

    else:
        new_slack_message['attachments'].extend(history)
        new_slack_message['attachments'].append(payload['original_message']['attachments'])
        return new_slack_message

def look(payload):

    room_parts = payload['actions'][0]['selected_options'][0]['value'].split("__")
    action = room_parts[0]
    location = room_parts[1]
    room = room_parts[2]
    item = room_parts[3]

    db_config = set_dynamic_db_config(payload['user']['id'].lower())

    if action == "item":
        with in_database(db_config, write=True):
            room_item = RoomItem.objects.get(room__name=room, item__name=item)
            room_item.inspected = True
            room_item.save()
        inspect_text = "[:eye: *{}* ] - {}".format(room_item.item.clean_name, room_item.item.inspect_text)
    elif action == "door":
        with in_database(db_config, write=True):
            door = Door.objects.get(curr_room__name=room, dest_room__name=item)
            door.inspected = True
            door.save()
        inspect_text = "[:eye: *{}* ] - {}".format(door.button_text, door.inspect_text)

    payload['original_message']['attachments'].append(
        dict(
            text        = inspect_text, 
            color       = "#ccebff",
            mrkdwn_in   = ['text']
        )
    )

    return load_room(payload, location, room, history=strip_actions(payload['original_message']['attachments']), new_room=False)



def open_item(payload):
    room_parts = payload['actions'][0]['name'].split("__")
    action = room_parts[0]
    location = room_parts[1]
    room = room_parts[2]
    target = room_parts[3]

    db_config = set_dynamic_db_config(payload['user']['id'].lower())

    with in_database(db_config):
        room_item = RoomItem.objects.get(room__name=room, item__name=target)
    
    if room_item.locked:
        payload['original_message']['attachments'].append(
            dict(
                text        = "[:no_entry_sign: *Open {}* ] - {}".format(room_item.item.clean_name, room_item.force_text),
                color       = "#ff9999",
                mrkdwn_in   = ['text']
            )
        )
    
    return load_room(payload, location, room, history=strip_actions(payload['original_message']['attachments']), new_room=False)