import requests
import json
import base64
import random
import time
from Crypto.Cipher import AES

param2 = "010001"
param3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
param4 = "0CoJUm6Qyw8W8jud"


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    text = text.encode("utf-8")
    encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text.decode('utf-8')


def asrsea(p1, p2, p3, p4):
    res = {}
    rand_num = "aq9d7cvBOJ1tzj1o"
    vi = b"0102030405060708"
    h_encText = AES_encrypt(p1, p4, vi)
    h_encText = AES_encrypt(h_encText, rand_num, vi)
    res["encText"] = h_encText
    res[
        "encSecKey"] = "5dec9ded1d7223302cc7db8d7e0428b04139743ab7e3d451ae47837f34e66f9a86f63e45ef20d147c33d88530a6c3c9d9d88e38586b42ee30ce43fbf3283a2b10e3118b76e11d6561d80e33ae38deb96832b1a358665c0579b1576b21f995829d45fc43612eede2ac243c6ebb6c2d16127742f3ac913d3ac7d6026b44cee424e"
    return res


for i in range(11):
    curr_time = int(time.time() * 1000)
    param1 = json.dumps(
        {"csrf_token": "", "cursor": "%s" % curr_time, "offset": str(i * 20), "orderType": "2", "pageNo": str(i + 1),
         "pageSize": "20", "rid": "R_SO_4_29004400", "threadId": "R_SO_4_29004400"})

    asrsea_res = asrsea(param1, param2, param3, param4)

    url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Referer": "https://music.163.com/song?id=29004400",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://music.163.com",
        "Host": "music.163.com"
        }

    param_data = {"params": asrsea_res["encText"],
                  "encSecKey": asrsea_res["encSecKey"]}

    r = requests.post(url, headers=headers, data=param_data, verify=False)
    for comment in json.loads(r.text)["data"]["comments"]:
        print(comment["content"])
    break

d = '{"csrf_token":"e8948107444ec97f0991173f9118273d"}'
e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'