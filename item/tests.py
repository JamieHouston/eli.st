"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from item.models import Attribute, Item
from django.contrib.auth.models import User


class ItemTests(unittest.TestCase):
    def setUp(self):
        self.user = User(username="user1")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_user_can_have_items(self):

        item1 = Item(name="item 1", created_by=self.user)
        item1.save()
        item2 = Item(name="item 2", created_by=self.user)
        item2.save()

        self.assertEqual(self.user.item_set.count(), 2)


class ItemAttributeTest(unittest.TestCase):
    def setUp(self):
        self.user = User(username="user1")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_item_can_have_attribute(self):
        item = Item(name="item 1", created_by=self.user)
        item.save()

        item.add_attribute("priority", "important")
        item.save()

        self.assertEqual(item.itemattribute_set.count(), 1)
        self.assertEqual(item.itemattribute_set.all()[0].value, "important")

    def test_get_item_with_attribute(self):
        attribute = Attribute.objects.create(name="attribute 1")

        item = Item(name="item 1", created_by=self.user)
        item.save()

        item.add_attribute(attribute.name, "value 1")

        dbItem = attribute.item_set.all().get(pk=item.pk)
        self.assertEqual(dbItem.pk, item.pk)
