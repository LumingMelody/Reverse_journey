import time

import requests
from lxml import etree
from selenium import webdriver
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    "PDF文件名"
])
driver = webdriver.Chrome()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "cookie": "passport_web_did=6991686627378610179; _csrf_token=006d8b440983f6a55624c75ec805cbb723740b6b-1627878898; lang=zh; garr_version_list=%7B%7D; vt=1; et=d2559f22427792d90a4449b5947f79ba; ot=d2559f22427792d90a4449b5947f79ba; __tea__ug__uid=6991686625102710303; locale=zh-CN; trust_browser_id=45cd2fe3-f4fa-4e14-8ad3-54f0344741ed; _ga=GA1.2.2054286673.1627881995; _gid=GA1.2.1200040649.1627881995; fid=d51de26d-6ecf-4a26-9364-d46043764697; is_anonymous_session=; MONITOR_WEB_ID=6991700032240025602; template-branch-fixed=1; landing_url=https://passport.feishu.cn/suite/passport/page/login/?query_scope=all&app_id=2&should_pass_through=1&utm_from=organic_ccm_share_web&redirect_uri=https%3A%2F%2Fnnf1sjjavr.feishu.cn%2Fdrive%2Fhome%2F&template_id=6882649779491307521&biz=feishu_docs; session=XN0YXJ0-1d426122-efdd-4d76-9604-03d9f342b8bg-WVuZA; template-branch-list=; swp_csrf_token=2f8a4936-b2a1-42b5-8203-f905dc6d6610; t_beda37=8b0ccfcba972fa82b6088e7cd229575634347796047dcda911415bfb71b22f75"
}


driver.get("https://bytedance.feishu.cn/docs/doccn5H7f2DfWgDcwFDjnDHLwIe#")

time.sleep(2)

for i in range(4, 72):
    driver.find_element_by_xpath(f'//*[@id="mainContainer"]/div[3]/div[1]/div[2]/div[1]/div[1]/div/div/ul/li[{i}]/a').click()
    filenames = driver.find_elements_by_xpath("//ul[@class='list-bullet1 r-list r-list-bullet']/li/span[3]/span/span/a/span/text()")
    for filename in filenames:
        ws.append(filename.text)
        print(filename.text)
    time.sleep(10)
    js = 'window.scrollBy(0, 50)'
    driver.execute_script(js)

wb.save(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_03\PDF_name.xlsx")
# def get_filename(url):
#     resp = requests.get(url, headers=headers)
#     # print(resp.text)
#     html = etree.HTML(resp.text)
#     filenames = html.xpath("//ul[@class='list-bullet1 r-list r-list-bullet']/li/span[3]//span/text()")
#     for filename in filenames:
#         print(filename)


# if __name__ == '__main__':
    # url = "https://bytedance.feishu.cn/docs/doccn5H7f2DfWgDcwFDjnDHLwIe#"
    # get_filename(url)
# //ul[@class='list-bullet1 r-list r-list-bullet']/li/span[3]/span/span/a/span/text()