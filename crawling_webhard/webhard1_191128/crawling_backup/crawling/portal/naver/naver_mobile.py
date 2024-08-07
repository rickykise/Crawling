import datetime,pymysql,time
import sys,os
import re
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'reply_data'
        data = {
            'ME_type': args[0],
            'ME_name': args[1],
            'ME_rank': args[2],
            'ME_title': args[3],
            'writeDate': args[4],
            'title_key': args[5],
            'keyword': args[6],
            'keyword_type': args[7],
            'uid': args[8],
            'url': args[9],
            'reporter_name': args[10],
            'reporter_media_name': args[11],
            'createDate': now,
            'updateDate':now
        }
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        # print(sql)
        curs.execute(sql, list(data.values()))
        conn.commit()
    except Exception as e:
        if e.args[0] != 1062:
            print("===========에러==========\n에러 : ",e,"\n",args,"\n===========에러==========")
        else:
            result = True
            conn.rollback()
    finally:
        return result

# 기자 가져오는 함수
def getReporter(conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT reporter_media_name,reporter_name  FROM reporter_data;'
        curs.execute(sql)
        result = curs.fetchall()


        returnValue = {}
        for i in range(len(result)):
            media = result[i][0].replace("\ufeff","")
            if media in returnValue:
                returnValue[media].append(result[i][1])
            else:
                returnValue.update({media:[result[i][1]]})
        # print(returnValue)

        return returnValue

#기자 체크
def checkReporter(content, reportern):
    returnValue = {
        'm' : None,
        'r' : None
    }

    for s in reportern.keys():
        if content.find(s) != -1 :
            for m in reportern[s]:
                if content.find(m) != -1 :
                    returnValue['m'] = s
                    returnValue['r'] = m

    return returnValue

def main():
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        link = "https://m.naver.com/"
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        try:
            driver.get(link)
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="nav"]/div[3]/nav/ul/li[2]').click()
            time.sleep(10)
            html = driver.find_element_by_class_name('id_ent').get_attribute('innerHTML')
        finally:
            driver.close()

        soup = BeautifulSoup(html,"html.parser")
        arr = []
        arr.extend(soup.find('div',{'class':'id_uio_thumbnail','index':'0'}).find_all('li','ut_item'))
        arr.extend(soup.find('div',{'class':'id_uio_text','index':'1'}).find_all('li','ut_item'))
        arr.extend(soup.find('div',{'class':'id_uio_thumbnail','index':'2'}).find_all('li','ut_item'))
        arr.extend(soup.find('div',{'class':'id_cui_cluster','index':'6'}).find_all('li','cc_item'))

        count = 1
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dbKey = getSearchKey(conn,curs)
        for value in arr:
            data = {
                'ME_type':'ent',
                'ME_name':'naver',
                'ME_rank':None,
                'ME_title':None,
                'writeDate':now,
                'url':None,
                'createDate':now,
                'updateDate':now
            }
            item = value.find('a','ut_a')
            if item is None:
                item = value.find('a','cc_la')
            data['ME_rank'] = count
            data['ME_title'] = item.get_text(' ',strip=True).strip()
            data['url'] = item['href']
            try:
                if data['url'].find('/video/') != -1:
                    data['uid'] = data['url'].split('/video/')[-1]
                elif data['url'].find('?') != -1:
                    num = None
                    # print(data['url'])
                    if data['url'].find('id=') != -1:
                        numlst = [i for i in data['url'].split('?')[1].split('&') if i.find('id=') != -1]
                        num = (len(numlst) > 1) and [i for i in numlst if i.find('a') != -1][0] or numlst[0]
                    elif data['url'].find('volumeNo=') != -1:
                        numlst = [i for i in data['url'].split('?')[1].split('&') if i.find('volumeNo=') != -1]
                        num = numlst[0]
                    elif data['url'].find('dummy=') != -1:
                        num = data['url'].split('?')[1].replace('dummy=','')

                    if num:
                        data['uid'] = re.sub('[^0-9]', '', num)

            except:
                pass

            mkey = getMainKeyword(dbKey,data['ME_title'])
            if mkey:
                paramKey = None
                data['title_key'] = dbKey[mkey]['add'][0]
                data['keyword'] = getPutKeyword(data['ME_title'],None,dbKey[mkey]['add'])

                if data['keyword']:
                    data['keyword_type'] = getPutKeywordType(data['keyword'],conn,curs)
                    data['keyword_type'] = (data['keyword_type'] == None) and '' or data['keyword_type']

            # print(data)
            try:
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = "INSERT INTO mobileent_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                curs.execute(sql, list(data.values()))
                conn.commit()
            except Exception as e:
                if e.args[0] != 1062:
                    print("===========에러==========\n에러 : ",e,"\n",args,"\n===========에러==========")
            count = count + 1
    finally:
        conn.close()

if __name__=='__main__':
    start_time = time.time()

    print("모바일 연예 크롤링 시작")
    main()
    print("모바일 연예 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
