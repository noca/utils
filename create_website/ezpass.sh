#!/bin/bash

pass=`echo $1 | md5sum | base64| cut -c1-8`

echo "$1: $pass"
