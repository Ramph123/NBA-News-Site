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
 
import ssl
 
ssl._create_default_https_context = ssl._create_unverified_context
 

# def GetAllUrl(home):
#     html = urllib.request.urlopen(home).read().decode('utf8')
#     soup = bs4.BeautifulSoup(html, 'html.parser')
#     links = soup.find_all('h4')
#     for link in links:
#         #print(link)
#         url_set.add(link.find('a').get('href'))
# def GetAllUrlL(home):
#     html = urllib.request.urlopen(home).read().decode('utf8')
#     soup = bs4.BeautifulSoup(html, 'html.parser')
#     f = open("/Users/weitong/desktop/NewsInfo/" + home[-12:-5] + ".txt", "w")
#     #f.write(home)
#     #f.write("\n")
#     titleFinder = soup.find('h1')
#     f.write(titleFinder.string.strip())
#     f.write("\n")
#     sourceFinder = soup.find("span", attrs={"class":"comeFrom"})
#     f.write(sourceFinder.find('a').get_text())
#     f.write("\n")
#     sourceFinder = soup.find("a", attrs={"class":"time"})
#     f.write(sourceFinder.find('span').get_text().strip())
#     f.write("\n")
#     contentFinder = soup.find("div", attrs={"class":"artical-main-content"})
#     f.write(contentFinder.get_text())
 

f = open("/Users/weitong/Desktop/TeamRoster/印第安纳步行者.txt", "w")
home = 'http://data.sports.sohu.com/nba/nba_team_info.php?teamid=11'
home1 = 'https://nba.hupu.com/players/pacers'

html = urllib.request.urlopen(home).read().decode('gb2312')
soup = bs4.BeautifulSoup(html, 'html.parser')
form = soup.find('div', attrs={"class":"pt"})
lists = form.find_all('li')
cur = 0
for item in lists:
        if (cur == 1 or cur == 4):
                content = item.get_text()
                f.write(re.match('\w+：(\w+)', content).group(1))
                f.write("\n")
        cur += 1



html = urllib.request.urlopen(home1).read().decode('utf8')
soup = bs4.BeautifulSoup(html, 'html.parser')
lists = soup.find_all('b')
for item in lists:
        name = item.find('a', attrs={"target": "_blank"})
        if name != None :
                f.write(name.get_text())
                f.write(" ")
        if re.match('\w+\s\w+',item.get_text()) != None :
                f.write(item.get_text())
                f.write("\n")

