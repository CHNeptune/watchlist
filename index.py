import os
import jieba

def index():
    data_path = 'data/'
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

    return invert_index,count_words
