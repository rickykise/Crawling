import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from snsFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def getTime(date):
    dateGettime = date.replace('·', '-')
    try:
        if dateGettime.find('오전 12:') != -1:
            writeDate = datetime.datetime.strptime(dateGettime, "오전 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d 00:%M:%S')
        elif dateGettime.find('오후 12:') != -1:
            writeDate = datetime.datetime.strptime(dateGettime, "오후 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')
        elif dateGettime.find('오후') != -1:
            writeDatech = datetime.datetime.strptime(dateGettime, "오후 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')
            clock = datetime.datetime.strptime(dateGettime, "오후 %H:%M - %Y년 %m월 %d일").strftime('%I')
            clock2 = int(clock)+12
            cl = str(clock2)
            writeDate = datetime.datetime.strptime(writeDatech, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d '+cl+':%M:%S')
        else:
            writeDate = datetime.datetime.strptime(dateGettime, "오전 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    return writeDate

def startCrawling(key):
    print("키워드 : ",key)
    i = 0;check = True
    updateNum = 0;insertNum = 0;
    checkDay = datetime.date.today() - datetime.timedelta(1)
    # link = "https://twitter.com/search?f=tweets&vertical=default&q="+key+"&src=typd"
    link = "https://twitter.com/search?q="+key+"&src=typd&f=live&vertical=default"
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            driver.get(link)
            time.sleep(1)
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            html = driver.find_element_by_class_name("css-1dbjc4n").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            article = soup.find_all('article', role="article")

            for item in article:
                writer = item.find('div', dir='auto').text.strip()
                url = 'https://twitter.com' + item.find('a', dir='auto')['href']
                div = item.find('div', role="group")['aria-label']

                if div.find('답글') == -1:
                    reply = 0
                else:
                    reply = div.split('답글')[0].strip()

                if div.find('리트윗') == -1:
                    share = 0
                else:
                    share = div.split('리트윗')[0].strip()
                    if share.find(',') != -1:
                        share = div.split(',')[1].strip()

                if div.find('마음에') == -1:
                    like = 0
                else:
                    like = div.split('마음에')[0].strip()
                    if like.find(',') != -1:
                        like = div.split(',')[1].strip()
                        if like.find(',') != -1:
                            like = div.split(',')[1].strip()

                driver.get(url)
                time.sleep(1)
                html = driver.find_element_by_class_name("css-1dbjc4n").get_attribute('innerHTML')
                soup = BeautifulSoup(html,'html.parser')
                article = soup.find('article', role="article")

                contents = article.find('div', dir="auto", lang="ko").text.replace('\n', '').strip()
                date = article.find_all('div', 'r-qvutc0', dir="auto")[3].find_all('span')[1].text.strip()
                writeDate = getTime(date)

                result = checkKeyword(contents,dbKey[key]['add'],dbKey[key]['del'])
                if result:
                    # if writeDate < checkDay.strftime('%Y-%m-%d'):
                    #     check = False;break
                    if writeDate < '2020-06-01':
                        check = False;break
                    putKey = getPutKeyword(contents,dbKey[key]['add'])
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = {
                        'sns_name': 'twitter',
                        'sns_title': remove_emoji(writer)+"#"+(putKey.replace("#","")), #제목
                        'sns_content': remove_emoji(contents), # 내용
                        'url': url, # url
                        'title_key': dbKey[key]['add'][0],
                        'keyword': putKey, # 키워드
                        'writeDate': writeDate, # 날짜
                        'sns_writer': remove_emoji(writer), # 글쓴이
                        'like_cnt': like, # 좋아요 수
                        'share_cnt': share, # 공유 수
                        'reply_cnt': reply, # 댓글 수
                        'createDate': now,
                        'updateDate': now
                    }
                    # print(data)
                    # print('============================================')

                    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                    conn2 = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        placeholders = ', '.join(['%s'] * len(data))
                        columns = ', '.join(data.keys())
                        sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                        curs.execute(sql, list(data.values()))
                        curs2.execute(sql, list(data.values()))
                        insertNum = insertNum+1
                    except Exception as e:
                        if e.args[0] == 1062:
                            sql = "UPDATE sns_data SET title_key=%s, like_cnt=%s, reply_cnt=%s, share_cnt=%s, updateDate=%s WHERE url=%s;"
                            curs.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['updateDate'],data['url']))
                            curs2.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['updateDate'],data['url']))
                            updateNum = updateNum+1
                        else:
                            print("DB에러:",e)
                    else:
                        conn.commit()
                        conn2.commit()
                    finally:
                        conn.close()
                        conn2.close()

            check = False;break

        print("insert : ",insertNum,"/update :",updateNum)
        print("=======================")
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    # 키워드 가져오기
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    # 크롤링 시작
    print("트위터 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '성난황소':
        #     startCrawling(k)
        startCrawling(k)
    print("트위터 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
