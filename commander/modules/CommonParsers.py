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

    def parse_natural_datetime(self, text_input):
        parsed, result_type = self.parser.parse(text_input)
        if result_type == 1:
            # found a date
            return_value = date.fromtimestamp(mktime((parsed[0], parsed[1], parsed[2], 0, 0, 0, 0, 0, 0)))
        elif result_type == 2:
            # found a time
            return_value = time(parsed[3], parsed[4])
        elif result_type == 3:
            # found a datetime
            return_value = datetime.fromtimestamp(mktime(parsed))
        else:
            return_value = None

        return return_value, result_type

    def parse_command(self, command, result):
        parsed, result_type = self.parse_natural_datetime(command)

        if result_type == 1:
            result["when"]["start_date"] = parsed
        elif result_type == 2:
            result["when"]["start_time"] = parsed
        elif result_type == 3:
            result["when"]["start_date"] = parsed.date()
            result["when"]["start_time"] = parsed.time()

        return command, result

NaturalDate.example = 'Write some code tomorrow'

# class RecurrenceFinder(object):
#     def __init__(self):
#         self.regexp = re.compile(self.command_regex)

#     def parse_command(self, command, result):
#         to_parse = command.lower()
#         matches = self.regexp.match(to_parse)
#         #pdb.set_trace()
#         if matches:
#             for key in matches.groupdict():
#                 # TODO: Compile sub
#                 re.sub(key, '', command)

#                 result["what"][key] = matches[key]

#         return command, result
# RecurrenceFinder.example = 'Do something every other month'




#class Shortcuts(Parser):
#    commandRegex = r'(?P<list>[\w\d]*):(?P<item>[\w\d]*)'

parsers = (
    AddToList,
    NaturalDate,
#    RecurrenceFinder,
    )
