import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def setData(num,driver):
    url = 'http://soccerline.kr/board/'+num
    driver.execute_script("window.open('"+url+"');")
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after)

    data=None
    try:
        data = {
            'title' : driver.find_element(By.XPATH,'//*[@id="container"]/div/section[2]/div/div[2]/h2').text.strip(),
            'url' : url,
            'contents' : driver.find_element(By.XPATH,'//*[@id="container"]/div/section[2]/div/div[4]').text.replace('\n',' ').replace('\t',' ').strip(),
            'date': driver.find_element(By.XPATH,'//*[@id="container"]/div/section[2]/div/div[3]/ul/li[2]/div/span[1]').text.replace('작성일: ','').strip(),
            'writer': driver.find_element(By.XPATH,'//*[@id="container"]/div/section[2]/div/div[3]/ul/li[1]/div').text.strip(),
            'ip': driver.find_element(By.XPATH,'//*[@id="container"]/div/section[2]/div/div[3]/ul/li[2]/div/span[2]').text.replace('IP:','').strip(),
            'board_number': num
        }
        print(data)
    except:
        pass
    finally:
        driver.close()

    return data

def startCrawling():
    idx=0;insertNum = 0;paramKey = None;check = True
    link = 'http://soccerline.kr/board?searchWindow=&searchType=0&searchText='+key+'&categoryDepth01=0&page='
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            driver.get(link+str(idx))
            time.sleep(3)
            textHtml = driver.find_element(By.XPATH,'//*[@id="boardListContainer"]/div/table/tbody').get_attribute('innerHTML')
            soup = BeautifulSoup(textHtml,'html.parser')
            trEles = soup.find_all("tr")
            if len(trEles) <= 3:
                break
            for item in trEles:
                tdEles = item.find_all('td',limit=4)
                if tdEles[0].text == '[공지]':continue
                dateCheck = tdEles[3].text.find(':')
                # print(dateCheck)
                if dateCheck == -1: check=False;break

                # dateCheck = tdEles[3].text
                #
                # if dateCheck < datetime.date.today().strftime('%Y-%m-%d'):
                #     check=False;break

                data = setData(tdEles[0].text,driver)
                driver.switch_to_window(driver.window_handles[0])
                if not data: continue

                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if result:
                    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                        putKeyType = getPutKeywordType(putKey,conn,curs)
                        dbResult = insert(conn,'soccerline',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        if dbResult:
                            check = False;break
                    finally :
                        conn.close()
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

    print("사커라인 크롤링 시작")
    for key in dbKey.keys():
        print("키워드 :",key)
        startCrawling()
    print("사커라인 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
