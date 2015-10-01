#!/usr/bin/env python3
"""
    Api Wrapper for wikidata queries

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


class Wikidata(CachedRequester):
    """
    api documentation see: https://www.wikidata.org/w/api.php
    search:
    > https://www.wikidata.org/w/api.php?action=wbsearchentities&search=QUERY&language=en&format=json

    get info about entity:
    > https://www.wikidata.org/entity/ENTITY.json
    e.g.:
    > https://www.wikidata.org/entity/Q16341.json
    """
    _baseurl = "https://www.wikidata.org/w/api.php?"

    def get_by_query(self, query):
        if query is None:
            return {}
        return self._request({"search": query, "action": "wbsearchentities", "language": "en", "format": "json", "limit": "50"})

    def get_related(self, query, entity="", mid=""):
        byquery = [r["label"].lower() for r in self.get_by_query(query)["search"] if "label" in r and r["label"] != ""]
        byentity =[]
        if entity != "" and entity != None:
            byentity = [r["label"].lower() for r in self.get_by_query(entity)["search"] if "label" in r and r["label"] != ""]

        return list(set(byquery + byentity))


def main(params):

    wikidata = Wikidata()

    lInfo("ok")
    entity = "bathroom".lower()
    query = "choose bathroom".lower()

    res = wikidata.get_by_query(entity)

    lInfo(json.dumps(res, indent=4, sort_keys=True))

    related_terms = {entity: 1, query: 1}

    for x in res["search"]:
        k = x["label"].lower()
        related_terms[k] = 1
        #print([x["label"],x.get("description", ""), x["id"]])

    print(len(related_terms))

    for k in sorted(related_terms.keys()):
        print("{} : {}".format(k, related_terms[k]))

    print(json.dumps(wikidata.get_related(entity), indent=4, sort_keys=True))

    query = "solar power home"
    entity = "solar power"
    mid = "/m/05t0ydv"
    print((query, entity, mid))
    print(json.dumps(wikidata.get_related(query, entity, mid), indent=4, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1:])
