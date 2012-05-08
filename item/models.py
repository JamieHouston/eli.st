from django.db import models
from django.contrib.auth.models import User
from timeDeltaField import TimedeltaField


class Attribute(models.Model):
    name = models.CharField(max_length=20)
    datatype = models.CharField(max_length=20)


class Item(models.Model):
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=255)
    created_by = models.ForeignKey(User)
    attributes = models.ManyToManyField(Attribute, through='ItemAttribute')

    def __unicode__(self):
        return self.name

    def add_attribute(self, attribute, value):
        dbAttribute, created = Attribute.objects.get_or_create(name=attribute)
        item_attribute = ItemAttribute(attribute=dbAttribute, value=value, item=self)
        item_attribute.save()

    def get_attributes(self):
        return self.attributes


class ItemAttribute(models.Model):
    attribute = models.ForeignKey(Attribute)
    item = models.ForeignKey(Item)
    value = models.CharField(max_length=50)

    def __unicode__(self):
        if self.attribute.datatype == "DATE":
            return "on " + self.value


class WhenCommand(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    recurring = TimedeltaField(blank=True)


class ItemCommand(models.Model):
    item = models.ForeignKey(Item)
    who = models.CharField(max_length=50)
    what = models.CharField(max_length=50)
    where = models.CharField(max_length=50)
    when = models.ForeignKey(WhenCommand)
    #attributes = models.ManyToManyField(Attribute, through='ItemAttribute')
