webapis
=======
[TOC]

authors:
> stg7@gmx.de

About
-----
A few web api tools for search request to different webservices. All request will be cached, therefore server traffic is reduced.

First Start
-----------
For some of the webservices you need API keys, that were configured in `api_keys.json` or
can be setted in each instance with `set_api_key(KEY)`

The easy way is to create the `api_keys.json` file with the following content, you can use `api_keys.json.example`:
```
{
    "freebase": "KEY",
    "chatnoir2": "dev",
    "chatnoir": "KEY"
}
```

Webservices
-----------

* [chatnoir](http://chatnoir.webis.de) & chatnoir2 (non public)
* [freebase](https://www.freebase.com/) & [wikidata](https://www.wikidata.org): semantic web search requests
* [google](https://google.com): google search scraped form html page
* [netspeak](http://netspeak.org): ngram queries
* [querysegmentation](http://webis16.medien.uni-weimar.de:8080/query-segmentation-server/): segments queries
* [whatismyip](https://www.whatismyip.com/)

Example run
-----------
Just call:
```
./example.py hello world
```

and you will get something like:
```
wikidata
{
    "search": [
        {
            "id": "Q2471943",
            "label": "Hello World",
            "match": {
                "language": "en",
                "text": "Hello World",
                "type": "label"
            },
            "url": "//www.wikidata.org/wiki/Q2471943"
        },
        .....
    ],
    "searchinfo": {
        "search": "hello world"
    },
    "success": 1
}
querysegmentation
{
    "hyb-a": "hello|world",
    "hyb-b": "hello|world",
    "hyb-i": "hello|world",
    "naive": "hello|world",
    "wiki-based": "hello|world",
    "wt-baseline": "hello|world",
    "wt-snp-baseline": "hello|world"
}
google
[
    {
        "link": "https://de.wikipedia.org/wiki/Hallo-Welt-Programm&amp;sa=U&amp;ved=0CBQQFjAAahUKEwjBjJnCvrfHAhVJNxQKHf-8BMs&amp;usg=AFQjCNEC-7j-QshsfJN5sDttc_1DtYuIKw\"",
        "title": "Hallo-Welt-Programm  Wikipedia"
    },
    ...
]

```

as output.