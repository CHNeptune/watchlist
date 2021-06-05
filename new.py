import re
import requests
from bs4 import BeautifulSoup
import bs4
def getUrls(url):
    req = requests.get(url).text
    if (req == None):
        return
    bf = BeautifulSoup(req, 'html.parser')
    div_bf = bf.find('div', attrs={'class': 'content_list'})
    if isinstance(div_bf, bs4.element.Tag):
        div_a = div_bf.find_all('div', attrs={'class': 'dd_bt'})
        urltxt = open('./url.txt', 'a', encoding='UTF-8')
        for div in div_a:
            link = div.find('a').get("href")
            urltxt.write(link+'\n')
        urltxt.close()


days = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",
        "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

for day in range(15):
    url = "http://www.chinanews.com/scroll-news/2021/05" + days[day] + "/news.shtml"
    getUrls(url)