#!/usr/bin/env python3
"""
    Api Wrapper for random.org random numbers

    Copyright 2015-today

    Author: Steve Göring
    Contact: stg7@gmx.de
"""

import sys
import os
import argparse
import json
import re

sys.path.insert(0, os.path.dirname(__file__) + '/..')
from webutils import CachedRequester
from webutils import lInfo


class Randomorg(CachedRequester):
    """
    get a random number
    """
    _baseurl = "https://www.random.org/integers/?"

    def get(self, min_=1, max_=100):
        """
        return a random integer between min_ and max_
        """
        params = {
                "num": 1,
                "min": min_,
                "max": max_,
                "col": 1,
                "base": 10,
                "format": "plain",
                "rnd": "new"
            }
        return {"rnd": self._raw_request(params, use_cache=False), "min": min_, "max": max_}


def main(params):
    randomorg = Randomorg()
    print(json.dumps(randomorg.get(10, 1000), indent=4, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1:])
