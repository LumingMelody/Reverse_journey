import execjs
from Crypto.Cipher import AES


def get_pwd(p):
    ctx = execjs.compile(open("./changfang.js", "r", encoding='utf-8').read())
    password = ctx.call("getPwd", p)
    print(password)
# def get_pwd(p):
#     mode = AES.MODE_CBC
#     str1 = "D9016ABEB39EBDBB43EB57B4BBF41FAB"
#     if len(str1) < 32:
#         str1 += "abcdefghijklmnopqrstuvwxyz1234567890"
#     key = str1[0:16]
#     iv = str1[16:32]
#     print(len(iv))
#     security = "\u4435\u5320\u4d35"
#     cryptos = AES.new(key.encode('utf-8'), mode, iv.encode('utf-8'))
#     # print(bytes(p.encode('utf-8')))
#     pwd = cryptos.encrypt(bytes(p.encode('utf-8')))
#     print(pwd)


if __name__ == '__main__':
    pwd = "123456"
    get_pwd(pwd)
