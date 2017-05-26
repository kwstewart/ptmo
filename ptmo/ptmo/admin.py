from django.contrib import admin

from models import *


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slack_channel')
    search_fields = ['name']
    save_as = True

admin.site.register(Location, LocationAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('location', 'name', 'text')
    search_fields = ['name']
    save_as = True
admin.site.register(Room, RoomAdmin)


class DoorAdmin(admin.ModelAdmin):
    list_display = ('curr_room', 'dest_room', 'text','locked')
    search_fields = ['name']
    save_as = True
admin.site.register(Door, DoorAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('curr_room', 'name', 'text','locked')
    search_fields = ['name']
    save_as = True
admin.site.register(Item, ItemAdmin)