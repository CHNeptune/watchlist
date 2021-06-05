import re
import requests
from bs4 import BeautifulSoup
import time

k=0
with open(r'./url.txt') as f:
    for i in range(1,200):
        print(i)
        url=f.readline().replace('\n','')
        if url[0]=='/':
            s=url[1:3]
            url = 'http://www.chinanews.com' + url
        else:
            s=url[25:27]
        filepath='D:/学习资料/大三下/信息与知识获取/实验/data/'
        print(url+'*')
        head = requests.head(url)
        req = requests.get(url)
        req.encoding = 'utf-8'
        try:
            bf = BeautifulSoup(req.text, 'html.parser')
            div = bf.find('div', attrs={'class': 'content'})
            h1 = div.find('h1')
            head = re.sub(r'\s+', '', h1.get_text())
            k+=1
            out = open(filepath+ str(k)+'.txt', 'w', encoding='utf-8', errors='ignore')
            out.write(url + '\n')
            out.write(head + '\n')
            timediv = div.find('div', attrs={'class': 'left-t'})
            time = timediv.get_text().replace(" ", "")[0:16]
            out.write(time)
            p = div.find('div', attrs={'class': 'left_zw'}).find_all('p', text=True)
            for ptext in p:
                out.write('\n'+ptext.text)
            out.close()
        except:
            print('skip')
