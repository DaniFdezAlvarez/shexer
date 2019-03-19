from __future__ import print_function
import sys


def log_to_error(msg, source=None, target_log=sys.stderr):
    # pass
    print(msg + ". Source: " + (source if source is not None else "Not specified"), file=target_log)
