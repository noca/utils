#!/usr/bin/env python

import subprocess


def shell(cmd):
    process = subprocess.Popen(
        args=cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = process.communicate()
    return_code = process.poll()
    return return_code, std_out, std_err

if __name__ == '__main__':
    import sys
    rc, so, se = shell(sys.argv[1])
    print "rc=%d" % rc
    print "so=%s" % so
    print "se=%s" % se
