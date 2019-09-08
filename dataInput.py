# -*- coding:utf8 -*-  
  
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nba_news.settings")

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()

from search.models import News, Team, Player

# path = "/Users/weitong/Desktop/nba_news/resource/NewsInfo"
path = "/Users/weitong/Desktop/nba_news/resource/TeamRoster"

fileList = []
files = os.listdir(path)
for f in files:  
        fileList.append(f)  

cur = 1

for fl in fileList:  
    if(fl[-3:] != "txt"):
        continue
    name = fl[:-4]
    # f = open("./resource/NewsInfo/" + fl, "r")
    f = open("./resource/TeamRoster/" + fl, "r")
    # title = f.readline().strip()
    # source = f.readline().strip()
    # time = f.readline().strip()
    # f.read(1)
    # content = f.read().strip()
    # News.objects.create(title = title, source = source, date = time, content = content)


    city = f.readline().strip()
    year = f.readline().strip()
    # print(name)
    # print(year)
    team = Team.objects.create(name = name, city = city, year = year)


    players = f.read()
    player_list = players.split('\n')
    # print(player_list)
    for p in player_list:
        if(p == ''):
            continue
        names = p.split(' ', 1)
        # print(names[0].strip(),"      ",names[1].strip())
        Player.objects.create(team = team, name_cn = names[0].strip(), name_en = names[1].strip())
