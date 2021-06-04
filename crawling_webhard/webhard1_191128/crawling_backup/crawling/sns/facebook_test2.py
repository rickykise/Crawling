import openpyxl,time,pymysql,datetime
import requests
import urllib.request
from bs4 import BeautifulSoup

def startCrawling():
    pageNum = 0;check = True;paramKey = None;insertNum = 0

    while check:
        r = requests.get('https://m.facebook.com/graphsearch/str/%EB%8D%94%EB%B3%B4%EC%9D%B4%EC%A6%88/stories-keyword/stories-public?tsid=0.8484371015225547&source=pivot&ref=content_filter')
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        print(soup)

if __name__=='__main__':
    start_time = time.time()
    startCrawling()
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
