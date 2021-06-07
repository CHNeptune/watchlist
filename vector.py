import jieba
from numpy import result_type
from index import index
import math
from search import search

def vector(string):
    data_path = 'data/'
    
    file_collect,searcher = search(string)
    # print('searcher=')
    # print(searcher)
    if len(file_collect) ==0:
        result = []
        result += [{"pos":"","event":"","url":"","rel":"","date":""}]
        return result

    tf = {}     #词频
    for filename in file_collect:       #   统计词频
        f = open(data_path + filename, mode='r', encoding='utf-8')
        url = f.readline()
        content = f.read()
        f.close()
        words = list(jieba.cut_for_search(content))
        for word in words:
            if word not in tf.keys():
                tf.setdefault(word,{})[filename] = 1
            elif filename not in tf[word].keys():
                tf.setdefault(word,{})[filename] = 1
            else:
                tf.setdefault(word, {})[filename] += 1

    idf = {}  # 逆词频
    for filename in file_collect:           #统计逆词频
        f = open(data_path+ filename, mode='r', encoding='utf-8')
        url = f.readline()
        content = f.read()
        f.close()
        for word in tf.keys():
            if word in content:
                if word not in idf.keys():
                    idf[word] = 1
                else:
                    idf[word] += 1


    # 将搜索词条当成文本统计词频和逆词频er
    for word in searcher:
        if word not in tf.keys():
            tf.setdefault(word, {})['search'] = 1
        elif 'search' not in tf[word].keys():
            tf.setdefault(word, {})['search'] = 1
        else:
            tf.setdefault(word, {})['search'] += 1
        if word not in idf.keys():
            idf[word] = 1
        else:
            idf[word] += 1

    len_search = len(set(searcher))    # 搜索词条长度
    len_file = len(file_collect) + 1   # 文本总数+词条文本

    search_weight = {}      #搜索文本向量
    Correlation = dict()  # 相关度
    #print(file_collect)
    for filename in file_collect:
        text_weight = {}    #文本向量
        for word in idf.keys():
            if word in searcher:
                search_weight[word] = tf[word]['search']/len_search * (1 + math.log2(len_file/idf[word]))
            else:
                search_weight[word] = 0
            if filename in tf[word].keys():
                text_weight[word] = tf[word][filename]/len_file * (1 + math.log2(len_file/idf[word]))
            else:
                text_weight[word] = 0
        #计算相关度
        weight = 0
        search_Module = 0
        text_Module = 0
        Correlation[filename] = 1
        for word in text_weight.keys():
            weight += search_weight[word] * text_weight[word]
            search_Module += search_weight[word]*search_weight[word]
            text_Module += text_weight[word]*text_weight[word]
        Correlation[filename] = weight / (search_Module * text_Module)
    #相关度排序
    Correlation_order=sorted(Correlation.items(),key=lambda x:x[1],reverse=True)
    # for i in range(len_file):
    #     print(Correlation_order[i])

    result = []

    for i in range(0,len_file-1):
        f = open(data_path + Correlation_order[i][0], mode='r', encoding='utf-8')
        url = f.readline()
        time = f.readline()
        content = f.readlines()
        f.close()

        record = ["","","","",""]


        #print(Correlation_order[i][0].replace('.txt',''))
        record[0]=Correlation_order[i][0].replace('.txt','')

        #print('相关度:     '+ str(Correlation_order[i][1]))
        record[1]='相关度:  '+ str(Correlation_order[i][1])

        #print('时间:   '+str(time))
        
        record[2]='时间:   '+str(time)

        record[3]=""
        i=int(0)
        for line in content:
            for word in set(searcher):
                if word in line:
                    #print(line)
                    line += '\n'
                    record[3] += line

                    i+=1
                    break
            if i>=3:
                break

        #print(url+'\n')
        record[4] = url

        result += [{"pos":record[0],"event":record[3],"url":record[4],"rel":record[1],"date":record[2]}]

    #print(result)
    return result;       



