import os
import jieba
import numpy as np
import math



def Search(searcher):

    data_path = 'data\\'

    res_path = 'cut.txt'
    #searcher = '广东CBA的MVP'

    invert_index = {}   #索引表
    count_words = {}    # 文本总词

    # 停用词表
    stopwords = [line.strip() for line in open('stop_words.txt',encoding='gbk').readlines()]

    files = os.listdir(data_path)  #文件名
    i = 0
    # 遍历文件
    for filename in files:
        i += 1
        if i <= 100:
            f =  open (data_path+ filename,mode='r',encoding='utf-8')
            url = f.readline()
            content = f.read()
            f.close()
            words = []
            segment = list(jieba.cut_for_search(content))
            # #去停用词
            for word in segment:
                if word not in stopwords:
                    words.append(word)
            # 倒插索引
            for word in words:
                invert_index.setdefault(word,[]).append(filename)
                invert_index[word] = list(set(invert_index[word]))
            segment1 = list(set(segment))
            count_words[filename] = len(segment1)


    # for key in invert_index.items():
    #     print(key)
    # for key in tf.items():
    #     print(key)
    # for key in idf.items():
    #     print(key)


    search = list(jieba.cut_for_search(searcher))
    #print(search)
    words = []
    for word in search:       # 去停用词
        if word not in stopwords:
            words.append(word)
    search = words

    file_collect = []   # 倒插索引后的文件名
    for word in search:
        file_collect.extend(invert_index[word])
    file_collect = list(set(file_collect))
    #print(file_collect)

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

    # for key in tf.items():
    #      print(key)

    idf = {}    #逆词频
    for filename in file_collect:           #统计逆词频
        f = open(data_path  + filename, mode='r', encoding='utf-8')
        url = f.readline()
        content = f.read()
        f.close()
        for word in tf.keys():
            if word in content:
                if word not in idf.keys():
                    idf[word] = 1
                else:
                    idf[word] += 1
    # for key in idf.items():
    #     print(key)

    # 将搜索词条当成文本统计词频和逆词频
    for word in search:
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

    len_search = len(set(search))    # 搜索词条长度
    len_file = len(file_collect) + 1   # 文本总数+词条文本

    search_weight = {}
    Correlation ={}
    for filename in file_collect:
        text_weight = {}

        for word in idf.keys():
            if word in search:
                search_weight[word] = tf[word]['search']/len_search * (1 + math.log2(len_file/idf[word]))
            else:
                search_weight[word] = 0
            if filename in tf[word].keys():
                text_weight[word] = tf[word][filename]/len_file * (1 + math.log2(len_file/idf[word]))
            else:
                text_weight[word] = 0

        weight = 0
        search_Module = 0
        text_Module = 0
        for word in text_weight.keys():
            weight += search_weight[word] * text_weight[word]
            search_Module += search_weight[word]*search_weight[word]
            text_Module += text_weight[word]*text_weight[word]

        Correlation[filename] = weight/(search_Module*text_Module)
    Correlation_order=sorted(Correlation.items(),key=lambda x:x[1],reverse=True)

    print(Correlation_order)
    print(search)
    i=0
    print("LENTH OF THIS LIST:---- ",len(Correlation_order))

    result = []


    for i in range(len(Correlation_order)):
        f = open(data_path + Correlation_order[i][0], mode='r', encoding='utf-8')
        url = f.readline()
        content = f.readlines()
        f.close()

        record = [0,1,2]

        #print(Correlation_order[i][0])
        record[0] = Correlation_order[i][0]

        i=int(0)

        record[1] = ""
        for line in content:
            for word in set(search):
                if word in line:
                    if i<3:

                        #print(line)
                        record[1] += line
                        
                    i+=1
                    break
        
        #print(url+'\n')
        record[2] = url


        result += [{"pos" :record[0] ,"event" : record[1], "url": record[2]}]
        i+=1

    return result