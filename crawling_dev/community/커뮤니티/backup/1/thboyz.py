# 디시인사이드 검색
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from commonFun import *
import time,pymysql,re,datetime
import requests

def startCrawling(key):
    print("키워드 : ",key)
    check = False;paramKey = None;insertNum = 0
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        for i in range(1,6):
            r = requests.get("http://search.dcinside.com/post/p/"+str(i)+"/sort/latest/q/"+key,timeout=10)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            all = soup.find("div", "integrate_cont")
            ul = all.find('ul', 'sch_result_list')
            searchDIV = all.find_all("li")

            for item in searchDIV:
                data = {'title' : '','url' : '','contents' : '','date':'','writer':'','ip':'','board_number':''}
                try:
                    driver.get(item.find("a",{"class","tit_txt"})['href'])
                    wait = WebDriverWait(driver, 5)
                    data['title'] = (item.find("a",{"class","tit_txt"}).text == False) and '' or item.find("a",{"class","tit_txt"}).text.split('-')[0].strip()
                    data['url'] = "http://m.dcinside.com/view.php?" + item.find("a",{"class","tit_txt"})['href'].replace("#1","").strip().split("view/?")[1]
                    data['board_number'] = data['url'].split("&no=")[1].split("&")[0]
                    contents = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/section/article[2]/div[1]/div/div[1]/div[1]'))).text.replace("\n","").replace("\t","")
                    data['contents'] = setText(contents,0)
                    try:
                        dateCheck = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/section/article[2]/div[1]/header/div/div/div[1]/span[3]'))).text
                        cyear = datetime.datetime.now().strftime('%Y')
                        date = datetime.datetime.strptime(dateCheck, "%m-%d %H:%M:%S").strftime(cyear+'-%m-%d %H:%M:%S')
                        data['date'] = date
                    except:
                        continue
                    data['writer'] = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="container"]/section/article[2]/div[1]/header/div/div/div[1]/span[1]'))).text
                    try:
                        data['ip'] = driver.find_element_by_xpath('//*[@id="container"]/section/article[2]/div[1]/header/div/div/div[1]/span[2]').text.split("(")[1].split(")")[0]
                    except:
                        data['ip'] = ''
                except Exception as e:
                    print('에러:'+e)
                    driver.refresh()
                    continue
                if data['date'] < '2019-01-07': check=True;break

                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)

                if result:
                    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        data['title'] = (len(data['title']) > 255) and data['title'][:240]+"…" or data['title']
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                        putKeyType = getPutKeywordType(putKey,conn,curs)
                        dbResult = insert(conn,'dcinside',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        if dbResult:
                            check=False
                    finally :
                        conn.close()

            if check: break
    except:
        pass
    finally:
        driver.quit()

    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()
    keywordSet = ['학치커','즉연','학치']

    print("디시인사이드 크롤링 시작")
    # for k in dbKey.keys():
    #     if dbKey[k]['add'][0] == '더보이즈':
    #         startCrawling(k)
    #     # startCrawling(k)
    for k in keywordSet:
        startCrawling(k)
    print("디시인사이드 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
