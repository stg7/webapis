#!/usr/bin/env python3
"""
    Api Wrapper for whatismyip queries

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


class Whatismyip(CachedRequester):
    """
    get your current external ip adress
    """
    _baseurl = "http://whatismyip.org/"

    def get(self):
        res = self._raw_request({}, use_cache=False)
        return re.findall("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", res)[0]


def main(params):
    whatismyip = Whatismyip()
    print(json.dumps(whatismyip.get(), indent=4, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1:])
