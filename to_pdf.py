import json
import re
import time

import pandas as pd
import pdfkit
import requests
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook

wb = Workbook()
wb1 = Workbook()

ws = wb.active
ws1 = wb1.active
ws.append([
    "微信链接"
])

ws1.append([
    "PDF下载链接"
])

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "cookie": "passport_web_did=6991686627378610179; _csrf_token=006d8b440983f6a55624c75ec805cbb723740b6b-1627878898; lang=zh; garr_version_list=%7B%7D; vt=1; et=d2559f22427792d90a4449b5947f79ba; ot=d2559f22427792d90a4449b5947f79ba; __tea__ug__uid=6991686625102710303; locale=zh-CN; trust_browser_id=45cd2fe3-f4fa-4e14-8ad3-54f0344741ed; _ga=GA1.2.2054286673.1627881995; _gid=GA1.2.1200040649.1627881995; fid=d51de26d-6ecf-4a26-9364-d46043764697; is_anonymous_session=; MONITOR_WEB_ID=6991700032240025602; template-branch-fixed=1; landing_url=https://passport.feishu.cn/suite/passport/page/login/?query_scope=all&app_id=2&should_pass_through=1&utm_from=organic_ccm_share_web&redirect_uri=https%3A%2F%2Fnnf1sjjavr.feishu.cn%2Fdrive%2Fhome%2F&template_id=6882649779491307521&biz=feishu_docs; session=XN0YXJ0-1d426122-efdd-4d76-9604-03d9f342b8bg-WVuZA; template-branch-list=; swp_csrf_token=2f8a4936-b2a1-42b5-8203-f905dc6d6610; t_beda37=8b0ccfcba972fa82b6088e7cd229575634347796047dcda911415bfb71b22f75"
}


def get_yuanrenyun_ip():
    # 代理隧道验证信息
    # url = "http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=&gm=4"
    url = "http://d.jghttp.alicloudecs.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=4&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&username=chukou01&spec=1"
    resp = requests.get(url).json()
    print(resp)
    ip = resp["data"][0]["ip"]
    port = resp["data"][0]["port"]
    meta = "http://%(host)s:%(port)s" % {
        "host": ip,
        "port": port,
    }
    proxies = {
        "http": meta,
        "https": meta
    }
    # print(proxies)
    return proxies


options = {
    'page-size': 'A4',
    #     'margin-top': '0.75in',
    #     'margin-right': '0.75in',
    #     'margin-bottom': '0.75in',
    #     'margin-left': '0.75in',
    'encoding': "UTF-8",
    #      'custom-header': headers,
    #     'debug-javascript': [''],
    #     'javascript-delay': 10000,
    #     'no-stop-slow-scripts': "",
    #     'load-media-error-handling': 'abort',
}


def get_ip():
    resp = requests.get(
        "http://lumingmelody.v4.dailiyun.com/query.txt?key=NP2908A5A2&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false")
    # print(resp.text)
    proxy = {
        'http://': f'{resp.text}',
        'https://': f'{resp.text}'
    }
    return proxy


def weixin_to_pdf(url):
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)
    t = html.xpath('//*[@id="activity-name"]/text()')
    title = (''.join(str(i) for i in t)).strip()
    print(title)
    config = pdfkit.configuration(wkhtmltopdf=r'D:\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(get_html(url), f'./巨量PDF/{title}.pdf', configuration=config, options=options)
    time.sleep(3)


def down_load(d_id, d_url):
    p_url = f"https://bytedance.feishu.cn/space/api/meta/?token={d_id}&type=12"
    proxies = get_ip()
    resp = requests.get(p_url, headers=headers, proxies=proxies).json()
    print(resp)
    time.sleep(3)
    title = resp['data']['title']
    response = requests.get(d_url, headers=headers)
    with open(f"./巨量PDF1/{title}", mode='wb') as f:
        f.write(response.content)
    time.sleep(3)


def get_html(url):
    res = requests.get(url)
    # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
    html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"', "")

    soup = BeautifulSoup(html)
    # 选择正文（去除javascrapt等）
    html = soup.select('div#img-content')[0]

    # 可以修改字体
    font = '''
    <style type="text/css">
         @font-face{font-family: "微软雅黑";src:url("‪C:\\Windows\\Fonts\\msyh.ttc")
    </style>
     <style type = "text/css">
        p { font-family: '微软雅黑', cursive; }
    </style>
    '''
    html = font + str(html)
    return html


if __name__ == '__main__':
    df = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_02\PDF下载链接.xlsx")
    urls = df['PDF下载链接']
    # df = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_03\未下载微信链接.xlsx")
    # urls = df['未下载微信链接']
    # # url = "https://mp.weixin.qq.com/s?__biz=MzUxNTk5NjY4MQ==&amp;mid=2247485533&amp;idx=1&amp;sn=8f5121e99ee6531eb8ce45bed4f5f4a0&amp;chksm=f9af653bced8ec2dbddc6cc7e8ee15a6d3875b32331b1480e891e987a5f3c7f5117042185b32&amp;token=1252715679&amp;lang=zh_CN#rd"
    for url in urls:
        # weixin_to_pdf(url)
        d_id = url.split("/")[-2]
        # print(d_id)
        down_load(d_id, url)
    # down_load("boxcn3f4uFHxMDV4cA9wIbcUGQi", "https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/all/boxcnZr2Ucnj0HKfnA8oDGyLSEd/")
