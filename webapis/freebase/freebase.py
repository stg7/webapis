#!/usr/bin/env python3
"""
    Api Wrapper for freebase queries

    Copyright 2015-today

    Project Task Track axiomatic reranking
    Author: Steve Göring
    Contact: stg7@gmx.de
"""

import sys
import os
import argparse
import json
import urllib.request
import shelve

sys.path.insert(0, os.path.dirname(__file__) + '/..')
from webutils import CachedRequester
from webutils import lInfo


class Freebase(CachedRequester):
    """
    https://developers.google.com/freebase/v1/getting-started
        * fist get an api key
        * store key in a plain text document named api_key and load it
    """
    _baseurl = "https://www.googleapis.com/freebase/v1/search?"

    def _request(self, params={}):
        params["key"] = self._api_key
        return super()._request(params)

    def get_by_query(self, query):
        if query is None:
            return {}
        return self._request({"query": query})

    def get_related(self, query, entity="", mid=""):
        byquery = [x["name"].lower() for x in self.get_by_query(query)["result"] if "name" in x and x["name"] != ""]
        byentity = []
        if entity != "" and entity != None:
            byentity = [x["name"].lower() for x in self.get_by_query(entity)["result"] if "name" in x and x["name"] != ""]

        return list(set(byquery + byentity))

    def get_by_mid(self, mid):
        if mid is None:
            return {}
        return self._request({"mid": mid})


def main(params):


    freebase = Freebase()

    lInfo("ok")
    lInfo(json.dumps(freebase.get_by_query("star trek"), indent=4, sort_keys=True))
    lInfo("...")
    lInfo(json.dumps(freebase.get_by_mid("/m/01j2bj"), indent=4, sort_keys=True))

    midresult = freebase.get_by_mid("/m/0jpmt")
    lInfo(json.dumps(midresult, indent=4, sort_keys=True))

    names = [x["name"] for x in midresult["result"]]
    lInfo(names)

    query = "solar power home"
    entity = "solar power"
    mid = "/m/05t0ydv"

    result = freebase.get_related(query, entity=entity, mid=mid)
    lInfo(json.dumps(result, indent=4, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1:])
