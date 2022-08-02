from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import getIMG
import datetime
import os
#使用twitter高级搜索
#照片栏最多显示50条twitter

serial = 1
first=""

serial = 1
full_data = []
wrong_log = []

def Chrome_Config():
    options = ChromeOptions()
    options.add_argument(r"输入本地登录信息目录")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless")  # => 为Chrome配置无头模式
    # options.add_argument("--headless")
    options.binary_location=r'chrome目录'
    driver = webdriver.Chrome(r'chromedriver目录', options=options)
    return driver

def getHeight(driver):
    js_height = 'return document.body.scrollHeight'
    js_scroll_end = 'window.scrollTo(0,document.body.scrollHeight)'
    height_now_t = 0
    while int(driver.execute_script(js_height)) > height_now_t:
                driver.execute_script(js_scroll_end)
                height_now_t = driver.execute_script(js_height)
                time.sleep(3)
    print(height_now_t)
    js_scroll_start = 'window.scrollTo(0,0)'
    driver.execute_script(js_scroll_start)
    return height_now_t

def scrollNormal(driver,height):
    js_scroll_2000 = 'window.scrollTo(0,{hn})'.format(hn=height)
    driver.execute_script(js_scroll_2000)

def run(since, until,log):
    global serial
    global full_data
    global wrong_log
    mon_sum = 0
    year_sum = 0
    all_sum = 0
    img_list = []
    IMG_LIST = []
    since = since+" 00:00:00"
    until = until+" 00:00:00"
    time_since = datetime.datetime.strptime(since,"%Y-%m-%d %H:%M:%S")
    time_until = datetime.datetime.strptime(until,"%Y-%m-%d %H:%M:%S")
    dur_days = (time_until-time_since).days
    # getIMG.getImg(test_url,test_url)
    # try:
    driver = Chrome_Config()
    if dur_days<=31:
        url = "输入请求地址".format(until=until, since=since)
    else:
        while (time_until-time_since).days >0:
            temp_until = time_since + datetime.timedelta(days=31)
            temp_until = datetime.datetime(temp_until.year,temp_until.month,1,temp_until.hour,temp_until.minute,temp_until.second) if temp_until.day!=1 else temp_until
            url = "输入请求地址".format(until=str(temp_until).split(" ")[0], since=str(time_since).split(" ")[0])
            driver.get(url)
            driver.implicitly_wait(20)
            # getHeight(driver)
            # try:
            height_now = int(0)
            last_height_now = 1300
            js_height = 'return document.body.scrollHeight'
            js_scroll_end = 'window.scrollTo(0,document.body.scrollHeight)'
            print(type(driver.execute_script(js_height)))
            height_now = getHeight(driver)
            while last_height_now < height_now:
                height_now = driver.execute_script(js_height)
                print("----------------------------------")
                print("height_now="+str(last_height_now))
                print("----------------------------------")
                if height_now <1300:
                    driver.execute_script(js_scroll_end)
                else:
                    scrollNormal(driver,last_height_now)
                    last_height_now+=1300
                print("----------------------------------")
                print("scroll normal")
                print("----------------------------------")
                time.sleep(2)
                input = driver.find_elements_by_tag_name("img")
                for img_id in range(len(input)):
                    img = input[img_id]
                    if img.get_attribute("src") != None:
                        url = img.get_attribute("src")
                        if "/media/" in url or "card_img" in url:
                            print(url)
                            img_list.append(url)

            driver.execute_script(js_scroll_end)
            print("----------------------------------")
            print("scroll outside")
            print("----------------------------------")
            time.sleep(1)
            input = driver.find_elements_by_tag_name("img")
            for img_id in range(len(input)):
                img = input[img_id]
                if img.get_attribute("src") != None:
                    url = img.get_attribute("src")
                    if "/media/" in url:
                        print(url)
                        img_list.append(url)

            time.sleep(1)
            img_list = list(set(img_list))
            mon_sum = len(img_list)
            print("----------------------------------")
            print("当前图片数量："+ str(mon_sum))
            log.write(str(time_since) + " 发图：" + str(mon_sum) + "张。")
            year_sum += mon_sum
            mon_sum = 0
            print("----------------------------------")
            for i in img_list:
                IMG_LIST.append(i)
            img_list = []

            for img_url in IMG_LIST:
                isExists = False
                print("---------下载"+img_url+"中---------")
                while not isExists:
                    getIMG.getImg(img_url,img_url,str(time_since))
                    isExists = os.path.exists(getIMG.validateTitle(img_url) + ".jpg")
                print("----------------------------------")
            IMG_LIST = []
            if temp_until.year != time_since.year:
                log.write(str(time_since.year) + "年 发图：" + str(year_sum) + "张。")
                all_sum += year_sum
                year_sum = 0
            time_since = temp_until

    return all_sum



if __name__ == '__main__':
    f = open("data.txt", "w+", encoding='utf-8')
    print("Plese input the time period like \"xxxx-xx-xx xxxx-xx-xx\"")
    [since, until] = input().split(" ")
    start = time.time()
    num = run(since, until,f)
    end = time.time()
    print("共爬取"+ str(num) +"张图，用时："+str(end - start))
    f.write("共爬取"+ str(num) +"张图，用时："+str(end - start))
    f.close()
