# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core import pubsub
from django.apps import AppConfig
from myfarog.events import MyfarogEvents


class MyfarogConfig(AppConfig):
    name = 'myfarog'

    def ready(self):
        pubsub.listen(MyfarogEvents.CHARACTER_CHANGE, inform_battle)