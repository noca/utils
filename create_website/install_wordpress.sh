#!/bin/bash
#
# 安装 wordpress, 前提是 安装好 PHP + Nginx + Mysql 环境.
#
 

dir="/home/work"

# 下载
cd $dir ||exit 1
wget https://wordpress.org/latest.zip ||exit 1
unzip latest.zip


echo "访问 http://机器公网IP 进行进一步配置, 如果遇到需要填写 wordpress 数据库信息, 那么可以用 create_mysqldb.sh 来创建一个数据库."



