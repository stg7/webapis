#!/usr/bin/env python3
"""
    Webutils

    Copyright 2015-today

    Author: Steve Göring
    Contact: stg7@gmx.de
"""

import os
import urllib.request
import shelve
import json
import re
import time
import string

class CachedRequester(object):
    _baseurl = None
    _api_key = ""
    __cache = None

    def __init__(self):
        classname = self.__class__.__name__.lower()
        self.__cache = shelve.open(os.path.dirname(os.path.realpath(__file__)) + "/_" + classname + "_cache")
        if self._baseurl == None:
            raise Exception("you must set baseurl to a valid value in each subclass")
        cfg = self.__load_config()
        self.set_api_key(cfg.get(classname, ""))

    def __del__(self):
        if self.__cache is not None:
            self.__cache.close()

    def set_api_key(self, api_key):
        self._api_key = api_key

    def _raw_request(self, params={}, baseurl="", waittime=0):
        if baseurl == "":
            baseurl = self._baseurl
        k = json.dumps(params,sort_keys=True) + baseurl
        if k in self.__cache:
            return self.__cache[k]

        time.sleep(waittime)
        url_values = urllib.parse.urlencode(params)
        req = urllib.request.Request(baseurl + url_values, headers={'User-Agent': 'Mozilla'})

        handle = urllib.request.urlopen(req, timeout=120)

        encoding = handle.headers.get_content_charset()

        try:
            content = str(handle.read().decode("latin-1"))
        except:
            content = str(handle.read().decode(encoding, errors='ignore'))

        result = ' '.join(content.split())
        self.__cache[k] = result

        return result

    def _request(self, params={}, baseurl="", waittime=0):
        """
        do a rest request and parse json result
        """
        if None in params.values() or len(params) == 0:
            return {}

        result = self._raw_request(params, baseurl, waittime)

        return json.loads(result)

    def _request_post(self, params={}, baseurl=""):
        """
        do a rest request and parse json result
        """
        if None in params.values() or len(params) == 0:
            return {}

        if str(params) + baseurl in self.__cache:
            return self.__cache[str(params) + baseurl]

        if baseurl == "":
            baseurl = self._baseurl

        data = bytes(urllib.parse.urlencode(params), "utf-8")
        req = urllib.request.Request(baseurl)

        handle = urllib.request.urlopen(req, data, timeout=120)
        content = str(handle.read().decode('utf-8', errors='ignore'))
        result = ' '.join(content.split())
        self.__cache[str(params)] = json.loads(result)

        return self.__cache[str(params)]

    def get_by_query(self, query):
        raise Exception("you must overrice get_by_query in each subclass")

    def get_related(self, query, entity="", mid=""):
        raise Exception("you must overrice get_related in each subclass")

    def __load_config(self):
        configfilename = os.path.dirname(os.path.realpath(__file__)) + "/api_keys.json"
        if not os.path.isfile(configfilename):
            raise Exception("api_key.json file is not aviable")

        f = open(configfilename)
        content = "".join(f.readlines())
        f.close()
        try:
            config = json.loads(content)
        except Exception as e:
            raise Exception("api_key.json file is not valid")

        return config


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', raw_html)
    from html import unescape

    tmp = unescape(cleantext.replace("\n", " "))

    filtered_string = ""
    for x in tmp:
        if x in string.printable:
            filtered_string += x

    return filtered_string


def lInfo(x):
    print(x)

def jPrint(x, output=True):
    str_x = json.dumps(x, indent=4, sort_keys=True)
    if output:
        lInfo(str_x)
    return str_x

if __name__ == "__main__":
    print("module is not a standalone module")
