import pdb
import json
import unittest
from CommandParser import Commander
import os
import sys

home = os.path.dirname(__file__)


class TestCommandParser(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.parser = Commander()
        self.parser.setup()
        module_path = os.path.join(home, 'tests')
        filenames = []
        self.tests = []

        for fn in os.listdir(module_path):
            if fn.endswith('.py') and not fn.startswith('_'):
                        filenames.append(os.path.join(home, 'tests', fn))

        for filename in filenames:
            pdb.set_trace()
            self.tests.append(json.load(open(filename)))
            # name = os.path.basename(filename)[:-3]
            # try:
            #     module = imp.load_source(name, filename)
            # except Exception, e:
            #     print >> sys.stderr, "Error loading %s: %s (in Commander.py)" % (name, e)
            # else:

            #     self.register(module)
            #     modules.append(name)


    def test_parsers(self):
        pdb.set_trace()
        for key in self.tests:
            pass




    # scenarios = (
    # (
    #     ["Add brocoli to grocery", "add brocoli to the grocery list"],
    #     #{"what.item": "brocoli", "what.list": "grocery"},
    #     {"what": {"item": "brocoli", "list": "grocery"}},
    # ),
    # (
    #     "Massage with Jill at 7:45PM on 6/1",
    #     {"what": "massage", "when.start_date": "6/1", "when.start_time": "7:45pm", "who": "jill"},
    #     {"what": "massage", "when": {"start_date": datetime.date(2012, 6, 1), "start_time": "19:45"}, "who": "jill"},
    # ),
    #("Plan dinners every other Sunday", {"what": "plan dinners", "when.start_date": "sunday", "when.recurrence.frequency": "2", "when.recurrent.period": "week"})
    # (
    #     "Plan dinners every other Sunday",
    #     {"what": "plan dinners", "when.recurrence": "every other sunday"},
    #     {"what": "plan dinners", "when": {"start_date": datetime.date(2012, 5, 20), "recurrence": {"frequency": 2, "period": "week"}}},
    # ),
    # (
    #     "Add brocoli and carrots to grocery list",
    #     {"what.item": "brocoli and carrots", "what.list": "grocery"},
    #     {"what": {"item": ["brocoli", "carrots"], "list": "grocery"}},
    # ),
    # (
    #     "The doctor on May 7th",
    #     {"what": "doctor", "when.start_date": "may 7th"},
    #     {"what": "doctor", "when": {"start_date": "may 7th"}},
    # ),
    # (
    #     "Text grocery to Lisa",
    #     {"what.list": "grocery", "action": "text", "who": "lisa"},
    #     {"what.list": "grocery", "action": "text", "who": "lisa"},
    #)

#     def setUp(self):
#         unittest.TestCase.setUp(self)

#         self.parser = Commander()
#         self.parser.setup()

#     def test_parser(self):
#         for scenario in self.scenarios:
#             before = scenario[0]
#             after = scenario[1]
#             if type(before) is list:
#                 for command in before:
#                     #print "comparing {0} to {1}".format(command, after)
#                     self.compare(command, after)
#             else:
#                 self.compare(before, after)

# #        result = {"what.list": "grocery", "what.item": "brocoli"}
# #        diff = set(parsed) - set(result)
# #        self.assertEqual(len(diff), 0)
#     def compare(self, before, after):
#         result = self.parser.parse_command(before)
#         self.assertDictEqual(result, after)

if __name__ == '__main__':
    unittest.main()
