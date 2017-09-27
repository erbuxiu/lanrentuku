#实现采集标题，标签，下载链接，预览图，分类等，并输出为csv。下载文件到脚本down目录下，并解压文件夹删除原压缩包，并删除广告文件。
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
def dirpath(path): #判断目录path目录是否存在，如果不存在就创建目录。
    import os
    if os.path.exists(path) == True:  # 判断有没有子目录
        pass
    else:
        os.mkdir(path)
def unzip(Afile,filepath): #传入文件名和路径，解压到单独的文件夹,并删除文件名中指定关键字
    import os
    import zipfile
    # Afile = "交通运输-6款创意出租车元素标签矢量素材.zip"
    # filepath = r"C:\Users\ASUS\Desktop\lanren\down\\"[:-1]

    myzip=zipfile.ZipFile(filepath+Afile,'r')
    myfilelist=myzip.namelist()
    for name in myfilelist:
        strname = name.encode('cp437').decode('gbk')
        if strname == "readme.html"or strname =="懒人图库.url": #判断文件名，如果文件名是不需要的就不解压
            pass
        else:
            strname=strname.replace('_lanrentuku.com','')
            path = filepath+Afile.split(".")[0]+"\\"
            dirpath(path)
            f_handle=open(path+strname,"wb")
            f_handle.write(myzip.read(name))
            f_handle.close()
    myzip.close()
def adddirfile(filedir,path):
    f = zipfile.ZipFile(filedir,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            f.write(os.path.join(dirpath,filename))
    f.close()
for i in range(1, int(lastpage())):
    wbdata = listlink(i)
    print("采集到",i,"列表页")
    headers = ['title', 'downlink', 'tags', 'author', 'category', 'img']
    with open('log.csv', 'a',newline='',encoding='gbk') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        filenum = 1
        for url in wbdata:
            downurl = downlink(url)
            f_csv.writerows([downurl])
            downfile = requests.get(downurl["downlink"])
            filename = downurl["title"][1]+"-"+downurl["title"][0]+"."+downurl["downlink"].split(".")[-1]
            path= os.path.split(os.path.realpath(sys.argv[0]))[0]+"\\down\\"#获取当前脚本路径并构造down子文件夹
            dirpath(path)
            with open(path+filename, "wb") as code:
                code.write(downfile.content)
                print("download"+filename+"successed！It is "+str(filenum)+"file.")
                filenum = filenum + 1
                unzip(filename,path)
                print("unzip-successed"+filename)
            os.remove(path + filename)









