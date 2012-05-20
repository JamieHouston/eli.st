import pdb
import re


class AddToList(object):
    def __init__(self):
        self.regexp = re.compile(self.command_regex)

    def parse_command(self, command, result):
        to_parse = command.lower()
        matches = self.regexp.match(to_parse)
        #pdb.set_trace()
        if matches:
            for key in matches.groupdict():
                # TODO: Compile sub
                re.sub(key, '', command)

                result["what"][key] = matches[key]

        return command, result

AddToList.command_regex = r'add (?P<item>[\w\d]*) to (the )?(?P<list>[\w\d]*)(list)?'
AddToList.example = 'Add carrots to the grocery list'


#class Shortcuts(Parser):
#    commandRegex = r'(?P<list>[\w\d]*):(?P<item>[\w\d]*)'

parsers = (
    AddToList,
    )
