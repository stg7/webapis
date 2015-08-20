#!/usr/bin/env python3
"""
    Webutils Example

    Copyright 2015-today

    Author: Steve Göring
    Contact: stg7@gmx.de
"""

import os
import sys

from webapis.webutils import jPrint
from webapis.webutils import lInfo

from webapis.wikidata import wikidata
from webapis.querysegmentation import querysegmentation
from webapis.google import google

from wikidata import *
from querysegmentation import *
from google import *


def main(args):
    if len(args) == 0:
        print("you should run with a query as command line argument")
        return

    engines = [wikidata.Wikidata(),  querysegmentation.Querysegmentation(), google.Google()]
    query = " ".join(args)

    for e in engines:
        print(e.__class__.__name__.lower())
        jPrint(e.get_by_query(query))

    pass

if __name__ == "__main__":
    main(sys.argv[1:])