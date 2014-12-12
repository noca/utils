#!/bin/bash
#
# 安装 Nginx + PHP 环境.
# 完成之后 Nginx 配置在 /etc/nginx/conf.d/;
# PHP 代码放在 /home/${php_user} 下, 并修改 Nginx 配置, 然后 reload.
 

php_user="$1"
useradd $php_user

yum -y install nginx ||exit 1
yum -y install php-common php-cli php-pecl-memcache php-xmlrpc php-gd php-tidy php-xml php-pecl-apc php-pdo php-pear php-mysql php-mbstring php-fpm php-mcrypt php-devel ||exit 1


/bin/rm -rf /etc/nginx/conf.d/*
echo 'server {
    listen       80 ;
    # server_name  nosa.me;   # 此处修改成自己的域名, 并把注释去掉.

    access_log /var/log/nginx/access.log;   # 日志文件名可修改, 也可不修改.
    error_log /var/log/nginx/error.log;

    root  /home/work/wordpress;    # 此次修改成自己的程序主目录.
    index index.php;

    location / {
            try_files $uri $uri/ /index.php?$args;
    }

    location ~* \.(html|js|css|png|jpg|jpeg|gif|ico)$ {
        expires max;
    }

    location ~ \.php$ {
        fastcgi_pass   127.0.0.1:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
        include        fastcgi_params;
    }
}' > /etc/nginx/conf.d/default.conf

sed -i "s/expose_php =.*/expose_php = Off/g"  /etc/php.ini
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

/etc/init.d/nginx restart
/etc/init.d/php-fpm restart
chkconfig nginx on
chkconfig php-fpm on

