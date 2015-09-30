#!/usr/bin/env python3
"""
    Api Wrapper for chatnoir2 queries

    Copyright 2015-today

    Author: Steve Göring
    Contact: stg7@gmx.de
"""

import sys
import os
import argparse
import json
import urllib.request
import shelve
import time

sys.path.insert(0, os.path.dirname(__file__) + '/..')
from webutils import CachedRequester
from webutils import lInfo


class Chatnoir2(CachedRequester):
    _baseurl = "http://webis8:8080"
    __chatnoir2searchurl = _baseurl + "/api/_simple?"
    __chatnoir2rawdocurl = _baseurl + "/cache?"

    def __get_internal_id(self, docid, index):
        internal_id = ""
        for r in self.get_by_query(docid, index)["results"]:
            if r["trec_id"] == docid:
                internal_id = r["id"]
                break
        return internal_id

    def get_by_query(self, query, index="webis_clueweb12", size=10):
        """
        :query
        :index index that should be used, possible values:
            "webis_clueweb12", "webis_clueweb09" or "webis_clueweb12,webis_clueweb09"
        """
        return self._request({"q": query, "i": index, "apiKey": self._api_key, "size": size}, self.__chatnoir2searchurl, 1)

    def __get_raw_document_by_internal_id(self, docid, index="webis_clueweb12"):
        """
        docid is the internal docid of chatnoir2
        """
        return self._raw_request({"docId": docid, "raw": "1", "plain": "1", "i": index, "apiKey": self._api_key}, self.__chatnoir2rawdocurl)

    def get_raw_document_by_id(self, docid, index="webis_clueweb12"):
        """
        use trec id to get the raw document
        """
        return self.__get_raw_document_by_internal_id(self.__get_internal_id(docid, index))

    def get_results_by_query(self, query, index="webis_clueweb12", size=50):
        """
        :query
        :index index that should be used, possible values:
            "webis_clueweb12", "webis_clueweb09" or "webis_clueweb12,webis_clueweb09"
        """
        res = self.get_by_query(query, index, size)
        return [r["trec_id"] for r in res["results"]]


def main(params):

    chatnoir2 = Chatnoir2()

    lInfo("ok")
    lInfo(json.dumps(chatnoir2.get_by_query("star trek"), indent=4, sort_keys=True))



if __name__ == "__main__":
    main(sys.argv[1:])
