from django.db import models
from account.models import CustomUser


class Attribute(models.Model):
    name = models.CharField(max_length=20)


class Item(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	created_by = models.ForeignKey(CustomUser)