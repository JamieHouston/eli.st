#from item.models import WhatCommand
import re
import pdb
from utils import words


class SearchItems(object):
    def __init__(self):
        self.regexp = re.compile(self.command_regex)

    def parse_command(self, command, result):
        to_parse = command.lower()
        matches = self.regexp.match(to_parse)
        if matches and matches.groupdict():
            item_list = matches.groupdict()["request"]
            if len(item_list.split()) == 1:
                item_list = words.singularize(item_list)
                result["action"] = "search"
                result["what"]["list"] = item_list
                command = ""
            elif len(item_list) == 0:
                command = ""
                result["action"] = "search"
                result["what"]["list"] = "all items"
        return command, result

SearchItems.command_regex = r'(view|search for|show) (my |me )?(everything)?(?P<request>[\w\d]*)( list)?'
SearchItems.example = 'View my groceries'

parsers = (
    SearchItems,
    )
