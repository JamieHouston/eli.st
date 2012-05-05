"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from item.models import Attribute, Item
from django.contrib.auth.models import User


def setUp(self):
    self.user = User(username="user1")
    self.user.save()


class ItemTests(unittest.TestCase):
    def test_user_can_have_items(self):

        item1 = Item(name="item 1", created_by=self.user)
        item1.save()
        item2 = Item(name="item 2", created_by=self.user)
        item2.save()

        self.assertEqual(self.user.item_set.count(), 2)


class ItemAttributeTest(unittest.TestCase):
    def test_item_can_have_attribute(self):
        item = Item(name="item 1", created_by=self.user)
        item.save()

        item.add_attribute(attribute="priority", value="important")
        item.save()

        self.assertEqual(item.itemattribute_set.count(), 1)
        self.assertEqual(item.itemattribute_set.all()[0].value, "important")
