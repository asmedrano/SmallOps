from fabric.api import run

class Runner(object):
    """ Base class for running commands"""
    parser = None
    valid_options = ['only_if', 'label'] # supported options
    label = None
    instuction = None
    section = None
    def __init__(self, section, valid_options, parser):
        self.parser = parser
        self.section = section
        self.valid_options = self.valid_options + valid_options

    def do_run(self):
        self.label = self.get_value(self.section, 'label') or None
        self.print_label(self.section)

    def print_label(self, prefix=''):
        if self.label != None:
            print "%s: Running %s" % (prefix, self.label)

    def get_value(self, section, option):
        return self.parser.get(section, option)

class BashRunner(Runner):

    def __init__(self, parser):
        super(BashRunner, self).__init__('bash', ['cmd','user'], parser)

    def do_run(self):
        super(BashRunner, self).do_run()
        cmd  = self.get_value(self.section, 'cmd')
        run(cmd)

class PackageRunner(Runner):

    def __init__(self, parser):
        super(PackageRunner, self).__init__('package', ['action, package'], parser)

    def do_run(self):
        super(PackageRunner, self).do_run()
        package = self.get_value(self.section, 'package')
        run('sudo apt-get install %s' % package)


class ServiceRunner(Runner):

    def __init__(self):
        super(PackageRunner, self).__init__('service', ['action, service'])

    def do_run(self):
        super(ServiceRunner, self).do_run()
        service = self.get_value(self.section, 'service')
        action = self.get_value(self.section, 'action')
        run('sudo service %s' % service, action)
