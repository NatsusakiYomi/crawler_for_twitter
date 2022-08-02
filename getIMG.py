import os
import re

import requests
from retry import retry

par_path = ''  # 父文件夹


def getImg(url, title, date):
    os.chdir(par_path)
    path = par_path+" "+validateTitle(date)
    dirExists = os.path.exists(path)
    if not dirExists:
        os.mkdir(path)
    os.chdir(path)
    isExists = os.path.exists(validateTitle(title) + ".jpg")
    imgurl = url.split("&name=")[0]+"&name=medium"
    if isExists:
        print("该图片已存在！")
        return

    while not isExists:
        global img

        @retry(tries=1000, delay=4)
        def getImg0():
            global img
            print("尝试下载中………")
            img = requests.get(imgurl, timeout=4)

        getImg0()

        if img.status_code == 200:
            open(validateTitle(title) + ".jpg", 'wb').write(img.content)
            print("下载成功！",validateTitle(title))
        else:
            print("下载失败！",validateTitle(title))
            # break
        isExists = os.path.exists(validateTitle(title) + ".jpg")


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
