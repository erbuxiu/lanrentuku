import requests
from bs4 import BeautifulSoup
import os,sys
import time
import zipfile
import csv
def downlink(url): #下载页获取下载链接 目前只能用于矢量素材
    req = requests.get(url).text
    req = BeautifulSoup(req,"html5lib")
    if  req.title.text!= "404页面 - 懒人图库":
        down = req.select("#l a.bt-blue")[0]["href"]
        tags = list(req.select("#l .tag")[0].stripped_strings)[1:]
        otherinfo = req.select("#l > div.title > div")[0].text
        date = otherinfo.split("　")[0]
        author = otherinfo.split("　")[1]
        category = otherinfo.split("　")[2]
        title = req.title.text.split("_")[0:2]
        img = req.select("#l  img")[0]["src"]
        info = {
            "title":title,
            "downlink": down,
            "tags": tags,
            "author":author,
            "category":category,
            "img": img,
        }
    else:
        info = {}
        print(url,"采集失败")
    return info
def listlink(page):
    url = "http://www.lanrentuku.com/vector/p{}.html".format(page)
    reqlist = requests.get(url).text
    reqlist = BeautifulSoup(reqlist,"html5lib")
    listlink= reqlist.select("#l > div.list-pic  a")
    listlink = list("http://www.lanrentuku.com"+listlink["href"] for listlink in listlink)
    return listlink
def lastpage():
    url = "http://www.lanrentuku.com/vector/"
    lastpage = requests.get(url).text
    lastpage = BeautifulSoup(lastpage,"html5lib")
    lastpage = lastpage.select("#l ul li a")[-1]["href"][1:5]
    return lastpage
for i in range(1, int(lastpage())):
    wbdata = listlink(i)
    print("采集到",i,"列表页")
    headers = ['title', 'downlink', 'tags', 'author', 'category', 'img']
    with open('log.csv', 'a',newline='',encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        filenum = 1
        imgnum = 1
        for url in wbdata:
            downurl = downlink(url)
            f_csv.writerows([downurl])
            downfile = downurl["downlink"]
            downimg = downurl["img"]
            downfile = requests.get(downfile)
            downimg = requests.get(downimg)
            filename = downurl["title"][1]+"-"+downurl["title"][0]+"."+downurl["downlink"].split(".")[-1]
            imgname = downurl["title"][1]+"-"+downurl["title"][0] + "." + downurl["img"].split(".")[-1]
            path= os.path.split(os.path.realpath(sys.argv[0]))[0]+"\\down\\"#获取当前脚本路径并构造down子文件夹
            if os.path.exists(path) == True:#判断当前时候有down目录，没有则创建
                pass
            else:
                os.mkdir(path)
            with open(path+filename, "wb") as code:
                code.write(downfile.content)
                print("下载"+filename+"文件成功！这是第"+str(filenum)+"个文件。")
                filenum = filenum + 1
                with open(path+imgname, "wb") as code:
                    code.write(downimg.content)
                    print("下载" + imgname + "预览图成功！这是第" + str(imgnum) + "个预览图。")
                    imgnum = imgnum + 1


