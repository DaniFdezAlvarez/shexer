import sys
from datetime import datetime

def _curr_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S -- ")


# def log_to_error(msg, source=None, target_log=sys.stderr):
#     # pass
#     print(msg + ". Source: " + (source if source is not None else "Not specified"), file=target_log)


def log_msg(verbose, msg, err=True):
    if verbose:
        print(_curr_time() + msg, flush=True, file=None if not err else sys.stderr)