from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import News, Team, Player

import jieba
import time
import re
import copy

jieba.load_userdict('./resource/userdict_for_team.txt')

inFile = open('./resource/db/index.txt','r')
content = inFile.read()
if content != '':
    dictionary = eval(content)
else:
    dictionary = {}
inFile.close()

former_keyword = ""
time_used = 0
results = []
name_trans = {'密尔沃基雄鹿':'雄鹿','多伦多猛龙':'猛龙','费城76人':'76人','波士顿凯尔特人':'凯尔特人','印第安纳步行者':'步行者',
              '布鲁克林篮网':'篮网','奥兰多魔术':'魔术','底特律活塞':'活塞','夏洛特黄蜂':'黄蜂','迈阿密热火':'热火',
              '华盛顿奇才':'奇才','亚特兰大老鹰':'老鹰','芝加哥公牛':'公牛','克利夫兰骑士':'骑士','纽约尼克斯':'尼克斯',
              '金州勇士':'勇士','丹佛掘金':'掘金','波特兰开拓者':'开拓者','休斯顿火箭':'火箭','犹他爵士':'爵士',
              '俄克拉荷马雷霆':'雷霆','圣安东尼奥马刺':'马刺','洛杉矶快船':'快船','萨克拉门托国王':'国王','洛杉矶湖人':'湖人',
              '明尼苏达森林狼':'森林狼','孟菲斯灰熊':'灰熊','新奥尔良鹈鹕':'鹈鹕','达拉斯独行侠':'独行侠','菲尼克斯太阳':'太阳' }
biaodian = ['，','。','、','？','！','“','”','：','；','【','】','（','）','-','——','+','=',',','.','/','\\','[',']','\'','{','}','*','&','^','%','$','#','@','!','?']

def update(in_dictionary):
    global dictionary
    dictionary = in_dictionary

def index(request):
    return render(request, 'search/index.html')

def latest(request):
    currentpage = request.GET.get('pageIndex')
    pageSize = 12
    if not currentpage or int(currentpage)<1:
        currentpage = 1
    current_page = int(currentpage)
    start = (current_page - 1) * pageSize
    end = current_page * pageSize
    if current_page * pageSize > News.objects.all().count():
        nextpage = current_page
    else:
        nextpage = current_page + 1
    if current_page <= 1:
        previous_page = 1
    else:
        previous_page = current_page - 1

    latest_news_list = News.objects.order_by('-date')[start:end]
    #template = loader.get_template('search/latest.html')
    context = {
        'latest_news_list': latest_news_list,
        'nextPage': nextpage,
        'prevpage': previous_page,
    }
    return render(request,'search/latest.html',context)
    #return HttpResponse(template.render(context, request))

def hotlist(request):
    #teams = {}
    teams = []
    rank = 1
    for team in Team.objects.all():
        #teams[team.name] = len(dictionary[name_trans[team.name]])
        teams.append((team, len(dictionary[name_trans[team.name]])))
    #team_list = sorted(teams.items(), key=lambda d: d[1], reverse = True)
    teams.sort(key=lambda d: d[1], reverse = True)
    for i in range(0,len(teams)) :
        teams[i] = teams[i] + (rank,)
        rank += 1
    #print(team_list)
    # template = loader.get_template('search/hotlist.html')
    # context = {
    #     'team_list': team_list
    # }
    # return HttpResponse(template.render(context, request))
    # return render(request, 'search/hotlist.html', {'team_list': team_list})
    return render(request, 'search/hotlist.html', {'team_list': teams})
        

def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    related = []
    for item in dictionary[name_trans[team.name]]:
        related.append(get_object_or_404(News, pk=item))
    currentpage = request.GET.get('pageIndex')
    pageSize = 12
    if not currentpage or int(currentpage)<1:
        currentpage = 1
    current_page = int(currentpage)
    start = (current_page - 1) * pageSize
    end = current_page * pageSize
    if current_page * pageSize > News.objects.all().count():
        nextpage = current_page
    else:
        nextpage = current_page + 1
    if current_page <= 1:
        previous_page = 1
    else:
        previous_page = current_page - 1

    data={
            'nextPage': nextpage,
            'prevpage': previous_page,
            'team_news_list' : related[start:end],
            'team': team,
        }
    return render(request, 'search/team.html', data)

