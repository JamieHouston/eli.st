from datetime import date, time, datetime
from time import mktime
import utils.parsedatetime as pdt
import utils.parsedatetime_consts as pdc
import pdb
import re

class AddToList(object):
    def __init__(self):
        self.regexp = re.compile(self.command_regex)

    def parse_command(self, command, result):
        to_parse = command.lower()
        matches = self.regexp.match(to_parse)
        if matches and matches.groupdict():
            result["action"] = "add"
            found = matches.groupdict()
            for key in found:
                # TODO: Compile sub
                text = found[key]
                to_parse = re.sub(text, '', to_parse)

                result["what"][key] = text
            for group in matches.groups():
                if group is not None and len(group):
                    to_parse = to_parse.replace(group, '')
        return to_parse, result

AddToList.command_regex = r'(add )(?P<item>[\w\d]*)( to )(the )?(?P<list>[\w\d]*)( list)?'
AddToList.example = 'Add carrots to the grocery list'


class NaturalDate(object):
    def __init__(self):
        c = pdc.Constants()
        c.BirthdayEpoch = 12
        self.parser = pdt.Calendar(c)

    def clean_string(self, text):
        if text.endswith("on"):
            return text[:(len(text) - 3)]
        return text

    def parse_natural_datetime(self, text_input):
        #pdb.set_trace()
        parsed, result_type, parts_to_remove = self.parser.parse(text_input)

        for part in filter(lambda p: len(p), parts_to_remove):
            text_input = text_input.replace(part, '').strip()
        if result_type == 1:
            # found a date
            text_input = self.clean_string(text_input)
            return_value = date.fromtimestamp(mktime((parsed[0], parsed[1], parsed[2], 0, 0, 0, 0, 0, 0)))
        elif result_type == 2:
            # found a time
            return_value = time(parsed[3], parsed[4])
        elif result_type == 3:
            # found a datetime
            return_value = datetime.fromtimestamp(mktime(parsed))
        else:
            return_value = None

        return text_input, return_value, result_type

    def parse_command(self, command, result):
        command, parsed, result_type = self.parse_natural_datetime(command.lower())

        if result_type == 1:
            result["when"]["start_date"] = parsed
        elif result_type == 2:
            result["when"]["start_time"] = parsed
        elif result_type == 3:
            result["when"]["start_date"] = parsed.date()
            result["when"]["start_time"] = parsed.time()

        if result_type:
            result["action"] = "add"

        return command, result

NaturalDate.example = 'Write some code tomorrow'


class RecurrenceFinder(object):
    def __init__(self):
        self.regexp = re.compile(self.command_regex)

    def parse_command(self, command, result):
        to_parse = command.lower()
        matches = self.regexp.match(to_parse)
        #pdb.set_trace()
        if matches:
            #pdb.set_trace()
            result["action"] = "add"
            result[""]
            pairs = matches.groupdict()
            frequency = pairs["frequency"]
            to_parse = re.sub(frequency, '', to_parse)
            result["when"]["recurrence"]["frequency"] = 1 if frequency == "every" else 2
            result["when"]["recurrence"]["day"] = pairs["period"]

        return to_parse, result
RecurrenceFinder.command_regex = r'.+\s(?P<frequency>every\sother|every)\s(?P<period>\w+).*'
RecurrenceFinder.example = 'Do something every other month'

#class Shortcuts(Parser):
#    commandRegex = r'(?P<list>[\w\d]*):(?P<item>[\w\d]*)'
parsers = (
    AddToList,
    NaturalDate,
    RecurrenceFinder,
    )
