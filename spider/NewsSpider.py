#coding=utf-8
import requests
import re  # 正则表达式
import bs4  # Beautiful Soup 4 解析模块
import urllib.request  # 网络访问模块
import codecs  #解决编码问题的关键 ，使用codecs.open打开文件
import sys   #1解决不同页面编码问题
import importlib
import time
importlib.reload(sys)
import os
 
import ssl
 
ssl._create_default_https_context = ssl._create_unverified_context
 
 
# 从首页获取所有链接
def GetAllUrl(home):
    html = urllib.request.urlopen(home).read().decode('utf8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    links = soup.find_all('h4')
    for link in links:
        #print(link)
        url_set.add(link.find('a').get('href'))
def GetAllUrlL(home):
    html = urllib.request.urlopen(home).read().decode('utf8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    if os.path.exists("/Users/weitong/Desktop/nba_news/resource/NewsInfo/" + home[-12:-5] + ".txt"):
        return
    f = open("/Users/weitong/Desktop/nba_news/resource/NewsInfo/" + home[-12:-5] + ".txt", "w")
    #f.write(home)
    #f.write("\n")
    titleFinder = soup.find('h1')
    f.write(titleFinder.string.strip())
    f.write("\n")
    sourceFinder = soup.find("span", attrs={"class":"comeFrom"})
    f.write(sourceFinder.find('a').get_text())
    f.write("\n")
    sourceFinder = soup.find("a", attrs={"class":"time"})
    f.write(sourceFinder.find('span').get_text().strip())
    f.write("\n")
    contentFinder = soup.find("div", attrs={"class":"artical-main-content"})
    f.write(contentFinder.get_text())
 
 
 
url_set = set()  # url集合
home = 'https://voice.hupu.com/nba'

cur = 1

for i in range(1,35):
    GetAllUrl(home + "/" + str(i))
    try:
        for d in url_set:
            time.sleep(1);
            GetAllUrlL(d)
            print(str(cur) + " " + d)
            cur += 1
    except Exception as e:
        print('Error:', e)
    url_set.clear()