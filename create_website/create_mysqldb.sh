#!/bin/bash
#
# 建立一个 Mysql 数据库.
#
 

read -p "输入数据库名称: " mysqldb
echo 
echo "您输入的数据库名称是: $mysqldb "
echo 
echo "开始创建数据库..."
echo


sleep 1


#/usr/bin/mysqladmin -u root password 'wandoujia!+234'
#grant all on *.* to ncdba@'localhost' identified by 'ncdba-+123' with grant option;
/usr/bin/expect -c "
set timeout 10
spawn mysql -uroot -hlocalhost -phell04321
expect \"mysql>\"
send \"create database $mysqldb ; \r\"
expect \"mysql>\"
send \"grant all on *.* to example@'localhost' identified by 'hell04321' ; \r\"
expect \"mysql>\"
send \"grant all on *.* to example@'10.%' identified by 'hell04321' ; \r\"
expect \"mysql>\"
send \"flush privileges ; \r\"
expect \"mysql>\"
send \"exit \r\"
expect eof
"

echo "数据库创建完成..."
echo 
echo "数据库名称是: $mysqldb"
echo "用户名是    : example"
echo "密码是      : hell04321"
echo 
echo "您需要修改 [程序数据库配置] 来使得程序可以连接数据库."
echo

