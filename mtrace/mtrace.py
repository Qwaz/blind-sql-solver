#!/usr/bin/env python3
import os
import sys

env = os.environ
env['LD_PRELOAD'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib_mtrace')

os.execve(sys.argv[1], sys.argv[1:], env)
