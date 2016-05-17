#!/usr/bin/env python

import sys
import pwd
import subprocess
from time import sleep


BLACKLIST = (
    # add blacklisted users here
    #'user1',
)

def set_password(user, password):
    cmd = ["sudo", '/usr/bin/passwd', user]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    p.stdin.write(u'%(p)s\n%(p)s\n' % { 'p': password })
    p.stdin.flush()
    # Give `passwd` cmd 1 second to finish and kill it otherwise.
    for x in range(0, 10):
        if p.poll() is not None:
            break
        sleep(0.1)
    else:
        p.terminate()
        sleep(1)
        p.kill()
        raise RuntimeError('Setting password failed. '
                '`passwd` process did not terminate.')
    if p.returncode != 0:
        raise RuntimeError('`passwd` failed: %d' % p.returncode)

try:
    username, password = sys.stdin.readline().split(':', 1)
except ValueError, e:
    sys.exit('Malformed input')

try:
    user = pwd.getpwnam(username)
except KeyError, e:
    sys.exit('No such user: %s' % username)

if user.pw_uid < 1000:
    sys.exit('Changing the password for user id < 1000 is forbidden')

if username in BLACKLIST:
    sys.exit('Changing password for user %s is forbidden (user blacklisted)' %
             username)

set_password(username, password)

