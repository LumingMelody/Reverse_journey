import requests
from hashlib import md5
import time
import random

appVersion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "244",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "OUTFOX_SEARCH_USER_ID=-1506602845@10.169.0.82; JSESSIONID=aaaUggpd8kfhja1AIJYpx; OUTFOX_SEARCH_USER_ID_NCOO=108436537.92676207; ___rl__test__cookies=1597502296408",
    "Host": "fanyi.youdao.com",
    "Origin": "http://fanyi.youdao.com",
    "Referer": "http://fanyi.youdao.com/",
    "user-agent": appVersion,
    "X-Requested-With": "XMLHttpRequest",
}


def r(e):
    # bv
    t = md5(appVersion.encode()).hexdigest()

    # lts
    lts = str(int(time.time() * 1000))

    # i
    i = lts + str(random.randint(0, 9))

    return {
        "ts": r,
        "bv": t,
        "salt": i,
        "sign": md5(("fanyideskweb" + e + i + "Y2FYu%TNSbMCxc3t2u^XT").encode()).hexdigest()
    }


def fanyi(word):
    data = r(word)
    params = {
        "i": word,
        "from": "UTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": data["salt"],
        "sign": data["sign"],
        "lts": data["ts"],
        "bv": data["bv"],
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }

    response = requests.post(url=url, headers=headers, data=params)
    # 返回json数据
    return response.json()


if __name__ == '__main__':
    word = "蔡徐坤"
    result = fanyi(word)

    # 对返回的json数据进行提取，提取出我们需要的数据
    r_data = result["translateResult"][0]
    print(r_data[0]["src"])
    print(r_data[0]["tgt"])
