"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from item.models import Attribute, Item
from account.models import CustomUser


class SimpleTest(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ItemTests(unittest.TestCase):
    def test_user_can_have_items(self):
        user = CustomUser(username="user1")
        user.save()

        item1 = Item(name="item 1", created_by=user)
        item1.save()
        item2 = Item(name="item 2", created_by=user)
        item2.save()

        self.assertEqual(user.item_set.count(), 2)


class ItemAttributeTest(unittest.TestCase):
    def test_item_can_have_attribute(self):
        user = CustomUser(username="user1")
        user.save()

        item = Item(name="item 1", created_by=user)
        item.save()

        attribute = Attribute(name="tag")
        attribute.save()

        item.add_attribute(attribute, value="important")
        item.save()

        self.assertEqual(item.itemattribute_set.count(), 1)
        self.assertEqual(item.itemattribute_set.all()[0].value, "important")
