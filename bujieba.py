import jieba
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  

jieba.load_userdict('./resource/userdict_for_team.txt')

dictionary = {}

with open('./resource/db/data.txt', 'r') as data:
    news_list = data.read().split('\n')
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

with open('./resource/db/index.txt', 'w') as index:
    print(dictionary, file = index)
