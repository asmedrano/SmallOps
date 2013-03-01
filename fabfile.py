from ConfigParser import SafeConfigParser
from fabric.api import run, env
from core.runners import BashRunner, PackageRunner, ServiceRunner

parser = SafeConfigParser()

def go(*recipes):
    """ Currently testing with fab -H nando -u asmedrano go:smallops """
    for r in recipes:
        parser.read("recipes/%s.ini" % r)
        _parse_sections(parser)


# Valid sections in config files
valid_sections = ['package','bash']

def _parse_sections(parser):
    for section in parser.sections():
       if section in valid_sections:
           # we'll need to validate here
           if section == 'bash':
               runner = BashRunner(parser=parser)
               runner.do_run()
           if section == 'package':
               runner = PackageRunner(parser=parser)
               runner.do_run()




