import unittest
from CommandParser import Parser


class TestCommandParser(unittest.TestCase):
    scenarios = (
    (
        ["Add brocoli to grocery", "add brocoli to the grocery list"],
        {"what.item": "brocoli", "what.list": "grocery"},
        {"what": {"item": "brocoli", "list": "grocery"}},
    ),
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
    )

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.parser = Parser()

    def test_parser(self):
        for scenario in self.scenarios:
            before = scenario[0]
            after = scenario[1]
            if type(before) is list:
                for command in before:
                    #print "comparing {0} to {1}".format(command, after)
                    self.compare(command, after)
            else:
                self.compare(before, after)

#        result = {"what.list": "grocery", "what.item": "brocoli"}
#        diff = set(parsed) - set(result)
#        self.assertEqual(len(diff), 0)
    def compare(self, before, after):
        result = self.parser.parse(before)
        self.assertDictEqual(result, after)

if __name__ == '__main__':
    unittest.main()
