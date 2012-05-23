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
            class_name = key.capitalize() + "Command"
            if class_name in globals():
                obj = globals()[class_name]()
                for val in command_dictionary[key].iterkeys():
                    if hasattr(obj, val):
                        setattr(obj, val, command_dictionary[key][val])
                obj.save()
                setattr(self, key, obj)