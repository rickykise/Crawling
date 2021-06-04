#네이버 talk
import datetime,pymysql,time
from datetime import date, timedelta
import sys,os
import urllib.request
import requests,re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'navertalk_data'
        data = {
            'portal_content': args[0],
            'portal_name': 'naver',
            'writer': args[1],
            'writeDate': args[2],
            'title_key': '더보이즈',
            'keyword': '더보이즈',
            'url': args[3],
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

def startCrawling():
    try:
        url = 'https://m.search.naver.com/search.naver?query=%EB%8D%94%EB%B3%B4%EC%9D%B4%EC%A6%88&where=m&sm=mtp_hty#api=%3Fwhere%3Dbridge%26query%3D%25EB%258D%2594%25EB%25B3%25B4%25EC%259D%25B4%25EC%25A6%2588%26tab_prs%3Dcsa%26col_prs%3Drea%26tab%3Dtalk%26format%3Dtext%26nqx_theme%3D%257B%2522theme%2522%253A%257B%2522main%2522%253A%257B%2522name%2522%253A%2522people_star%2522%252C%2522score%2522%253A%25221.000000%2522%252C%2522os%2522%253A%25226120529%2522%252C%2522pkid%2522%253A%25221%2522%257D%257D%257D%26sm%3Digr_brg&_lp_type=cm'
        link = url
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)

        for i in range(0, 30) :
            try:
                driver.find_element_by_xpath('//*[@id="_sau_bridge_star_search_talk"]/div/div[6]/a').click()
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                i +=1
            except:
                break

        print('시작')
        html = driver.find_element_by_id("_sau_bridge_star_search_talk").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        ul = soup.find('ul', 'u_cbox_list')
        li = ul.find_all('li')
        print(len(li))

        for items in li:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            content = items.find('div', 'u_cbox_text_wrap').find('span', 'u_cbox_contents').text.strip()
            writer = items.find('div', 'u_cbox_info').find('span', 'u_cbox_nick').text.strip()
            objectId = items.find('div', 'u_cbox_info_base').find('a')['data-param'].split("star_")[1].split("'")[0]
            commentNo = items.find('div', 'u_cbox_info_base').find('a')['data-param'].split("commentNo:")[1].split(",")[0]
            writeDatech = items.find('div', 'u_cbox_info_base').find('span', 'u_cbox_date')['data-value'].split("+")[0]
            writeDate = datetime.datetime.strptime(writeDatech, "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            url = 'http://srp.naver.com/main.nhn?itemSvcCd=CBM&itemVirtualSvcCd=STK&itemType=CMNT&itemId=starsearch%3Bdefault%3Bstar_'+objectId+'%3B'+commentNo+'&itemTitle='+content+'&itemCateId=STK_001&itemCateName=%EC%8A%A4%ED%83%80TALK_%EB%8C%93%EA%B8%80&itemCateLevel=0&itemCateId=STK_001%3B001&itemCateName=%EC%8A%A4%ED%83%80TALK_%EB%8C%93%EA%B8%80&itemCateLevel=1&itemCateId=STK_001%3B001%3B001&itemCateName=%EC%8A%A4%ED%83%80TALK_%EB%8C%93%EA%B8%80&itemCateLevel=2&itemWriterNick='+writer+'&memberType=Y&reportCountryCd=KR&reportLangCd=ko&m=rprtFrm'

            data = {
                'portal_content': content,
                'writer': writer,
                'writeDate': writeDate,
                'url': url,
                'createDate': now,
                'updateDate':now
            }
            # print(data)

            conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                dbResult = insert(conn,data['portal_content'],data['writer'],data['writeDate'],data['url'],data['createDate'],data['updateDate'])
                if dbResult:
                    return False
            finally :
                conn.close()

    except:
        pass
    finally:
        driver.close()


if __name__=='__main__':
    start_time = time.time()

    print("네이버 talk 크롤링 시작")
    startCrawling()
    print("네이버 talk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
