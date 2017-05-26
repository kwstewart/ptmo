from django.db import models
from django.contrib.auth.models import User

# https://stackoverflow.com/questions/27401779/dynamically-set-database-based-on-request-in-django

class Level(models.Model):
    name = models.CharField(max_length=16)
    text = models.TextField()

    class Meta:
        verbose_name = "Level"
        verbose_name_plural = "Levels"

    def __unicode__(self):
        return '%s' % (self.name)

class Location(models.Model):
    level           = models.ForeignKey(Level)
    name            = models.CharField(max_length=64)
    slack_channel   = models.CharField(max_length=16)
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __unicode__(self):
        return '%s' % (self.name)


class Room(models.Model):
    location    = models.ForeignKey(Location)
    name        = models.CharField(max_length=64)
    clean_name  = models.CharField(max_length=64, blank=True, null=True)
    text        = models.TextField()
    
    class Meta:
        verbose_name        = "Room"
        verbose_name_plural = "Rooms"

    def __unicode__(self):
        return '%s' % (self.name)


class Door(models.Model):
    curr_room       = models.ForeignKey(Room, related_name="current_room")
    dest_room       = models.ForeignKey(Room, related_name="destination_room")
    button_text     = models.CharField(max_length=16)
    inspect_text    = models.TextField()
    attempted       = models.BooleanField(default=False)
    locked          = models.BooleanField(default=False)
    lock_text       = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name        = "Door"
        verbose_name_plural = "Doors"

    def __unicode__(self):
        return '%s' % (self.text)

class Item(models.Model):
    name            = models.CharField(max_length=16)
    inspect_text    = models.TextField()
    obtainable      = models.BooleanField(default=False)

    class Meta:
        verbose_name        = "Item"
        verbose_name_plural = "Items"

    def __unicode__(self):
        return '%s' % (self.name)


class RoomItem(models.Model):
    room        = models.ForeignKey(Room)
    item        = models.ForeignKey(Item)
    button_text = models.CharField(max_length=16, null=True, blank=True)
    inspected   = models.BooleanField(default=False)
    attempted   = models.BooleanField(default=False)
    locked      = models.BooleanField(default=False)
    lock_text   = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name        = "RoomItem"
        verbose_name_plural = "RoomItems"


class Inventory(models.Model):
    user    =  models.ForeignKey(User)
    item    =  models.ForeignKey(Item)

    class Meta:
        verbose_name        = "Inventory"
        verbose_name_plural = "Inventory"

