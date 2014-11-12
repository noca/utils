#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
    WEB服务器的 keepalive_timeout 是30s
"""

import urllib
import httplib
import time


def keepalive(t):
    url = "www.wandoujia.com"
    conn = httplib.HTTPConnection(url)

    conn.request("GET", "/")
    ret = conn.getresponse()
    print ret.status, ret.reason
    data = ret.read()

    time.sleep(t)

    conn.request("GET", "/")
    ret = conn.getresponse()
    print ret.status, ret.reason
    data = ret.read()

    conn.close()


if __name__ == "__main__":
    keepalive(15)
    keepalive(31)