#!/usr/bin/env python3
"""
    Querysegmentation Wrapper

    Copyright 2015-today

    Author: Steve Göring
    Contact: stg7@gmx.de
"""

import sys
import os
import argparse
import json

sys.path.insert(0, os.path.dirname(__file__) + '/..')
from webutils import CachedRequester
from webutils import lInfo


class Querysegmentation(CachedRequester):
    _baseurl = "http://webis16.medien.uni-weimar.de:8080/query-segmentation-server/query"

    def get_by_query(self, query):
        if query is None:
            return {}
        return self._request_post({"": query})


def main(params):

    query_segmentation = QuerySegmentation()

    lInfo("ok")
    entity = "bathroom".lower()
    query = "choose bathroom".lower()

    res = query_segmentation.get_by_query(query)

    lInfo(json.dumps(res, indent=4, sort_keys=True))

    print(res["hyb-a"])


if __name__ == "__main__":
    main(sys.argv[1:])
