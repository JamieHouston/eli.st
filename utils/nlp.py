#!/usr/bin/env python

"""
Parse human-readable request including date or location
"""

import utils.parsedatetime as pdt
import utils.parsedatetime_consts as pdc
from nltk.corpus import wordnet
import re

from time import mktime
from datetime import date


class Parser(object):
    def __init__(self):
        c = pdc.Constants()
        c.BirthdayEpoch = 12
        self.parser = pdt.Calendar(c)

    def parse(self, text_input):
        chunks = text_input.split(' ')
        name = chunks[0]
        date_struct = self.parser.parse(chunks[1])
        return_date = date.fromtimestamp(mktime(date_struct[0]))
        return name, return_date

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
                self.new_type("where.list", True)
            elif chunk == "with":
                self.new_type("who")
            elif chunk == "every":
                self.new_type("when.recurrence")
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
