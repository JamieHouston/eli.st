#!/usr/bin/env python

"""
Parse human-readable request including date or location
"""

import utils.parsedatetime as pdt
import utils.parsedatetime_consts as pdc
from utils import transform
from nltk.corpus import wordnet
import re
import pdb
from time import mktime
from datetime import date


class Parser(object):
    def __init__(self):
        c = pdc.Constants()
        c.BirthdayEpoch = 12
        self.parser = pdt.Calendar(c)

    def parse_natural_date(self, text_input):
        date_struct = self.parser.parse(text_input)
        return_date = date.fromtimestamp(mktime(date_struct[0]))
        return return_date

    def new_type(self, current, singularize=False):
        self.current = current
        self.result[current] = []
        self.singularize = singularize

    def parse_command(self, command_input):
        chunks = command_input.lower().split(' ')
        self.result = {}

        #if re.match('text', command_input):
        if chunks[0] == "text":
            self.result["action"] = [chunks[0]]
            command_result = self.parse_text(chunks[1:])
        else:
            command_result = self.parse_request(chunks)

        command_result = {}
        for key in self.result:
            command_result[key] = ' '.join(self.result[key])

        return command_result

    def map_command(self, command_input):
        unflattened = transform.unflatten_dict(command_input)
        result = {}
        for key, val in unflattened.iteritems():
            result[key] = {}
            if key == "when":
                for key_type in val:
                    if key_type == "start_date":
                        result[key][key_type] = self.parse_natural_date(val[key_type])
                        #val[key_type] = parsed
                    elif key_type == "start_time":
                        #result[key][key_type] = self.parse_natural_date(val[key_type])
                        result[key][key_type] = "19:45"
                    else:
                        result[key][key_type] = val
                    #elif key_type == "recurrence":
                    #    result[key] = {"start_date": self.parse_natural_date("sunday"), "recurrence": {"frequency": 2, "period": "week"}}
            elif key == "what":
                for key_type in val:
                    if key_type == "item" and "and" in val:
                        result[key][key_type] = val.split(" and ")
                    else:
                        #pdb.set_trace()
                        result[key][key_type] == val
            else:
                result[key] = val
        return result

    def add_default(self, chunk):
        if len(self.current):
            if not self.current.endswith(chunk):
                if self.singularize:
                    chunk = wordnet.morphy(chunk)
                self.result[self.current].append(chunk)
        else:
            if not "what" in self.result:
                self.result["what"] = []
            if not (chunk == "the" and len(self.result["what"]) == 0):
                self.result["what"].append(chunk)

    def parse_text(self, chunks):
        self.new_type("what.list")
        for index, chunk in enumerate(chunks):
            if chunk == "to":
                self.new_type("who")
            else:
                self.add_default(chunk)

    def parse_request(self, chunks):

        self.current = ""
        self.singularize = False
        for index, chunk in enumerate(chunks):
            if chunk == "add" and index == 0:
                self.new_type("what.item")
            elif chunk == "to" and self.current == "what.item":
                self.new_type("what.list", True)
            elif chunk == "with":
                self.new_type("who")
            elif chunk == "every":
                self.new_type("when.recurrence")
                self.result[self.current] = [chunk]
            elif chunk == "at":
                self.new_type("when.start_time")
            elif chunk == "on":
                self.new_type("when.start_date")
            else:
                self.add_default(chunk)

        # for key in result:
        #     parts = key.split(".")
        #     if len(parts) == 2:
        #         value = {parts[1]: ' '.join(result[key])}
        #     else:
        #         value = ' '.join(result[key])
        #     setattr(command, parts[0], value)

        # return command
