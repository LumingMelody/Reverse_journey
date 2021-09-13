from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import cv2 as cv
import numpy as np

# -------------------------------------爬取滑块验证码中的两个图片
# 创建浏览器
web = Chrome()

# 获取网站
web.get('https://dun.163.com/trial/sense')

# 寻找可疑用户-滑动拼图按钮，点击，由于加载较慢，需要设置一两秒的等待
web.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[2]/ul/li[2]').click()
time.sleep(1.5)

# 寻找点击完成验证按钮块，点击，由于加载较慢，需要设置一两秒的等待
web.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[1]').click()
time.sleep(2)

# 寻找滑块图片和缺失背景图片的url地址
bg_img_src=web.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div[1]/img[1]').get_attribute('src')

front_img_src=web.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div[1]/img[2]').get_attribute('src')

# 将这两个图片根据url，下载到本地
with open('bg.jpg','wb') as f:
    f.write(requests.get(bg_img_src).content)
with open('front.jpg','wb') as f:
    f.write(requests.get(front_img_src).content)

# ----------------------------------------处理图片，寻找豁口
# 读取图片
bg = cv.imread('bg.jpg')
front = cv.imread('front.jpg')

# 灰度处理，是为了提高我们的效率，类似于降维打击
bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)  # 将blue，green，red转为gray
front = cv.cvtColor(front, cv.COLOR_BGR2GRAY)  # 将blue，green，red转为gray

# 对滑块处理，我们下载出来滑块图片，发现上下多了一对空白，经过灰度会将此空白变成黑色，如果用此图片匹配背景会有问题，因此需要切除
front = front[front.any(1)]  # 1是要灰度后边比较亮的，黑色就是暗的数字0，因此这样做会将小块儿留下来

# 用滑块匹配背景图
# cv.TM_CCOEFF_NORMED算法，匹配精度最高，时间最慢，会将滑块每个像素点与背景图像素对比，返回一个每个像素点匹配相似度的矩阵，寻找相似度最大的
result = cv.matchTemplate(bg, front, cv.TM_CCOEFF_NORMED)
yiwei_max_loc = np.argmax(result)  # 返回矩阵的最大一维位置，但是我们需要二维的位置
x, y = np.unravel_index(yiwei_max_loc, result.shape)  # 会将一维的位置逆向根据二维的形状，返回位置横纵坐标

# 我们这个滑块验证码只需要移动横坐标
# 寻找移动的滑块
div = web.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[2]')

# 引入动作链发生在哪个浏览器,drag_and_drop_by_offset方法是抓住块移动多少再放下
# 但是OpenCV比较奇葩，纵坐标和横坐标相反，在我们人的横坐标移动是OpenCV的纵坐标移动
# 如果浏览器没动静，可能我们下载得图片和原来的网页图片大小比例不同，需要自己算比例，然后对移动值计算
# 当然此方法不一定100%可以过去
ActionChains(web).drag_and_drop_by_offset(div,xoffset=y,yoffset=0).perform()

