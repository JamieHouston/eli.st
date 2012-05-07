#!/usr/bin/env python

"""
Parse human-readable request including date or location
"""

import utils.parsedatetime as pdt
import utils.parsedatetime_consts as pdc
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
