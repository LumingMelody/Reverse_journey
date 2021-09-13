# -*- coding: UTF-8 -*-
"""
@author:AmoXiang
@file:steam.py
@time:2020/12/11
"""

import requests
import execjs

# TODO 1. 获取 publickey_mod, publickey_exp
url = "https://store.steampowered.com/login/getrsakey/"
form_data = {
    "donotcache": "1628149001019",
    "username": "xushaomei"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (K"
                  "HTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Referer": "https://store.steampowered.com/login/?redir=&redir_ssl=1",
    "Cookie": "browserid=2492153338320958144; timezoneOffset=28800,0; _ga=GA1.2.1931609162.1616572260; steamCountry=CN%7Cefa7bbadb9f3078361dbd023f18d64f2; sessionid=1e5fa224446cbb3e90f0262d; _gid=GA1.2.248463524.1628148517"
}
response = requests.post(url=url, headers=headers, data=form_data)  # 注意是post请求
data = response.json()
publickey_exp = data["publickey_exp"]
publickey_mod = data["publickey_mod"]
print(publickey_exp, publickey_mod)
# TODO 2. 加密
node = execjs.get()  # 实例化一个对象
ctx = node.compile(open("./steam.js", "r", encoding="utf8").read())  # 编译
funcName = 'getPwd("{0}","{1}","{2}")'.format('123456', publickey_mod, publickey_exp)
pwd = ctx.eval(funcName)
print(pwd)
