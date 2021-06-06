import jieba
from index import index

def search(string):
    str = string
    searcher = list(jieba.cut_for_search(str))
    stopwords = [line.strip() for line in open('stop_words.txt',encoding='gbk').readlines()]
    #print(searcher)
    words = []
    for word in searcher:       # 去停用词
        if word not in stopwords:
            words.append(word)
    search = words
    file_collect = []   # 倒插索引后的文件名
    invert_index,count_words = index()
    for word in searcher:
        if word in invert_index.keys():
            file_collect.extend(invert_index[word])
    file_collect = list(set(file_collect))
    return file_collect,searcher