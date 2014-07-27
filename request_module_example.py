#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time


def main():
    url = "http://www.wandoujia.com"

    headers_dict = {"connection": "Keep-Alive"}
    r = requests.get(url, headers=headers_dict)
    # print r.status_code
    # print r.content
    # print r.encoding
    # print r.text

    # ret = r.__dict__
    # headers = ret["headers"]
    headers = r.headers

    # print headers
    # print headers["content-encoding"]
    print headers["connection"]

    r = requests.get(url, headers=headers_dict)
    headers = r.headers
    print headers["connection"]


if __name__ == "__main__":
    main()
