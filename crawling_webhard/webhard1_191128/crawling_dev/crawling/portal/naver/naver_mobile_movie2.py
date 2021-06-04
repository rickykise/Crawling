import datetime,pymysql,time
import sys,os
import re
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

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
                    print(data['url'])
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

            # try:
            #     placeholders = ', '.join(['%s'] * len(data))
            #     columns = ', '.join(data.keys())
            #     sql = "INSERT INTO mobileent_data ( %s ) VALUES ( %s );" % (columns, placeholders)
            #     curs.execute(sql, list(data.values()))
            #     conn.commit()
            # except Exception as e:
            #     if e.args[0] != 1062:
            #         print("===========에러==========\n에러 : ",e,"\n",args,"\n===========에러==========")
            # count = count + 1
    finally:
        conn.close()

if __name__=='__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" %(time.time() - start_time))
