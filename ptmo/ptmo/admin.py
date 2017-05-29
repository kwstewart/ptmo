from django.contrib import admin

from models import *


class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'value')
    search_fields = ['user', 'key', 'value']
    save_as = True

admin.site.register(UserPreference, UserPreferenceAdmin)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')
    search_fields = ['name']
    save_as = True

admin.site.register(Level, LevelAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'slack_channel')
    search_fields = ['name', 'level']
    save_as = True

admin.site.register(Location, LocationAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('clean_name', 'location', 'name', 'text')
    search_fields = ['clean_name', 'name']
    save_as = True

admin.site.register(Room, RoomAdmin)


class DoorAdmin(admin.ModelAdmin):
    list_display = ('button_text', 'curr_room', 'dest_room', 'inspect_text')
    search_fields = ['button_text', 'curr_room', 'dest_room']
    save_as = True
admin.site.register(Door, DoorAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('clean_name', 'name', 'inspect_text', 'obtainable')
    search_fields = ['name','clean_name','inspect_text']
    save_as = True
admin.site.register(Item, ItemAdmin)


class RoomItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'room')
    search_fields = ['room','item']
    save_as = True
admin.site.register(RoomItem, RoomItemAdmin)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')
    search_fields = ['user','item']
    save_as = True
admin.site.register(Inventory, InventoryAdmin)