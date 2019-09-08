#coding=utf-8
import requests
import os
import time
import re  # 正则表达式
import bs4  # Beautiful Soup 4 解析模块
import urllib.request  # 网络访问模块
import codecs  #解决编码问题的关键 ，使用codecs.open打开文件
import sys   #1解决不同页面编码问题
import importlib
importlib.reload(sys)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from django.http import HttpResponse
import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()

from search.models import News, Team, Player
from search.views import update
import jieba
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer 

phase = 0
is_running = 0

def get_state(request):
    return HttpResponse(is_running)

def spider(request):
    global phase, is_running
    
    if(is_running == 1):
        is_running = 2
    else :
        if is_running == 0:
            is_running = 1
        flag = False
        cur = 1
        url_set = set()  # url集合
        home = 'https://voice.hupu.com/nba'
        new_file = []
        for i in range(1,36):
            if is_running != 1:
                break
            html = urllib.request.urlopen(home + "/" + str(i)).read().decode('utf8')
            soup = bs4.BeautifulSoup(html, 'html.parser')
            links = soup.find_all('h4')
            for link in links:
                url_set.add(link.find('a').get('href'))
            for d in url_set:
                if is_running != 1:
                    break
                #print(d)
                time.sleep(1)
                html1 = urllib.request.urlopen(d).read().decode('utf8')
                soup1 = bs4.BeautifulSoup(html1, 'html.parser')
                print(cur)
                cur += 1
                path = "./resource/NewsInfo/" + d[-12:-5] + ".txt"
                if os.path.exists(path):
                    flag = True
                    continue
                f = open(path, "w")
                new_file.append(path)
                titleFinder = soup1.find('h1')
                #print(titleFinder.string.strip())
                f.write(titleFinder.string.strip())
                f.write("\n")
                sourceFinder = soup1.find("span", attrs={"class":"comeFrom"})
                f.write(sourceFinder.find('a').get_text())
                f.write("\n")
                sourceFinder = soup1.find("a", attrs={"class":"time"})
                f.write(sourceFinder.find('span').get_text().strip())
                f.write("\n")
                contentFinder = soup1.find("div", attrs={"class":"artical-main-content"})
                f.write(contentFinder.get_text())

                # print(str(cur) + " " + d)
                #cur += 1
            if flag:
                break
            url_set.clear()
        phase = 1
        print('phase 1 finished!')       
        
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nba_news.settings")
        db_news = []
        for fl in new_file:  
            if(fl[-3:] != "txt"):
                continue
            name = fl[:-4]
            f = open(fl, "r")
            title = f.readline().strip()
            source = f.readline().strip()
            time1 = f.readline().strip()
            f.read(1)
            content = f.read().strip()
            q = News.objects.create(title = title, source = source, date = time1, content = content)
            db_news.append(q)
        phase = 2
        print('phase 2 finished!')
        
        
        news_list = []
        #with open('./resource/db/data.txt', "w") as out:  
        for item in db_news:
            #out.write(str(item.id) + " " + item.title + " " + item.content.replace('\n', ' ') + '\n')
            news_list.append(str(item.id) + " " + item.title + " " + item.content.replace('\n', ' ') + '\n')
        phase = 3
        print('phase 3 finished!')
        
        
        inFile = open('./resource/db/index.txt','r')
        content = inFile.read()
        dictionary = eval(content)
        inFile.close()
        for news in news_list:
            content = news.split(' ', 1)
            if(content == ['']):
                continue
            corpus = [' '.join(jieba.cut(content[1])),]
            vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
            transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
            tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
            word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
            weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
            
            num = content[0]
            for j in range(len(word)): 
                if word[j] not in dictionary:
                    dictionary[word[j]] = {}
                if num not in dictionary[word[j]]:
                    dictionary[word[j]][num] = weight[0][j]
                else:
                    dictionary[word[j]][num] += weight[0][j]
        phase = 4
        print('phase 4 finished!')

        with open('./resource/db/index.txt', 'w') as index:
            print(dictionary, file = index)
        update(dictionary)

        if(is_running == 2):
            is_running = 0
            return HttpResponse("爬虫停止!")
        elif(is_running == 1):
            is_running = 0
            return HttpResponse("爬虫完成!")