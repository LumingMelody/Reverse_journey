import requests
from lxml import etree
import execjs


def get_key():
    url = "https://passport.wanmei.com/sso/login?service=passport&isiframe=1&location=2f736166652f"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Cookie": "JSESSIONID=17EEC8F4F6C01473D36A4EEAC726D4E2.passport1; Hm_lvt_ced744dfae7a0fe07aadbd98133e242b=1628232930; Hm_lpvt_ced744dfae7a0fe07aadbd98133e242b=1628232930; __mtxud=9edb05677404a5f2.1628232929529.1628232929529.1628232929529.1; __mtxsr=csr:www.baidu.com|cdt:/link|advt:(none)|camp:(none); __mtxcar=www.baidu.com:/link; uuid=BV4lkD5XRGSLxN8QD1gcaQ; sd=LXGVhM_QONzs8har84xGxvOwJMesoRHBZDpB97m9uPk; puclic_hg_flag2=true; __mtxsd=466ab24b.1628232962924.33395.2; Hm_lvt_2451e91cabdc44e0611c28a8ee93af90=1628232963; Hm_lpvt_2451e91cabdc44e0611c28a8ee93af90=1628232963"
    }
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)
    pub_key = html.xpath('//input[@id="e"]/@value')[0]
    return pub_key


def get_pwd(password):
    # pub_key = get_key()
    # print(pub_key)
    node = execjs.get()
    ctx = node.compile(open("./wanmei.js", "r", encoding='utf-8').read())
    pwd = ctx.call("getPwd", password)
    print(pwd)


if __name__ == '__main__':
    password = "123456"
    get_pwd(password)
