#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This script performs the inspection of Github pull requests for the
compliance with contributing guidelines."""

from __future__ import (absolute_import, division, print_function)

__author__ = "Paul Greenberg @greenpau"
__version__ = "1.0.1"
__maintainer__ = "Paul Greenberg"
__email__ = "greenpau@outlook.com"
__status__ = "Alpha"

import os
import sys
import logging
import signal
from pprint import pprint
IS_PYGIT_READY = True
try:
    from git import Repo
    IS_PYGIT_READY = True
except ModuleNotFoundError:
    IS_PYGIT_READY = False

SCRIPT_NAME = str(os.path.basename(__file__)).replace('.pyc', '').replace('.py', '').replace('./', '')
SCRIPT_DIR = str(__file__).replace(os.path.basename(__file__), '')
STDIN_TIMEOUT = 2
SCRIPT_INPUT = []
LOG = logging.getLogger(SCRIPT_NAME)
logging.basicConfig(stream=sys.stdout, format='%(asctime)s %(name)s [%(levelname)s] %(message)s')
LOG.setLevel(logging.DEBUG)

def trigger_timeout(signum, frame):
    """Raises TimeoutError."""
    raise TimeoutError()

def capture_stdin():
    """Processes piped input."""
    output = []
    for line in sys.stdin:
        output.append(line.rstrip())
    return output

def main():
    """Manages pull request inspection."""
    if not IS_PYGIT_READY:
        LOG.error('This script requires GitPython (gitpython.readthedocs.org)')
        sys.exit(1)
    signal.signal(signal.SIGALRM, trigger_timeout)
    signal.alarm(STDIN_TIMEOUT)
    piped_input_found = False
    args_input = sys.argv[1:]
    try:
        piped_input = capture_stdin()
        if piped_input:
            piped_input_found = True
    except TimeoutError:
        pass

    LOG.info("Piped input found: %r", piped_input_found)
    if piped_input_found:
        pprint(piped_input)

    if args_input:
        LOG.info("Input arguments found: %s", args_input)
    else:
        LOG.info("Input arguments not found")

    repo = Repo('.')
    # LOG.debug('Active branch: %s', repo.active_branch.name)
    LOG.debug('Bare: %r', repo.bare)
    for branch in repo.branches:
        # Refs.symbolic
        LOG.debug('Branch: %s', type(branch))
        LOG.debug('Branch: %r', branch.is_detached)
        LOG.debug('Remote: %r', branch.is_remote())
        LOG.debug('Valid: %r', branch.is_valid())
        # git.refs.log.RefLog
        branch_log = branch.log()
        LOG.debug('Log: %s', type(branch_log))


if __name__ == '__main__':
    main()
