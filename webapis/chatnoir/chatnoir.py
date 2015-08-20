#!/usr/bin/env python3
"""
    Api Wrapper for chatnoir queries

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
from webutils import lInfo, jPrint
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../html2text-2014.9.25.zip")

import html2text


class Chatnoir(CachedRequester):
    _baseurl = "http://webis15.medien.uni-weimar.de/chatnoir"
    __searchurl = _baseurl + "/json?"
    __docurl = _baseurl + "/clueweb?"
    __snippeturl = _baseurl + "/snippet?"

    def get_by_query(self, query, limit=10):
        """
        :query
        :limit how many results should be retrieved
        """
        return self._request({"query": query, "token": self._api_key, "resultlength": limit}, self.__searchurl)

    def __get_raw_document_by_internal_id(self, docid):
        """
        docid is the internal docid of chatnoir2
        """
        html = self._raw_request({"id": docid, "token": self._api_key}, self.__docurl)
        return {"raw": html2text.html2text(html)}

    def __to_longid(self, docid):
        return str(int(docid.replace("clueweb09-", "")[2:].replace("-", "")))

    def get_result_vector_by_query(self, query, limit=10):
        res = self.get_by_query(query, limit)
        return [x["WarcTrecID"] for x in res["Page"]]

    def get_document_by_id(self, docid):
        """
        use trec id to get the raw document
        """
        res = self.__get_raw_document_by_internal_id(self.__to_longid(docid))
        res["docid"] = docid
        return res

    def get_snippet(self, docid, query):
        return self._request({"query": query, "token": self._api_key, "id": self.__to_longid(docid), "length": 500}, self.__snippeturl)


def main(params):

    chatnoir = Chatnoir()

    lInfo("ok")
    jPrint(chatnoir.get_by_query("star trek"))
    jPrint(chatnoir.get_document_by_id("clueweb09-en0011-25-35348"))
    jPrint(chatnoir.get_snippet("clueweb09-en0011-25-35348", "star trek"))


if __name__ == "__main__":
    main(sys.argv[1:])
