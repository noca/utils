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
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain", "Connection": "Keep-Alive"}

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
    keepalive(0)
    keepalive(31)
