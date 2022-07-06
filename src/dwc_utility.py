import time
import json
import os
import logging
from pathlib import Path

import dwc_config as config

logger = logging.getLogger("utility")

# Create some timer functions to track the execution time
# for the named operation.  This allows setting multiple timers
# at the same time.

timers = {}

def setLevel(level):
    logger.setLevel(level)

def set_timer(name="default"):
    timers[name] = time.perf_counter();
    
def get_timer(name="default"):
    if name in timers:
        elapsed = time.perf_counter() - timers[name]

        return elapsed

    logger.debug("WARNING: Timer not found: {}".format(name))

    return 0

def start_timer(name):
    set_timer(name)

def log_timer(name, msg):
    return "{} - elapsed {}.".format(msg, get_timer(name))

def write_json(json_name, object):
    """
        Write out the provided object to the specified file.
    """

    # Ensure the working directory exists before trying to write
    # this file.

    json_path = os.path.join(Path(__file__).parent.absolute(), "working")

    if not os.path.exists(json_path):
        os.mkdir(json_path)

    json_file = os.path.join(json_path, f"{json_name}.json")

    with open(json_file, "w") as outfile:
        outfile.write(json.dumps(object, indent = 4)) # With pretty print

    return json_file

if __name__ == "__main__":
    write_json("mark", {})