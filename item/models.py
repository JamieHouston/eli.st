from django.db import models
from account.models import CustomUser


class Attribute(models.Model):
    name = models.CharField(max_length=20)


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser)
    attributes = models.ManyToManyField(Attribute, through='ItemAttribute')

    def add_attribute(self, attribute, value):
        item_attribute = ItemAttribute(attribute=attribute, value=value, item=self)
        item_attribute.save()


class ItemAttribute(models.Model):
    attribute = models.ForeignKey(Attribute)
    item = models.ForeignKey(Item)
    value = models.CharField(max_length=50)
