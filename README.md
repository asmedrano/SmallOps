#SmallOps
Automated Ops via Fabric.

##Why
We use Chef at work and its great. Especially when you are managing a bunch of machines. For my home servers I dont really want to use Chef. Its a little too much for what I do. So this was my solution to not writing bash scripts.

## Installation
You will need ```Fabric``` http://docs.fabfile.org/en/1.5/#installation as well as the SmallOps code https://github.com/asmedrano/SmallOps

## Before you get started
```Fabric``` communicates to your server via SSH so make sure you have that all set up. If you'd like you can set up password less sudo for the user you run any ```sudo``` commands as. This is up to you. If you don't, you'll end up sitting there typing in the password more than once. 

## Running it
```cd``` into the directory with the SmallOps code

Run it 

```$ fab -H ip_or_hostname_for_server -u user_run_as go:the_name_of_your_file.ini```

## Scripts
SmallOps uses ```config.ini``` type files to orchestrate actions. As of right now you have to have your directory structured in this way.
```

├── core
├── fabfile.py
└── resources -> ../SmallOpsResources # this is symbolic link. Using it this way lets you keep your scripts in thier own gitrepo
├── files
│   └── test.txt
└── scripts
    └── smallops-sample-script.ini
```

### Example Script
```
;BTW this is comment 

;[package]
;package=nginx
;label=nginx

;[service]
;service=nginx
;label=Restart Service Example
;action=restart

;[bash]
;label=bash example
;cmd=ls /home

;[git]
;label=Git Example
;url=git://github.com/asmedrano/myShell.git
;branch=master
;directory=/tmp/test
;user=someuser
;sync=False

;[file]
;label=File Example
;name=/path/tofile/on/your/local/system
;directory=/path/on/server
;user=someuser
;mode=0755

```

### Supported directives
Right now SmallOps knows 5 directives:

```package``` installs packages via apt-get

```service``` usefull for managing a service such as nginx or apache2

```bash``` ... Bash Commands

```git``` Clone and pull git repos

```file``` Put local files onto the target server


### Directives
All directives support the following options:

```label``` A label for the action you are running

```user``` The user to execute as  #TODO though most of them are implemented.

Hopefully the options specific to the directive are self explanitory. I will however add some better docs later.

