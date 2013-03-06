from ConfigParser import SafeConfigParser
from fabric.api import run, env
from core.runners import FileRunner, GitRunner, BashRunner, PackageRunner, ServiceRunner

parser = SafeConfigParser()

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
                _parse_sections(parser)
            else:
                print '***** Could not find script: %s *****' % (r)


# Valid sections in config files
valid_sections = ['package','bash', 'service', 'git', 'file']

def _parse_sections(parser):
    user = env['user']
    for section in parser.sections():
       if section in valid_sections:
           # we'll need to validate here
           if section == 'bash':
               runner = BashRunner(parser=parser, user=user)
               runner.do_run()
           elif section == 'package':
               runner = PackageRunner(parser=parser, user=user)
               runner.do_run()
           elif section == 'service':
               runner = ServiceRunner(parser=parser, user=user)
               runner.do_run()
           elif section == 'git':
               runner = GitRunner(parser=parser, user=user)
               runner.do_run()
           elif section == 'file':
               runner = FileRunner(parser=parser, user=user)
               runner.do_run()

