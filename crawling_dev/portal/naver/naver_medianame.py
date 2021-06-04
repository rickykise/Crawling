import os,sys
import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *

# url 가져오는 함수
def getSearchUrlmedia(conn,curs):
    with conn.cursor() as curs:
        sql = 'select url from media_data where writeDate >= curdate() and media_check =0 and media_subname = "naver" and media_name = "naver"  order by createDate desc;'
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

#기자 체크
def checkMediaName(content, reportern):
    mediaName = None

    for s in reportern.keys():
        if content.find(s) != -1 :
            mediaName = s

    return mediaName

def main(url):
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # print(url)
    updateNum = 0;
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    contents = ""

    if soup.find('div', id='articleBodyContents'):
        contents = soup.find('div', id='articleBodyContents').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
        # print(contents)
    elif soup.find('div', 'end_body_wrp'):
        contents = soup.find('div', 'end_body_wrp').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
        # print(contents)
    elif soup.find('div', id='newsEndContents'):
        contents = soup.find('div', id='newsEndContents').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
        # print(contents)
    
    if contents != "":
        dbreporter = getReporter(conn,curs)
        media_name = checkMediaName(contents, dbreporter)
        if media_name != None:
            # print(media_name)
            try:
                sql = "update media_data set media_name=%s, media_check=1 where url=%s and media_name = 'naver';"
                curs.execute(sql, (media_name, url))
                conn.commit()
                updateNum = updateNum+1
                i = i+1
            except Exception as e:
                if e.args[0] == 1062:
                    sql = "delete from media_data where media_name = 'naver' and url =%s;"
                    curs.execute(sql, (url))
                    conn.commit()

    print("updateNum :",updateNum)
    print("=============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrlmedia(conn,curs)
    conn.close()

    for u in getUrl:
        main(u)
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
