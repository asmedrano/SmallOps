from ConfigParser import SafeConfigParser
from fabric.api import run, env
from core.runners import FileRunner, GitRunner, BashRunner, PackageRunner, ServiceRunner
from core.config import *
from collections import OrderedDict
import re

class SectionDict(OrderedDict):
    _unique = 0

    def __setitem__(self, key, val):
        if key in VALID_SECTIONS:
            self._unique += 1
            key = str(self._unique) + key
        OrderedDict.__setitem__(self, key, val)

parser = SafeConfigParser(dict_type=SectionDict)

def go(*recipes):
    """ Currently testing with fab -H nando -u asmedrano  go:mysite/samplescript"""
    for r in recipes:
        site = r.split('/')[0]
        if not site:
            print '****Error****'
            print 'Please Choose A Site directory'

        try:
            script = r.split('/')[1]
        except IndexError:
            print '****Error****'
            print 'Please Choose A Script to Run.'

        if site and script:
            f = parser.read("resources/%s/scripts/%s.ini" % (site, script))
            if f:
                print "***** Running script %s *****" % (r)
                _parse_sections(parser, site)
            else:
                print '***** Could not find script: %s *****' % (r)

def _parse_sections(parser, cwsite):
    user = env['user']
    for section in parser.sections():
        if re.sub(r'\d','',section) in VALID_SECTIONS:
            # we'll need to validate here
            if 'bash' in section:
                runner = BashRunner(section=section,parser=parser, user=user, cws=cwsite)
                runner.do_run()
            elif 'package' in section:
                runner = PackageRunner(section=section, parser=parser, user=user,cws=cwsite)
                runner.do_run()
            elif 'service' in section:
                runner = ServiceRunner(section=section, parser=parser, user=user,cws=cwsite)
                runner.do_run()
            elif 'git' in section:
                runner = GitRunner(section=section, parser=parser, user=user,cws=cwsite)
                runner.do_run()
            elif 'file' in section:
                runner = FileRunner(section=section, parser=parser, user=user,cws=cwsite)
                runner.do_run()


