import pdb
import os
import imp
import sys
from collections import defaultdict

home = os.path.dirname(__file__)


def tree():
    return defaultdict(tree)


class Commander(object):
    # TODO: Add config or way to say which modules or modules.parsers to use
    # Like: SingleParser, ActionParser.Text, etc

    def setup(self):
        self.variables = {}
        self.examples = {}
        self.parsers = []

        filenames = []
        modules = []
        module_path = os.path.join(home, 'modules')
        for fn in os.listdir(module_path):
                if fn.endswith('.py') and not fn.startswith('_'):
                    filenames.append(os.path.join(home, 'modules', fn))

        for filename in filenames:
            name = os.path.basename(filename)[:-3]
            try:
                module = imp.load_source(name, filename)
            except Exception, e:
                print >> sys.stderr, "Error loading %s: %s (in Commander.py)" % (name, e)
            else:

                self.register(module)
                modules.append(name)
        if modules:
            print >> sys.stderr, 'Registered modules:', ', '.join(modules)
        else:
            print >> sys.stderr, "Warning: Couldn't find any modules"



    def register(self, module):
        def bind(self, func):

            # register documentation
            if not hasattr(func, 'name'):
                func.name = func.__class__.__name__
            if hasattr(func, 'example'):
                self.examples[func.name] = func.example
            self.parsers.append(func)

        if hasattr(module, 'parsers'):
            for func in module.parsers:
                parser = func()
                if hasattr(parser, 'setup'):
                        parser.setup()
                bind(self, parser)

    def parse_command(self, command):
        result = tree()

        for parser in self.parsers:
            #pdb.set_trace()
            if len(command) == 0:
                # all done (or can't even get started)
                break

            # TODO: is this the right way to do this?
            command, result = parser.parse_command(command, result)

        # TODO: Pull this into function as well:
        if command and result.has_key("what") and result["what"].has_key("item") is None:
            result["what"]["item"] = command

        return result
