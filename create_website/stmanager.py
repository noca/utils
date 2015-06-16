#!/usr/bin/env python
# -*- coding: utf-8 -*-

ngx_dir = '/etc/nginx/conf.d/'
php_dir = '/home/work/sites/'
ngx_exec = '/etc/init.d/nginx'


import sys
import os
import shutil
from string import Template


def usage():
    print '''
    Usage: stmanager add    网站域名
           stmanager delete 网站域名
           stmanager list
    '''
    exit(1)


class SiteOperation(object):
    _ngx_dir = ngx_dir
    _php_dir = php_dir

    def __init__(self, domain):
        self._domain = domain

    def add(self):
        config_template = Template('''
        server {
            listen       80 ;
            server_name  $server_name;
            access_log /var/log/nginx/$server_name-access.log;
            error_log /var/log/nginx/$server_name-error.log;

            root  $php_dir$server_name;
            index index.php index.html index.htm;
            location / {
                try_files $$uri $$uri/ /index.php?$$args;
            }
            location ~* \.(html|js|css|png|jpg|jpeg|gif|ico)$$ {
                expires max;
            }
            location ~ \.php$ {
                fastcgi_pass   127.0.0.1:9000;
                fastcgi_index  index.php;
                fastcgi_param  SCRIPT_FILENAME  $$document_root$$fastcgi_script_name;
                include        fastcgi_params;
            }
        }
        ''')
        config = config_template.safe_substitute(
            server_name=self._domain,
            php_dir=self._php_dir
        )
        
        if not os.path.exists(self._ngx_dir):
            print "Nginx 的配置文件 %s 目录不存在" % \
                self._ngx_dir
            return False
        
        site_dir = self._php_dir + self._domain
        if not os.path.exists(site_dir):
            os.makedirs(site_dir)
            # use work as site user
            os.chown(site_dir, 500, 500)

        config_file = self._ngx_dir + self._domain \
                      + ".conf"
        with open(config_file, 'w') as f:
            f.write(config)
    
        return True

    def delete(self):
        config_file = self._ngx_dir + self._domain \
                      + ".conf"
        if os.path.exists(config_file):
            os.remove(config_file)
        
        site_dir = self._php_dir + self._domain
        if os.path.exists(site_dir):
            shutil.rmtree(site_dir)

        return True

    @classmethod
    def list(self):
        configs = os.listdir(self._ngx_dir)
        configs = [c[:-5] for c in configs]
        sites = os.listdir(self._php_dir)
        
        real_sites = set(configs).intersection(
            sites)
        print "已有网站:\n"
        for s in real_sites:
            print "\t%s\n" % s
        
        return True

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] in ['add', 'delete']:
        op = sys.argv[1]
        domain = sys.argv[2]

        site = SiteOperation(domain)
        getattr(site, op)()
        os.system(ngx_exec + " reload")
    elif len(sys.argv) == 2 and sys.argv[1] in ['list']:
        SiteOperation.list()
    else:
        usage()
