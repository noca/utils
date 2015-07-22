#!/bin/bash

OS_M_VERSION=`cat /etc/redhat-release | sed -e 's/^[^0-9]*\([0-9]\)\(\..*\)/\1/g'`
