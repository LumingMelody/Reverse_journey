import requests
import execjs
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}
url = "http://login.shikee.com/getkey?v=f35d09f500ab8959dbd7ae6ed851867a"


def get_rsa_n():
    resp = requests.get(url, headers).text
    # rsa_n = str(resp).replace("var rsa_n =", "").replace(";", "").replace('"', '')
    ex = r'var rsa_n = "(.*?)";'
    rsa_n = re.findall(ex, resp)[0]
    print(rsa_n)
    return rsa_n


def get_pwd(pwd):
    rsa_n = get_rsa_n()
    ctx = execjs.compile(open("./shike.js", "r", encoding='utf-8').read())
    password = ctx.call("getPwd", pwd, rsa_n)
    print(password)


if __name__ == '__main__':
    get_pwd("123456")
