from item.models import WhatCommand
import re
import pdb
from utils import words


class SearchItems(object):
    def __init__(self):
        self.regexp = re.compile(self.command_regex)

    def parse_command(self, command, result):
        to_parse = command.lower()
        matches = self.regexp.match(to_parse)

        if matches:
            item_list = matches.groupdict()["request"]
            if len(item_list.split()) == 1:
                item_list = words.singularize(item_list)
            model_results = WhatCommand.objects.filter(list=item_list)
            results = [{"pk": what_command.pk, "item": what_command.item} for what_command in model_results]
            if results:
                result["action"] = "search"
                result["results"] = results

        return command, result

SearchItems.command_regex = r'(view|search for|show me) (my )?(?P<request>[\w\d]*)( list)?'
SearchItems.example = 'View my groceries'

parsers = (
    SearchItems,
    )
