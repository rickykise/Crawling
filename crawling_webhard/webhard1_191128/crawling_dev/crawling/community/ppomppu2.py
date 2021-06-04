# ppomppu 검색
import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : ",key)
    link = "http://www.ppomppu.co.kr/zboard/zboard.php?id=freeboard&page=1&search_type=sub_memo&keyword="+key
    print(link)
    check = True;

    while check:
        textHtml = requests.get(link).text
        soup = BeautifulSoup(textHtml,'html.parser')
        table = soup.find("tbody")
        print(table)


if __name__=='__main__':
    startCrawling('아이유')
    # start_time = time.time()
    #
    # conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    # curs = conn.cursor(pymysql.cursors.DictCursor)
    # dbKey = getSearchKey(conn,curs)
    # conn.close()

    # print("ppomppu 크롤링 시작")
    # for k in dbKey.keys():
    #     startCrawling(k)
    # print("ppomppu 크롤링 끝")
    # print("--- %s seconds ---" %(time.time() - start_time))
    # print("=================================")
