import datetime,pymysql,time
import sys,os
import re
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

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
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        link = "https://m.naver.com/"
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="nav"]/a').click()
        time.sleep(3)

        html = driver.find_element_by_class_name("ma_inner").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        countLi = 0
        li = soup.find("ul", 'ma_list').find_all("li")
        for item in li:
            countLi = countLi + 1
            if item.find('a')['data-panel'] == 'MOVIE':
                countLi + 1
                # print(countLi)
                driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li['+str(countLi)+']').click()
                time.sleep(3)
                continue
        #driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[6]').click()
        # time.sleep(1)
        #driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[7]').click()
        #time.sleep(1)
        #driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[8]').click()
        #time.sleep(1)
        #driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[9]').click()
        #time.sleep(1)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[10]').click()
        # time.sleep(1)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[11]').click()
        # time.sleep(1)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[12]').click()
        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[13]').click()
        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[14]').click()
        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[15]').click()
        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[16]').click()
        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[18]').click()
        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="_MM_THUMBNAIL_AREA"]/li[19]').click()
        # time.sleep(3)

        driver.find_element_by_xpath('//*[@id="_MM_SAVE"]').click()
        time.sleep(10)
        html = driver.find_element_by_class_name('id_movie').get_attribute('innerHTML')
        soup = BeautifulSoup(html,"html.parser")
        li = soup.find('div','brick-vowel').find_all('li','ct_item')

        count = 1
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dbKey = getSearchKey(conn,curs)
        dbreporter = getReporter(conn,curs)
        for value in li:
            data = {
                'ME_type':'movie',
                'ME_name':'naver',
                'ME_rank':None,
                'ME_title':None,
                'writeDate':now,
                'uid':None,
                'url':None,
                'reporter_name':None,
                'reporter_media_name':None,
                'createDate':now,
                'updateDate':now
            }
            item = value.find('a','ct_a')
            if item is None:
                continue
            data['ME_rank'] = 0
            data['ME_title'] = item.get_text(' ',strip=True).strip()
            data['url'] = item['href']
            href = data['url']
            print(href)
            if href.find('m.entertain.naver.com/movie/now/read?') != -1 or href.find('M.entertain.naver.com/movie/now/read?') != -1:
                driver.get(href)
                time.sleep(3)
                page_main = driver.find_element_by_class_name("newsct_body").get_attribute('innerHTML')
                tags = BeautifulSoup(page_main,'html.parser')
                content = tags.find('div', 'newsct_article go_trans').text.replace("\n","").replace("\t","")
                reporter = checkReporter(content, dbreporter)
                # print(reporter)
                data['reporter_media_name'] = reporter['m']
                data['reporter_name'] = reporter['r']
            elif href.find('entertain.naver.com/movie/now/read?') != -1:
                driver.get(href)
                time.sleep(3)
                page_main = driver.find_element_by_class_name("end_ct_area").get_attribute('innerHTML')
                tags = BeautifulSoup(page_main,'html.parser')
                content = tags.find('div', 'end_body_wrp').text.replace("\n","").replace("\t","")
                reporter = checkReporter(content, dbreporter)
                # print(reporter)
                data['reporter_media_name'] = reporter['m']
                data['reporter_name'] = reporter['r']
            try:
                if href.find('/postView') != -1:
                    driver.get(href)
                    time.sleep(3)
                    if driver.find_element_by_class_name("se_doc_viewer").get_attribute('innerHTML'):
                        page_main = driver.find_element_by_class_name("se_doc_viewer").get_attribute('innerHTML')
                        tags = BeautifulSoup(page_main,'html.parser')
                        content = tags.find('div', 'se_component_wrap sect_dsc __se_component_area').text.replace("\n","").replace("\t","")
                        reporter = checkReporter(content, dbreporter)
                        data['reporter_media_name'] = reporter['m']
                        data['reporter_name'] = reporter['r']
                    elif driver.find_element_by_class_name("se_body_wrap").get_attribute('innerHTML'):
                        page_main = driver.find_element_by_class_name("se_body_wrap").get_attribute('innerHTML')
                        tags = BeautifulSoup(page_main,'html.parser')
                        content = tags.find('div', 'se_card_textArea').text.replace("\n","").replace("\t","")
                        # print(content)
                        reporter = checkReporter(content, dbreporter)
                        data['reporter_media_name'] = reporter['m']
                        data['reporter_name'] = reporter['r']
            except:
                pass
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
                # else:
                #     data['uid'] = data['url'].split('/')[-1]
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

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            curs = conn.cursor(pymysql.cursors.DictCursor)
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
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("모바일 영화 크롤링 시작")
    main()
    print("모바일 영화 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
