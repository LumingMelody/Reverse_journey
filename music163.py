# 1. 找到未加密的参数
# 2. 想办法把参数进行加密（必须参考网易的逻辑） ，params => encText, encSecKey => encSecKey
# 3. 请求到网易，拿到评论信息

# pip install pycryptodome
from Crypto.Cipher import AES
from base64 import b64encode
from bs4 import BeautifulSoup
import requests
import json

url = "https://music.163.com/weapi/comment/resource/comments/get"
# 请求方式是POST
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_167827",
    "threadId": "R_SO_4_167827"
}

# 单曲歌 R_SO_4_1313118277
# 歌单 "A_PL_0_2022186054"
# rid和threadId为 R_SO_4_ + 歌曲ID拼接而成

# 服务于d函数的
e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = 'nYXLafpydDFlqRNh'  # 手动固定，人家的是随机的


def get_encSecKey():  # 由于i，e，f固定，那么c函数结果固定
    return "8f2960e5fa10ec2f643aa6a9f76f6b40f85dc4e0f7cfadc70370991ffa3234b08987d5f684619660448a8f0880dbc34436011b1f5b1091d1de4b448acc8ae259d71f84573229ade8ed9894ea55ebbfb6cd1a92e827c93ae14f5af34bdd994c004286dfa3fee40c12cf1d9da5cc3a33313a9f6b19cb10f1eb28d45d9cb8933590"


# 转化成16的倍数，为下方加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def enc_params(data, key):  # 加密过程
    iv = '0102030405060708'
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), iv=iv.encode('utf-8'), mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode('utf-8'))  # 加密，加密的内容的长度必须是16的倍数，AES加密的逻辑
    # bs的结果不能直接转换成字节,需要先转换成base64

    return str(b64encode(bs), 'utf-8')  # 转换成字符串返回


# 把参数进行加密
def get_params(data):  # data为json字符串
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second


# 处理加密过程
'''
function a(a) {  # 参数传为16
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)  # 循环16次
            e = Math.random() * b.length,   # 随机数  
            e = Math.floor(e),  # 取整
            c += b.charAt(e);   # 取在字符串b中的XXX位置
        return c                # 产生16位随机的字母或数字
    }
    function b(a, b) {   # a是要加密的内容
        var c = CryptoJS.enc.Utf8.parse(b)    # b是密钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)   # e是数据
          , f = CryptoJS.AES.encrypt(e, c, {  # c是加密的密钥
            iv: d,   # 偏移量
            mode: CryptoJS.mode.CBC  # 加密模式：CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {   d:数据，e:010001，f:很长的定值，e:定值
        var h = {}   # 空对象
          , i = a(16);  # i就是一个16位的随机值，我们可以把i设置成定值
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
    上面那部分相当于
        h.encText = b(d, g),          # g是密钥
        h.encText = b(h.encText, i),  # 得到的就是params   i也是密钥
        h.encSecKey = c(i, e, f),      # 得到的就是encSecKey，e和f是定死的，如果此时把i固定，c函数返回的值也是固定的
        return h
    window.asrsea = d
    .....
    var bKf6Z = window.asrsea(JSON.stringify(i8a), bva3x(["流泪", "强"]), bva3x(Tu8m.md), bva3x(["爱心", "女孩", "惊恐", "大笑"]));
    bva3x(["流泪", "强"])运算结果为：010001
    bva3x(Tu8m.md)运算结果为：00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
    bva3x(["爱心", "女孩", "惊恐", "大笑"])运算结果为：0CoJUm6Qyw8W8jud

'''


def get_comment(s_id, page_num):
    # 发送请求得到评论
    data['rid'] = f'R_SO_4_{s_id}'
    data['threadId'] = f'R_SO_4_{s_id}'
    data['pageNo'] = page_num + 1
    resp = requests.post(url, data={
        'params': get_params(json.dumps(data)),
        'encSecKey': get_encSecKey()
    })
    resp_data = json.loads(resp.text)['data']
    print(resp_data)
    for result in resp_data['comments']:
        comment_user = result['user']['nickname']
        comment = result['content']
        print(comment_user + ':' + comment)
    # 获取热评
    # hotComments = resp_data['hotComments']
    # if hotComments == None:
    #     print('数据为空')
    #     return


if __name__ == '__main__':
    # 歌曲ID
    song_id = '167827'
    # range里面的参数是要抓取的页数
    for page_num in range(10):
        get_comment(song_id, page_num)
