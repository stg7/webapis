#!/usr/bin/env python3
"""
    google_api - send search requests to google and return resulting urls

    author: Steve Göring
    contact: stg7@gmx.de
    2015
"""

import os
import sys
import datetime
import shelve
import argparse
import time
import json
import re
import random

sys.path.insert(0, os.path.dirname(__file__) + '/..')
from webutils import CachedRequester
from webutils import lInfo
from webutils import jPrint
from webutils import cleanhtml


class GoogleAPI(CachedRequester):
    """
    api documentation: https://developers.google.com/web-search/docs/

    example request:
        http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=star&start=4
    """
    _baseurl = "http://ajax.googleapis.com/ajax/services/search/web?"

    def get_by_query(self, query, limit=4):
        if limit > 32:
            raise Exception("limit to large, must be <= 32")
        if query is None:
            return {}

        time.sleep(5)

        res = self._request({"q": query, "v": "1.0", "userip": "141.54.178.24"}) #

        # for more results: set start=4,8,12,... and get each result as a combined json
        results = res["responseData"]["results"]

        for start in range(4, limit, 4):
            res_tmp = self._request({"q": query, "start": start, "v": "1.0", "userip": "141.54.178.24"})
            time.sleep(1)
            results += res_tmp["responseData"]["results"]

        res["responseData"]["results"] = results
        return res

    def get_related(self, query, entity="", mid=""):
        res = self.get_by_query(query)["responseData"]["results"]

        t = lambda x: " ".join([y for y in x.split() if len(y) > 3])
        titles = [t(x["titleNoFormatting"]) for x in res]
        snippets = [t(cleanhtml(x["content"])) for x in res]



class Google(CachedRequester):
    """
    scrape google search
    """
    _baseurl = "http://www.google.de/search?"

    def __extract_results(self, res):
        res_list = re.compile("""<li class="g">(.*?)</li>""", flags=re.DOTALL)
        res_link = re.compile("""<a href="/url\?q=(.*?)>(.*?)</a>""", flags=re.DOTALL)

        results = []
        for res_entry in res_list.findall(res):
            parts = res_link.findall(res_entry)
            if len(parts) != 0:
                p = parts[0]
                link = p[0]
                title = cleanhtml(p[1])
                results.append({"link": link, "title": title})
        return results

    def get_by_query(self, query, limit=9):
        if query is None:
            return []

        res = self._raw_request({"q": query}, waittime=random.randint(0, 10))
        results = self.__extract_results(res)

        for start in range(len(results), limit, 10):
            results = results + self.__extract_results(self._raw_request({"q": query, "start": start}, waittime=random.randint(0, 10)))

        return results

    def __remove_dups(self, a):
        """
        remove duplicate terms in a string a, e.g.
            "hello world hello" -> "hello world"
        """
        terms = a.split()
        res_terms = []
        for t in terms:
            if t not in res_terms:
                res_terms.append(t)
        return " ".join(res_terms)

    def get_related(self, query, entity="", mid=""):
        res = self.get_by_query(query) + self.get_by_query(entity)

        tidy = lambda x: " ".join(x.replace(":", " ").replace("?", " ").replace(".", " ").replace(",", "").replace("-", " ").split())

        # heuristic filter
        t = lambda x: " ".join([tidy(y) for y in x.split() if len(y) > 2]).lower()

        # heuristic remove term duplicates
        related_queries = [self.__remove_dups(t(x["title"])) for x in res]
        return list(set(related_queries))


def main(params):
    parser = argparse.ArgumentParser(description='google_api - send search requests to google and return resulting urls', epilog="stg7 2015")

    parser.add_argument('query', type=str, nargs='+', help='query')
    argsdict = vars(parser.parse_args())

    query = " ".join(argsdict["query"])
    lInfo(query)

    google = Google()
    results = google.get_by_query(query, 15)

    jPrint(results)

    print("\n\n")
    query = "solar power home"
    entity = "solar power"
    mid = "/m/05t0ydv"

    jPrint(google.get_related(query, entity, mid))



if __name__ == "__main__":
    main(sys.argv[1:])