def news(request, news_id):
    news_piece = copy.copy(get_object_or_404(News, pk=news_id))
    cur = 1
    for player in Player.objects.all():
        if player.name_cn.strip() == '':
            continue
        #print(player.name_cn)
        news_piece.content = news_piece.content.replace(player.name_cn, '<a href=/team/' +  str(player.team.id) + '>' + player.name_cn + '</a>')
    for team in Team.objects.all():
        #print('''<a href="{% url 'search:team' ''' +  str(team.id) + ' %}"}>' + name_trans[team.name] + '</a>')
        news_piece.content = news_piece.content.replace(name_trans[team.name], '<a href=/team/' +  str(team.id) + '>' + name_trans[team.name] + '</a>')
    return render(request, 'search/news.html', {'news': news_piece})

def result(request):
    global former_keyword, results, time_used
    ###导出数据库新闻
    # with open('./resource/db/data.txt', "w") as out:  
    #     for item in News.objects.all():
    #         out.write(str(item.id) + " " + item.title + " " + item.content.replace('\n', ' ') + '\n')

    # dictionary = {}
    # with open('./resource/db/data.txt', 'r') as data:
    #     news_list = data.read().split('\n')
    #     for news in news_list:
    #         content = news.split(' ', 1)
    #         if(content == ['']):
    #             continue
    #         word_list = jieba.cut_for_search(content[1])
    #         for word in word_list:
    #             if word not in dictionary:
    #                 dictionary[word] = set()
    #             dictionary[word].add(content[0])
    keyword = request.GET['keyword']
    if keyword == '':
        return HttpResponseRedirect(reverse('search:index'))
    
    if(former_keyword != keyword):
        results = []
        start_time = time.time()
        tmp = {}
        keyword_list = jieba.cut(keyword)
        for item in keyword_list:
            if item in biaodian or item.strip() == '':
                continue
            if item in dictionary:
                for num in dictionary[item]:
                    #tmp.append((num,dictionary[item][num]))
                    if num not in tmp:
                        tmp[num] = dictionary[item][num]
                    else:
                        tmp[num] += dictionary[item][num]
        tmp = sorted(tmp.items(), key=lambda x:x[1], reverse = True)
        for i in tmp:
            n = get_object_or_404(News, pk=i[0])
            if n not in results:
                results.append(n)
        end_time = time.time()
        time_used = end_time - start_time
        former_keyword = keyword
    # context = {
    #     'keyword': keyword,
    #     'time_used': time_used,
    #     'result': result,
    #     'num': len(result),
    # }

    output = []
    for res in results:
        flag = True
        qqq = copy.copy(res)        
        keyword_list = jieba.cut(keyword)
        #keyword_list = [keyword,]
        #print(','.join(keyword_list))
        for k in keyword_list:
            if k in biaodian or k.strip() == '':
                continue
            if(re.search(re.compile(r'.{,40}'+k+'.{,40}'), res.content) != None):
                if flag == True:
                    qqq.content = "..." + re.search(re.compile(r'.{,40}'+k+'.{,40}'), qqq.content).group(0) + "..."
                qqq.title = qqq.title.replace(k, '<span style="color: red">' + k + '</span>')
                qqq.content = qqq.content.replace(k, '<span style="color: red">' + k + '</span>')
                flag = False
        if flag == False:
            output.append(qqq)
    currentpage = request.GET.get('pageIndex')

    pageSize = 12
    if not currentpage or int(currentpage)<1:
        currentpage = 1
    current_page = int(currentpage)
    start = (current_page - 1) * pageSize
    end = current_page * pageSize
    if current_page * pageSize > len(output):
        nextpage = current_page
    else:
        nextpage = current_page + 1
    if current_page <= 1:
        previous_page = 1
    else:
        previous_page = current_page - 1
    print(keyword)
    data={
            'nextPage': nextpage,
            'prevpage': previous_page,
            'time_used' : time_used,
            'keyword' : keyword,
            'result' : output[start:end],
            'num' : len(output),
        }
    return render(request,'search/result.html',data)