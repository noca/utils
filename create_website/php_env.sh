#!/bin/bash
#
# 安装 Nginx + PHP + Mysql 环境.
# 完成之后 Nginx 配置在 /etc/nginx/conf.d/;
# PHP 代码放在 /home/${php_user} 下, 并修改 Nginx 配置, 然后 reload.
# 使用 create_mysqldb.sh 建立数据库. 

. env.sh


# PHP 用户.
php_user="$1"
useradd $php_user


# 安装.
yum -y install nginx ||exit 1
yum -y install php-common php-cli php-pecl-memcache php-xmlrpc php-gd php-tidy php-xml php-pecl-apc php-pdo php-pear php-mysql php-mbstring php-fpm php-mcrypt php-devel ||exit 1
yum -y install libaio expect mysql mysql-server ||exit 1


# 配置 Nginx.
/bin/rm -rf /etc/nginx/conf.d/*
echo 'user              work;
worker_processes  2;

error_log  /var/log/nginx/error.log;
#error_log  /var/log/nginx/error.log  notice;
#error_log  /var/log/nginx/error.log  info;

pid        /var/run/nginx.pid;


events {
    worker_connections  65535;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;
    client_max_body_size 2048m;

    #gzip  on;
    
    # Load config files from the /etc/nginx/conf.d directory
    # The default server is in conf.d/default.conf
    include /etc/nginx/conf.d/*.conf;

}' > /etc/nginx/nginx.conf


# 配置 PHP.
sed -i "s/expose_php =.*/expose_php = Off/g"  /etc/php.ini
sed -i "s/post_max_size =.*/post_max_size = 20M/g" /etc/php.ini
sed -i "s/upload_max_filesize =.*/upload_max_filesize = 20M/g" /etc/php.ini
sed -i "s/apache/${php_user}/g" /etc/php-fpm.d/www.conf
sed -i "s/pm.max_children = 50/pm.max_children = 256/" /etc/php-fpm.d/www.conf
sed -i "s/pm.start_servers = 5/pm.start_servers = 32/" /etc/php-fpm.d/www.conf
sed -i "s/pm.min_spare_servers = 5/pm.min_spare_servers = 16/" /etc/php-fpm.d/www.conf
sed -i "s/pm.max_spare_servers = 35/pm.max_spare_servers = 64/" /etc/php-fpm.d/www.conf
sed -i "s/;pm.max_requests = 500/pm.max_requests = 2048/" /etc/php-fpm.d/www.conf
sed -i "s/;pm.status_path = \/status/pm.status_path = \/status/" /etc/php-fpm.d/www.conf
sed -i "s/;request_terminate_timeout = 0/request_terminate_timeout = 5s/" /etc/php-fpm.d/www.conf
sed -i "s/;request_slowlog_timeout = 0/request_slowlog_timeout = 5s/" /etc/php-fpm.d/www.conf
sed -i "s/^rlimit_files =.*/rlimit_files = 65535/" /etc/php-fpm.d/www.conf
sed -i "s/^apc.shm_size=.*/apc.shm_size=256M/g" /etc/php.d/apc.ini
sed -i "/short_open_tag/s/Off/On/g" /etc/php.ini
sed -i "s/.*date\.timezone.*/date\.timezone=Asia\/Shanghai" /etc/php.ini


# 启动程序

if [ $OS_M_VERSION -eq 7 ]; then
    systemctl start nginx
    systemctl start php-fpm
    systemctl start mysqld
else
    /etc/init.d/nginx restart
    /etc/init.d/php-fpm restart
    /etc/init.d/mysqld start
fi


# 配置 Mysql.
#/usr/bin/mysqladmin -u root password 'wandoujia!+234'
#grant all on *.* to ncdba@'localhost' identified by 'ncdba-+123' with grant option;
/usr/bin/expect -c "
set timeout 10
spawn mysql -uroot -hlocalhost
expect \"mysql>\"
send \"grant all on *.* to root@'localhost' identified by 'hell04321' ; \r\"
expect \"mysql>\"
send \"flush privileges ; \r\"
expect \"mysql>\"
send \"exit \r\"
expect eof
"


# 开机启动.

if [ $OS_M_VERSION -eq 7 ]; then
    systemctl enable nginx
    systemctl enable php-fpm
    systemctl enable mysqld
else
    chkconfig nginx on
    chkconfig php-fpm on
    chkconfig mysqld on
fi
