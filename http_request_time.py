#!/usr/bin/python
#-*- coding: utf-8 -*-


"""
    Reference: http://curl.haxx.se/libcurl/c/curl_easy_getinfo.html

    pycurl.NAMELOOKUP_TIME 域名解析时间
    pycurl.CONNECT_TIME 远程服务器连接时间
    pycurl.PRETRANSFER_TIME 连接上后到开始传输时的时间
    pycurl.STARTTRANSFER_TIME 接收到第一个字节的时间
    pycurl.TOTAL_TIME 上一请求总的时间
    pycurl.REDIRECT_TIME 如果存在转向的话，花费的时间

    pycurl.EFFECTIVE_URL
    pycurl.HTTP_CODE HTTP 响应代码
    pycurl.REDIRECT_COUNT 重定向的次数
    pycurl.SIZE_UPLOAD 上传的数据大小
    pycurl.SIZE_DOWNLOAD 下载的数据大小
    pycurl.SPEED_UPLOAD 上传速度
    pycurl.HEADER_SIZE 头部大小
    pycurl.REQUEST_SIZE 请求大小
    pycurl.CONTENT_LENGTH_DOWNLOAD 下载内容长度
    pycurl.CONTENT_LENGTH_UPLOAD 上传内容长度
    pycurl.CONTENT_TYPE 内容的类型
    pycurl.RESPONSE_CODE 响应代码
    pycurl.SPEED_DOWNLOAD 下载速度
    pycurl.SSL_VERIFYRESULT
    pycurl.INFO_FILETIME 文件的时间信息
"""

import pycurl
import sys


class body_callback:

    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf


def http_request_time(input_url):
    cb = body_callback()
    c = pycurl.Curl()
    c.setopt(pycurl.WRITEFUNCTION, cb.body_callback)
    c.setopt(pycurl.ENCODING, 'gzip')
    c.setopt(pycurl.URL, input_url)
    c.perform()

    http_code = c.getinfo(pycurl.HTTP_CODE)
    http_namelookup_time = c.getinfo(pycurl.NAMELOOKUP_TIME)
    http_conn_time = c.getinfo(pycurl.CONNECT_TIME)
    http_pre_tran = c.getinfo(pycurl.PRETRANSFER_TIME)
    http_start_tran = c.getinfo(pycurl.STARTTRANSFER_TIME)
    http_total_time = c.getinfo(pycurl.TOTAL_TIME)
    http_size = c.getinfo(pycurl.SIZE_DOWNLOAD)

    result_dict = {
        "http_code": http_code,
        "namelookup_time": http_namelookup_time,
        "http_size": http_size,
        "conn_time": http_conn_time,
        "pre_tran": http_pre_tran,
        "start_tran": http_start_tran,
        "total_time": http_total_time,
        "http_size": http_size
    }

    return result_dict


if __name__ == '__main__':
    input_url = sys.argv[1]
    print http_request_time(input_url)
