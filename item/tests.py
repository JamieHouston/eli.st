from django.utils import unittest
from item.models import Attribute, Item
from django.contrib.auth.models import User
import datetime
from utils import nlp, transform


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


class ParseDateTests(NlpTests):
    def setUp(self):
        self.parser = nlp.Parser()

    def test_add_item_on_date(self):
        text_input = "something tomorrow"
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        item = Item()
        chunks = self.parser.parse(text_input)
        item.name, item.value = chunks
        self.assertEqual(item.name, "something")
        self.assertEqual(item.value, tomorrow)


class NlpTests(NlpTests):
    scenarios = (
        ("Massage with Jill at 7:45PM on 4/1", {"what": "massage", "when.start_date": "4/1", "when.start_time": "7:45pm", "who": "jill"}),
        #("Plan dinners every other Sunday", {"what": "plan dinners", "when.start_date": "sunday", "when.recurrence.frequency": "2", "when.recurrent.period": "week"})
        ("Plan dinners every other Sunday", {"what": "plan dinners", "when.recurrence": "every other sunday"}),
        ("Add brocoli to grocery", {"what.item": "brocoli", "where.list": "grocery"}),
        #("Add brocoli and carrots to grocery list", {"what.item": ["brocoli", "carrots"], "where.list": "grocery"}),
        ("Add brocoli and carrots to grocery list", {"what.item": "brocoli and carrots", "where.list": "grocery"}),
        ("The doctor on May 7th", {"what": "doctor", "when.start_date": "may 7th"}),
        ("Text grocery to Lisa", {"what.list": "grocery", "action": "text", "who": "lisa"})
    )

    def test_scenarios(self):
        for scenario in self.scenarios:
            #result = self.parser.parse_command(scenario[0])
            result = self.parser.parse_command(scenario[0])
            #comparison = transform.DictToObject(**scenario[1])
            comparison = scenario[1]

        self.assertDictEqual(result, comparison)
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
