import re
import time
import execjs
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Cookie": "SSO-KGZQRT=10BE96BC08BB9353B6FFDA21EBE27BC8; KZLBS=d7d10e488a0e2047; Hm_lvt_1287c2225a527abe3386233dd9316f99=1628492118; Hm_lpvt_1287c2225a527abe3386233dd9316f99=1628492118; SSO-KGZLT=3ddc4eab-87e7-4fff-8cf7-6af3c8028f7b; SSO-KGZIT=475cf876-eb30-4a51-9d5b-a3f109be1696",
    "Referer": "https://passport.kongzhong.com/"
}


def get_dc():
    ts = str(time.time()).split(".")[0]
    url = f"https://sso.kongzhong.com/ajaxLogin?j=j&&type=1&service=https://passport.kongzhong.com/&username=123@qq.com&password=313d7013daa400a3c1f3&vcode=v03s&toSave=0&_={ts}"
    resp = requests.get(url, headers=headers).text
    print(resp)
    ex = r'KZLoginHandler.jsonpCallbackKongZ\((.*?)\)'
    dc = re.findall(ex, resp)[0]
    json_data = json.loads(dc)
    return json_data['dc']


def get_pwd(p):
    dc = get_dc()
    ctx = execjs.compile(open('./kongzhong.js', "r", encoding='utf-8').read())
    pwd = ctx.call("getPwd", p, dc)
    print(pwd)


if __name__ == '__main__':
    password = "123456"
    get_pwd(password)
