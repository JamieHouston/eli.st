import pdb
from django.db import models
from django.contrib.auth.models import User
#from timeDeltaField import TimedeltaField


# class Attribute(models.Model):
#     name = models.CharField(max_length=20)
#     datatype = models.CharField(max_length=20)


# class Item(models.Model):
#     name = models.CharField(max_length=50)
#     details = models.CharField(max_length=255)
#     created_by = models.ForeignKey(User)
#     attributes = models.ManyToManyField(Attribute, through='ItemAttribute')

#     def __unicode__(self):
#         return self.name

#     def add_attribute(self, attribute, value):
#         dbAttribute, created = Attribute.objects.get_or_create(name=attribute)
#         item_attribute = ItemAttribute(attribute=dbAttribute, value=value, item=self)
#         item_attribute.save()

#     def get_attributes(self):
#         return self.attributes


# class ItemAttribute(models.Model):
#     attribute = models.ForeignKey(Attribute)
#     item = models.ForeignKey(Item)
#     value = models.CharField(max_length=50)

#     def __unicode__(self):
#         if self.attribute.datatype == "DATE":
#             return "on " + self.value


class WhatCommand(models.Model):
    item = models.CharField(max_length=255, blank=True, null=True)
    list = models.CharField(max_length=100, blank=True, null=True)


class WhoCommand(models.Model):
    person = models.CharField(max_length=100, blank=True, null=True)


class WhereCommand(models.Model):
    location = models.CharField(max_length=255, blank=True, null=True)


class WhenCommand(models.Model):
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    recurrence = models.CharField(max_length=100, blank=True, null=True)
    #recurring = TimedeltaField(blank=True)


class UserCommand(models.Model):
    user = models.ForeignKey(User, null=True)
    original_command = models.CharField(max_length=1000)
    what = models.ForeignKey(WhatCommand, blank=True, null=True)
    who = models.ForeignKey(WhoCommand, blank=True, null=True)
    when = models.ForeignKey(WhenCommand, blank=True, null=True)

    def convert_from(self, command_dictionary):
        for key in command_dictionary.keys():
            #if hasattr(self, key):
            #    self[key] = 
            if key == "what":
                what = WhatCommand()
                what.item = command_dictionary[key].get("item", None)
                what.list = command_dictionary[key].get("list", None)
                what.save()
                self.what = what
            elif key == "when":
                when = WhenCommand()
                when.start_date = command_dictionary[key].get("start_date", None)
                when.start_time = command_dictionary[key].get("start_time", None)
                when.end_date = command_dictionary[key].get("end_date", None)
                when.save()
                self.when = when
                #self.when = WhenCommand(command_dictionary[key])
            elif key =="where":
                where = WhereCommand()
                where.location = command_dictionary[key].get("location", None)
                where.save()
                self.where = where
                #self.where = WhereCommand(command_dictionary[key])
            elif key == "who":
                who = WhoCommand()
                who.person = command_dictionary[key].get("person", None)
                who.save()
                self.who = who
                #self.who = WhoCommand(command_dictionary[key])
