import datetime,pymysql,time
import sys,os
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

def main():
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        link = "http://entertain.naver.com/movie"
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        try:
            driver.get(link)
            html = driver.find_element_by_id('newsWrp').get_attribute('innerHTML')
        finally:
            driver.close()

        soup = BeautifulSoup(html,"html.parser")
        news_lst = soup.find('ul','news_lst').find_all('li')

        current = datetime.datetime.now()
        now = current.strftime('%Y-%m-%d %H:%M:%S')
        dbKey = getSearchKey(conn,curs)
        for li in news_lst:
            item = li.find('div','tit_area')
            writerDate = item.find('span','press')
            wd = writerDate.get_text('@',strip=True).strip().split('@')
            wdate = None
            if wd[1].find('분전') != -1:
                wdate = current - datetime.timedelta(minutes=int(wd[1].replace('분전','')))
            elif wd[1].find('시간전') != -1:
                wdate = current - datetime.timedelta(hours=int(wd[1].replace('시간전','')))

            data = {
                'NM_title':item.find('a','tit').text.strip(),
                'writer':wd[0],
                'writeDate':(wdate is None) and wdate or wdate.strftime('%Y-%m-%d %H:%M'),
                'title_key':'',
                'keyword':'',
                'keyword_type':'',
                'url':'http://entertain.naver.com'+item.find('a','tit')['href'],
                'createDate':now,
                'updateDate':now
            }
            mkey = getMainKeyword(dbKey,data['NM_title'])

            if mkey:
                paramKey = None
                data['title_key'] = dbKey[mkey]['add'][0]
                data['keyword'] = getPutKeyword(data['NM_title'],None,dbKey[mkey]['add'])

                if data['keyword']:
                    data['keyword_type'] = getPutKeywordType(data['keyword'],conn,curs)
                    data['keyword_type'] = (data['keyword_type'] == None) and '' or data['keyword_type']

            try:
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = "INSERT INTO navermovienews_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                curs.execute(sql, list(data.values()))
                conn.commit()
            except Exception as e:
                if e.args[0] != 1062:
                    print("===========에러==========\n에러 : ",e,data,"\n===========에러==========")
    finally:
        conn.close()

if __name__=='__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" %(time.time() - start_time))
