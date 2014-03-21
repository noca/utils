#!/usr/bin/env python

import re


def isValidIp(ip):
    """
    检查ip是否合法.
    """

    p = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    s = p.findall(ip.strip())
    if s == []:
        return False

    return len([i for i in s[0].split('.') if (0 <= int(i) <= 255)]) == 4

if __name__ == '__main__':
    print isValidIp("10.0.0.1")
