#!/usr/bin/env python3
"""
    Api Wrapper for netspeak queries

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


class Netspeak(CachedRequester):
    _baseurl = "http://api.netspeak.org/netspeak3/search?"

    def get_by_query(self, query):
        """
        netspeak3 api documentation: http://www.netspeak.org/#developer

        a query can have operators:

            query="a house*" : Matches zero or more words.
            query="a #house" : Finds matches using the following word and each of its synonyms in turn.
            query="a ?house" : Matches exactly one word.
            query="a [house, car]" : Finds matches using each word in turn, including the empty word. Nesting of operators is not allowed.
            query="a {house, car}" : Finds matches of each permutation of the enclosed words. Nesting of operators is not allowed.
        """
        if query is None:
            return []
        return self._request(params={"query": query, "format": "json"})

    def __get_realted_by_query(self, query):
        if query == "" or query == None:
            return []
        query = "*" + "*".join(query.split()) + "*"
        result = self.get_by_query(query)
        # parse result and tidy up, all unneeded things were removed
        res_tidy = []
        for k in result.keys():
            if isinstance(result[k], list):
                for kk in result[k]:
                    if isinstance(kk, dict):
                        res = ""
                        for kkk in kk:
                            if isinstance(kk[kkk], list):
                                for w in kk[kkk]:
                                    if w["2"] != "":
                                        res += " " + w["2"]
                        res_tidy.append(res.strip())
        return res_tidy

    def get_related(self, query, entity="", mid=""):
        res = self.__get_realted_by_query(query) + self.__get_realted_by_query(entity)
        return list(set([x.replace(".","").replace(",","").replace("  "," ").strip() for x in res]))


def main(params):

    netspeak = Netspeak()

    lInfo("ok")
    entity = "bathroom".lower()
    query = "choose bathroom".lower()

    res = netspeak.get_related(query)


    lInfo(json.dumps(res, indent=4, sort_keys=True))



if __name__ == "__main__":
    main(sys.argv[1:])
