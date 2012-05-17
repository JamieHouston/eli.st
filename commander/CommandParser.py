import re


class Parser():
    def __init__(self):
        commandRegex = r'add (?P<item>[\w\d]*) to (the )?(?P<list>[\w\d]*)(list)?'
        self.regexp = re.compile(commandRegex)

    def parse(self, command):
        to_parse = command.lower()
        self.match = self.regexp.match(to_parse)
        return self.is_valid() and self.parse_command()

    def is_valid(self):
        return self.match

    def parse_command(self):
        result = {}
        matches = self.match.groupdict()
        for key in matches:
            result["what." + key] = matches[key]
        return result


class AddToList(Parser):
    pass


class Shortcuts(Parser):
    commandRegex = r'(?P<list>[\w\d]*):(?P<item>[\w\d]*)'
