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
import re
import time
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

    top_commit_hexsha, base_commit_hexsha = extract_metadata()
    LOG.info("Top commit SHA:      %s", top_commit_hexsha)
    LOG.info("Baseline commit SHA: %s", base_commit_hexsha)

def extract_metadata():
    """Extracts commit hashes from pull request."""
    repo = Repo('.')
    count = 0
    top_commit_hexsha = ""
    base_commit_hexsha = ""
    for commit in repo.iter_commits():
        count += 1
        LOG.debug('Commit Type: %s', type(commit))
        LOG.debug('commit %s', commit.hexsha)
        LOG.debug('Author: %s, <%s>', commit.author.name, commit.author.email)
        LOG.debug('Date:   %s', time.asctime(time.gmtime(commit.committed_date)))
        LOG.debug('Message: %s', commit.message)
        top_commit_hexsha, base_commit_hexsha = parse_merged_commit_message(commit.message)
    if count != 1:
        msg = "expected 1 commit, got %d" % (count)
        raise Exception(msg)
    return top_commit_hexsha, base_commit_hexsha

def parse_merged_commit_message(message):
    """Parses commit message for the presence of commit hashes."""
    regex = r'^Merge\s(?P<top_commit_hexsha>[a-f0-9]+)\sinto\s(?P<base_commit_hexsha>[a-f0-9]+)$'
    for line in message.split('\n'):
        line = line.rstrip()
        if not line.startswith('Merge '):
            continue
        if not re.match(regex, line):
            continue
        LOG.debug('Matched: %s', line)
        matcher = re.match(regex, line)
        return matcher.group('top_commit_hexsha'), matcher.group('base_commit_hexsha')
    raise Exception("commit hashes not found")

if __name__ == '__main__':
    main()
