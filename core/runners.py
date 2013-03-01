from fabric.api import run, settings, put, sudo
import re
from ConfigParser import NoOptionError

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
        try:
            return self.parser.get(section, option)
        except NoOptionError:
            return None


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

    def __init__(self, parser):
        super(ServiceRunner, self).__init__('service', ['action, service'], parser)

    def do_run(self):
        super(ServiceRunner, self).do_run()
        service = self.get_value(self.section, 'service')
        action = self.get_value(self.section, 'action')
        run('sudo service %s %s' % (service, action))

class FileRunner(Runner):

    def __init__(self, parser):
        super(FileRunner, self).__init__('file', ['directory', 'name', 'user'], parser)

    def do_run(self):
        super(FileRunner, self).do_run()
        user = self.get_value(self.section, 'user')
        directory = self.get_value(self.section, 'directory') or '/home/%s' % user
        name = self.get_value(self.section, 'name')
        mode = self.get_value(self.section, 'mode')
        put_files = put(name, directory, mode)
        # we need to chown this to the user
        sudo('chown %s %s' % (user, put_files[0]), quiet=True)
        sudo('chgrp %s %s' % (user, put_files[0]), quiet=True)


class GitRunner(Runner):
    def __init__(self, parser):
        self.match = re.compile('[0-9a-zA-Z-_?!]+\.git')
        super(GitRunner, self).__init__('git', ['sync', 'url', 'branch','user'], parser)

    def do_run(self):
        super(GitRunner, self).do_run()
        user = self.get_value(self.section, 'user')
        remote = self.get_value(self.section, 'url')
        branch = self.get_value(self.section, 'branch') or 'master'
        directory = self.get_value(self.section, 'directory') or '/home/%s/%s' % (user, self.match.findall(remote)[0].replace('.git',''))
        sync = True if self.get_value(self.section, 'sync') == 'True' else False
        cmd = 'sudo su {0} -c "git clone {1} -b {2} {3}"'.format(user, remote, branch, directory)
        with settings(warn_only=True):
            result = run(cmd)
            if result.return_code == 0:
                print 'Cloned repo'
            elif result.return_code == 1:
                print result
            elif result.return_code==128:
                # now we are just gonna update the repo since it exists
                if sync == True:
                    print 'Syncing repo'
                    cmd = 'sudo su {0} -c "cd {1} && git pull"'.format(user, directory)
                    run(cmd)
                else:
                    print 'Skipping sync'

            else:
                print result, result.return_code, len(result.return_code)
                raise SystemExit()

