#!/bin/bash

if [ $# -ne 1 ]
then
	echo "使用方法： addftpuser 用户名"
	exit 1
fi 

ftpasswd --passwd --name $1 --file /etc/proftpd/ftpd.passwd --uid 500 --gid 500 --home /workdir/ --shell /bin/false

