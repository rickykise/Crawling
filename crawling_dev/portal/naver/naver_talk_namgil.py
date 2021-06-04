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
            'title_key': '김남길',
            'keyword': '김남길',
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

# 이모티콘 삭제 처리 1
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

def startCrawling():
    try:
        url = 'https://m.entertain.naver.com/tvBrand/6490039/talk'
        url = urllib.parse.unquote(url)
        link = url
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)

        for i in range(0, 30) :
            try:
                driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div[7]/a').click()
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                i +=1
            except:
                break

        html = driver.find_element_by_class_name("u_cbox_content_wrap").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        ul = soup.find('ul', 'u_cbox_list')

        li = ul.find_all('li')
        print(len(li))

        for items in li:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            content = items.find('span', 'u_cbox_contents').text.strip()
            content = remove_emoji(content)
            writer = items.find('span', 'u_cbox_nick').text.strip()
            objectId = items.find('a', 'u_cbox_btn_report')['data-param'].split("objectId:'")[1].split("'")[0]
            commentNo = items.find('a', 'u_cbox_btn_report')['data-param'].split("commentNo:")[1].split(",")[0]
            writeDatech = items.find('span', 'u_cbox_date')['data-value'].split("+")[0]
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
            # print('=========================================')

            conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
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
