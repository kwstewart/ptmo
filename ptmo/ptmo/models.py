from django.db import models

class Location(models.Model):
    name                = models.CharField(max_length=64)
    slack_channel   =  models.CharField(max_length=16)
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Room(models.Model):
    location    = models.ForeignKey(Location)
    name                = models.CharField(max_length=64)
    text               = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class Door(models.Model):
    curr_room    = models.ForeignKey(Room, related_name="current_room")
    dest_room    = models.ForeignKey(Room, related_name="destination_room")
    name                = models.CharField(max_length=64)
    text                = models.CharField(max_length=16)
    locked      = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Door"
        verbose_name_plural = "Doors"


class Item(models.Model):
    curr_room    = models.ForeignKey(Room)
    name                = models.CharField(max_length=64)
    text                = models.CharField(max_length=16)
    locked      = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


