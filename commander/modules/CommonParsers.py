import re


parsers = (
    add_to_list,
    )

def add_to_list(command, result):
    def setup():
        self.regexp = re.compile(commandRegex)

    def parse_command(command, result):
        to_parse = command.lower()
        matches = self.regexp.match.groupdict()
        for key in matches:
            # TODO: Compile sub
            re.sub(key, '', command)

            result["what." + key] = matches[key]

        return command, result

    return parse_command(command, result)

add_to_list.command_regex = r'add (?P<item>[\w\d]*) to (the )?(?P<list>[\w\d]*)(list)?'
add_to_list.example = 'Add carrots to the grocery list'

#class Shortcuts(Parser):
#    commandRegex = r'(?P<list>[\w\d]*):(?P<item>[\w\d]*)'
