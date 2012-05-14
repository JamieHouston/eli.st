from django.utils import unittest
from item.models import Attribute, Item
from django.contrib.auth.models import User
import datetime
from utils import nlp, transform
import pdb


class UserTests(unittest.TestCase):
    def setUp(self):
        self.user = User(username="user1")
        self.user.save()

    def tearDown(self):
        self.user.delete()


class ItemTests(UserTests):
    def test_user_can_have_items(self):

        item1 = Item(name="item 1", created_by=self.user)
        item1.save()
        item2 = Item(name="item 2", created_by=self.user)
        item2.save()

        self.assertEqual(self.user.item_set.count(), 2)


class ItemAttributeTest(UserTests):
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


class NlpTests(unittest.TestCase):
    def setUp(self):
        self.parser = nlp.Parser()


class NlpTests(NlpTests):
    scenarios = (
        (
            "Massage with Jill at 7:45PM on 6/1",
            {"what": "massage", "when.start_date": "6/1", "when.start_time": "7:45pm", "who": "jill"},
            {"what": "massage", "when": {"start_date": datetime.date(2012, 6, 1), "start_time": "19:45"}, "who": "jill"},
        ),
        #("Plan dinners every other Sunday", {"what": "plan dinners", "when.start_date": "sunday", "when.recurrence.frequency": "2", "when.recurrent.period": "week"})
        (
            "Plan dinners every other Sunday",
            {"what": "plan dinners", "when.recurrence": "every other sunday"},
            {"what": "plan dinners", "when": {"start_date": datetime.date(2012, 5, 20), "recurrence": {"frequency": 2, "period": "week"}}},
        ),
        (
            "Add brocoli to grocery",
            {"what.item": "brocoli", "what.list": "grocery"},
            {"what": {"item": "brocoli", "list": "grocery"}},
        ),
        (
            "Add brocoli and carrots to grocery list",
            {"what.item": "brocoli and carrots", "what.list": "grocery"},
            {"what": {"item": ["brocoli", "carrots"], "list": "grocery"}},
        ),
        (
            "The doctor on May 7th",
            {"what": "doctor", "when.start_date": "may 7th"},
            {"what": "doctor", "when": {"start_date": "may 7th"}},
        ),
        (
            "Text grocery to Lisa",
            {"what.list": "grocery", "action": "text", "who": "lisa"},
            {"what.list": "grocery", "action": "text", "who": "lisa"},
        )
    )

    def test_utils(self):
        dictionaries = (
            (
                {'a' : 'b', 'c.d' : 'z', 'c.e' : 1},
                {'a' : 'b', 'c' : {'d' : 'z', 'e' : 1}}
            ),
            (
                {"one.two": "three"},
                {"one": {"two": "three"}},
            ),
            (
                {"one.two.three": "four"},
                {"one": {"two": {"three": "four"}}},
            ),
            (
                {"this.first": "is_first", "this.second": "is_not_second", "foo": "bar", "that.first.level": "first.level", "that.first.up": "up"},
                {"foo": "bar", "this": {"first": "is_first", "second": "is_not_second"}, "that": {"first": {"level": "first.level", "up": "up"}}},
            ),
            (
                {"what": "massage", "when.start_date": "6/1", "when.start_time": "7:45pm", "who": "jill"},
                {"what": "massage", "when": {"start_date": "6/1", "start_time": "7:45pm"}, "who": "jill"},
            ),
        )

        for attempt in dictionaries:
            #pdb.set_trace()
            translated = transform.unflatten_dict(attempt[0])
            ending = attempt[1]
            for key in (ending.keys()):
                self.assertEqual(translated[key], ending[key])

        #pdb.set_trace()

    def test_scenarios(self):
        for scenario in self.scenarios:
            #result = self.parser.parse_command(scenario[0])
            result = self.parser.parse_command(scenario[0])
            #comparison = transform.DictToObject(**scenario[1])
            comparison = scenario[1]
            #pdb.set_trace()
            self.assertDictEqual(result, comparison)

    def test_npl_mapping(self):
        for scenario in self.scenarios:
            #pdb.set_trace()
            result = self.parser.map_command(scenario[1])
            comparison = scenario[2]

            for key in (comparison.keys()):
                self.assertEqual(result[key], comparison[key])

        #for key in comparison.__dict__:
        #    self.assertEqual(getAttr(result,key), comparison[key])

# class ViewTests(UserTests):
#     def setUp(self):
#         self.attribute = Attribute(datatype="DATE", name="Due")
#         self.item = Item(created_by=self.user)

#     def test_response_of_dated_item(self):
#         pass
#         #views.add_item("bbq tomorrow")
#         # response should equal "bbq on tomorrow"
