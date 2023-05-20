import time
import ntplib
import datetime
import requests
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.edge.options import Options

# 一些变量，不用修改
# 用于记录ntp服务器时间和本地时间差值,启动时会进行一次计算,后续获取时间采用读本次时间+差值的方法作为NTP服务器时间
time_gap = 0
# 拍牌页面链接
page_url = 'https://paimai2.alltobid.com/bid?type=individual'
# 今天的11点29分0秒时间
time_11_29 = datetime.datetime.today().replace(hour=18, minute=29, second=0, microsecond=0)

# 出价策略设置，修改下面的值 #
'''
修改下面这部分的出价值和出价时间设置策略，脚本默认出价两次，如下默认配置表示：
第一次在11点29分30秒加价300并点击出价，然后你需要手动输入验证码并提交
第二次在11点29分45秒加价800并点击出价，然后11:29:55+0.5秒时自动点击提交，在这之前你需要输入好验证码并等待
'''
# 第一次出价的加价值
first_add_price_num = 300
# 第一次出价时间
first_add_price_time = int(time.mktime((time_11_29+datetime.timedelta(seconds=30)).timetuple()))
# 第二次出价的加价值
second_add_price_num = 800
# 第二次出价时间
second_add_price_time = int(time.mktime((time_11_29+datetime.timedelta(seconds=45)).timetuple()))
# 第二次确认时间，时间格式化只能到秒，所以用浮点数，可以在秒上在延迟0.x秒
submit_time = time.mktime((time_11_29+datetime.timedelta(seconds=55)).timetuple()) + 0.5


def init_time():
    global time_gap
    response = ntplib.NTPClient().request('ntp.aliyun.com')
    # https://www.cnpython.com/qa/356322
    ts = response.tx_time + (response.recv_time - response.orig_time + response.dest_time - response.tx_time) / 2
    time_gap = ts - time.time()
    print(f'NTP时间比本地时间快{round(time_gap, 3)}s')


def err_exit(text):
    print(f'\n{text}')
    exit()


def get_time(always_from_ntp=False):
    if always_from_ntp:
        response = ntplib.NTPClient().request('ntp.aliyun.com')
        ts = response.tx_time + (response.recv_time - response.orig_time + response.dest_time - response.tx_time)/2
    else:
        ts = time.time() + time_gap
    print('\r' + time.strftime('%Y-%m-%d %X', time.localtime(ts)), end='', flush=True)
    return ts


class Pai(object):
    def __init__(self):
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        try:
            if requests.get('http://127.0.0.1:9222/json/list', timeout=1).status_code != 200:
                err_exit('未以debug模式打开Edge, 无法继续运行, 脚本退出')
        except Exception as e:
            err_exit('未以debug模式打开Edge, 无法继续运行, 脚本退出')
        # 连接Edge
        self.driver = Edge(options=options)
        if self.driver.current_url != page_url:
            err_exit(f'当前页面为:{self.driver.current_url}, 请用Edge打开拍牌页面, 本次退出运行')
        print(f'\n浏览器连接成功, 页面正确:{self.driver.current_url}')

    def get_info(self):
        # 本来想从这里读取页面上的系统时间的，意义不大，没写
        pass

    def bid_price(self, price):
        # 自定义加价框，输入加价值
        elements = self.driver.find_elements(By.TAG_NAME, 'input')
        element_input_custom_add_price = elements[0]
        element_input_custom_add_price.clear()
        element_input_custom_add_price.send_keys(str(price))
        # 加价按钮和出价按钮
        elements = self.driver.find_elements(By.TAG_NAME, 'span')
        for i in elements:
            if i.text == '加价':
                i.click()
        for i in elements:
            if i.text == '出价':
                i.click()

    def confirm(self):
        # 点击确定按钮，用于最后的自动提交
        elements = self.driver.find_elements(By.TAG_NAME, 'span')
        for i in elements:
            if i.text == '确定':
                i.click()
                break

    # 下面这几个函数为使用xpath精准获取页面元素的写法，存在不准确的风险，未使用
    def bid_price_xpath(self, price):
        # 倒计时
        element_time = self.driver.find_element(By.XPATH, '')
        element_price = self.driver.find_element(By.XPATH, '')
        # 加价
        element_input_custom_add_price = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/input')
        element_input_custom_add_price.clear()
        element_input_custom_add_price.send_keys(str(price))
        element_button_custom_add_price = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/span')
        element_button_custom_add_price.click()
        # 出价
        element_button_custom_bid_price = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[3]/div/span')
        element_button_custom_bid_price.click()

    def confirm_xpath(self):
        # 确认
        element_button_custom_add_price = self.driver.find_element(By.XPATH, '')
        element_button_custom_add_price.click()

    def get_info_xpath(self):
        pass


if __name__ == '__main__':
    print(f'拍牌页面链接: {page_url}')
    init_time()
    if get_time() > submit_time:
        err_exit('已过提交时间，请重设时间')
    pai = Pai()
    first_add_price_done = False
    second_add_price_done = False
    second_confirm_price_done = False
    while True:
        t = get_time()
        # 第一次出价, 不会自动确定, 输入验证码后手动确定
        if second_add_price_time > t > first_add_price_time and not first_add_price_done:
            pai.bid_price(first_add_price_num)
            first_add_price_done = True
        # 第二次出价, 输入验证码后等待
        if submit_time > t > second_add_price_time and not second_add_price_done:
            pai.bid_price(second_add_price_num)
            second_add_price_done = True
        # 到达时间后, 点击确定按钮提交
        if t > submit_time and not second_confirm_price_done:
            pai.confirm()
            second_confirm_price_done = True
        if t > submit_time and second_confirm_price_done:
            print('\n一切都结束了,拜拜,下次不见')
            break
        time.sleep(0.08)
