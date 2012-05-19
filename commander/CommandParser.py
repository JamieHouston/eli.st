import pdb
import re, os, imp, sys
from collections import defaultdict

home = os.getcwd()

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

        for fn in os.listdir(os.path.join(home, 'modules')):
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
                func.name = func.__name__
            if hasattr(func, 'example'):
                self.examples[func.name] = func.example
            self.parsers.append(func)

        if hasattr(module, 'parsers'):
            for func in module.parsers:
                if hasattr(func, 'setup'):
                        func.setup()
                bind(self, func)

    def parse_command(self, command):
        result = tree()

        for parser in self.parsers:
            if len(command) == 0:
                # all done (or can't even get started)
                break

            # TODO: is this the right way to do this?
            command, result = parser(command, result)

        # TODO: Pull this into function as well:
        if len(command) and result["what"]["item"] is None:
            result["what"]["item"] = command

        return result
