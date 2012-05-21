import utils.parsedatetime as pdt
import utils.parsedatetime_consts as pdc
from utils import transform, words
from time import mktime
from datetime import date


class ManualParser(object):
    def __init__(self):
        c = pdc.Constants()
        c.BirthdayEpoch = 12
        self.parser = pdt.Calendar(c)

    def parse_natural_date(self, text_input):
        date_struct, found = self.parser.parse(text_input)
        return_date = date.fromtimestamp(mktime((date_struct[0], date_struct[1], date_struct[2], 0, 0, 0, 0, 0, 0)))
        return return_date, found

    def new_type(self, current, singularize=False):
        self.current = current
        self.result[current] = []
        self.singularize = singularize

    def parse_command(self, command, result):
        parsed = self._parse_command(command)
        return self.command_output, self.map_command(parsed)

    def _parse_command(self, command):
        chunks = command.lower().split(' ')
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

    def check_dates(self):
        """
        If the text ends with a date (like tomorrow) pull it out
        """

        if ((not "when" in self.result) or (not "start_date" in self.result["when"])) and ("what" in self.result) and ("item" in self.result["what"]) and (type(self.result["what"]["item"]) is str):
            chunks = self.result["what"]["item"].split()
            if len(chunks):
                date_ending, found_date = self.parse_natural_date(chunks[-1])
                if found_date:
                    self.new_type("when.start_date")
                    self.result[self.current] = str(date_ending)
                    self.result["what"]["item"] = " ".join(chunks[:-1])

    def map_command(self, command_input):
        unflattened = transform.unflatten_dict(command_input)
        self.result = {}
        for key, val in unflattened.iteritems():
            self.result[key] = {}
            #pdb.set_trace()
            if key == "when":
                for key_type in val:
                    if key_type == "start_date":
                        #pdb.set_trace()
                        self.result[key][key_type] = str(self.parse_natural_date(val[key_type])[0])
                        #val[key_type] = parsed
                    elif key_type == "start_time":
                        #result[key][key_type] = self.parse_natural_date(val[key_type])
                        self.result[key][key_type] = "19:45"
                    else:
                        self.result[key][key_type] = val
                    #elif key_type == "recurrence":
                    #    result[key] = {"start_date": self.parse_natural_date("sunday"), "recurrence": {"frequency": 2, "period": "week"}}
            elif key == "what" and type(val) is dict:
                for key_type in val:
                    #pdb.set_trace()
                    if key_type == "item" and "and" in val[key_type]:
                        self.result[key][key_type] = val[key_type].split(" and ")
                    else:
                        #pdb.set_trace()
                        self.result[key][key_type] = val[key_type]
            else:
                self.result[key] = val

        self.check_dates()

        return self.result

    def add_default(self, chunk):
        if len(self.current):
            if not self.current.endswith(chunk):
                if self.singularize:
                    chunk = words.singularize(chunk)
                self.result[self.current].append(chunk)
        else:
            self.command_output = " " + chunk
        #     self.current = "what.item"
        #     if not self.current in self.result:
        #         self.result[self.current] = []
        #     if not (chunk == "the" and len(self.result[self.current]) == 0):
        #         self.result[self.current].append(chunk)

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

        if chunks[0] == "add":
            chunks = chunks[1:]

        for index, chunk in enumerate(chunks):
            if chunk == "to" and self.current == "what.item":
                self.new_type("what.list", True)
            elif chunk == "with":
                self.new_type("who")
            elif chunk == "at":
                self.new_type("when.start_time")
            elif chunk == "on":
                self.new_type("when.start_date")
            else:
                self.add_default(chunk)

parsers = (
    ManualParser,
    )
