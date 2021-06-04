# 디시인사이드 검색
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from commonFun import *
import time,pymysql,re,datetime
import requests
import urllib.parse

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'PHPSESSID=77b945962e032dfb088b10a7b3b0072f; __utmc=118540316; __utmz=118540316.1578368789.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ck_lately_gall=8F%7C2JG%7Chj%7CJb%7CE9; __gads=ID=4fa7eaabd018c53b:T=1578368786:S=ALNI_Mb0RzPpVAxVALHSuFCCH5X7zskKvQ; last_alarm=1580714218; __utma=118540316.1484170209.1578368788.1578635810.1580714219.4; __utmb=118540316.2.10.1580714219; _ga=GA1.2.1484170209.1578368788; __utmt=1; ci_c=36a72830487d8cfc230bdbcb919b3f45; alarm_popup=1; p214Cap=1; wcs_bt=f92eaecbc22aac:1580714219; p214=1',
    'Host': 'gall.dcinside.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    check = False;paramKey = None;insertNum = 0;key = '김선호'
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        for i in range(1,3):
            r = requests.get("https://gall.dcinside.com/board/lists/?id=drama_new3&page="+str(i)+"&search_pos=&s_type=search_subject_memo&s_keyword="+key,timeout=10, headers=headers)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            table = soup.find("table", "gall_list").find('tbody')
            tr = table.find_all("tr", 'ub-content us-post')

            for item in tr:
                try:
                    driver.get('https://gall.dcinside.com'+item.find("a")['href'])
                    wait = WebDriverWait(driver, 5)
                    title = (item.find("a").text == False) and '' or item.find("a").text.split('-')[0].strip()
                    url = 'https://gall.dcinside.com'+item.find("a")['href'].replace("#1","").strip().replace("http://", "https://")
                    url = urllib.parse.unquote(url)
                    countNum = countNumget(url)
                    if countNum >= 1:
                        continue
                    board_number = item.find('td', 'gall_num').text.strip()

                    contents = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/section/article[2]/div[1]/div/div[1]/div[1]'))).text.replace("\n","").replace("\t","").replace("<iframe","").replace("<frame","")
                    contents = setText(contents,0)
                    try:
                        dateCheck = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/section/article[2]/div[1]/header/div/div/div[1]/span[3]'))).text
                        date = datetime.datetime.strptime(dateCheck, '%Y.%m.%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        continue
                    writer = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/section/article[2]/div[1]/header/div/div/div[1]/span[1]'))).text
                    try:
                        ip = driver.find_element_by_xpath('//*[@id="container"]/section/article[2]/div[1]/header/div/div/div[1]/span[2]').text.split("(")[1].split(")")[0]
                    except:
                        ip = ''
                    data = {
                        'title' : title,
                        'url' : url,
                        'contents' : contents,
                        'date': date,
                        'writer': writer,
                        'ip': ip,
                        'board_number': board_number
                    }
                    # print(data)
                    # print("=================================")
                except:
                    continue

                # if data['date'] < datetime.datetime.now().strftime('%Y-%m-%d'): check=True;break

                if key == '공유' or key == '정유미': paramKey = key

                conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                conn2 = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    data['title'] = (len(data['title']) > 255) and data['title'][:240]+"…" or data['title']
                    # putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    # putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'dcinside',data['title'],data['contents'],data['writer'],data['ip'],data['date'],'김선호','김선호','배우',data['url'],data['board_number'])
                    insert(conn2,'dcinside',data['title'],data['contents'],data['writer'],data['ip'],data['date'],'김선호','김선호','배우',data['url'],data['board_number'])
                    if dbResult:
                        check=True;break
                finally:
                    conn.close()
                    conn2.close()
            if check: break
    except:
        pass
    finally:
        driver.quit()

if __name__=='__main__':
    start_time = time.time()

    print("디시인사이드 크롤링 시작")
    startCrawling()
    print("디시인사이드 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
