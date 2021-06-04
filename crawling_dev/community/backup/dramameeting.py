from commonFun import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import datetime,time,pymysql
import urllib.request

def getContents(url):
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(url)
        ele = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME,'container')))
        soup = BeautifulSoup(ele.get_attribute("innerHTML"),"html.parser")
    except TimeoutException:
        return
    finally:
        driver.quit()
    data = None
    try:
        info = soup.find_all("td","han")[1]
        name = info.find("span","",title="").text
        if name == '':
            name = info.find("span","",title="").find("img",align="absmiddle")['alt']
        data = {
            'title' : remove_emoji(info.find("font","view_title2").text.strip()),
            'contents' : remove_emoji(soup.find("td","board-contents").get_text(strip=True).strip().replace('\xa0','')),
            'date' : [item for item in str(soup.find("table","info_bg").find("table").find_all("td")[4]).split("<br/>") if item.find("등록일:") != -1][0].replace("등록일:","").replace("\n","").strip(),
            'url' : soup.find("span",id="url_container").findNextSibling('input')['value'],
            'board_number' : '',
            'ip':' ',
            'writer' : remove_emoji(name),
        }
        data['board_number'] = data['url'].split("&no=")[1]
    except:
        pass

    return data

def startCrawling():
    print("키워드 : ",key)
    driver = webdriver.PhantomJS("c:/python36/phantomjs/bin/phantomjs")

    paramKey = None;check=True;i = 0
    if key == '공유' or key == '정유미': paramKey = key
    encText = urllib.parse.quote(key,encoding="euc-kr")
    site = "http://www.ppomppu.co.kr/search_bbs.php?search_type=sub_memo&keyword="+encText+"&page_size=50&bbs_id=&order_type=date&bbs_cate=2&page_no="
    try:
        while check:
            i = i+1
            try:
                driver.get(site+str(i))
                ele = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME,'search_result')))
                soup = BeautifulSoup(ele.get_attribute("innerHTML"),"html.parser")
                divEles = soup.find_all("div","item");
                if len(divEles) == 0: break
            except TimeoutException:
                print("TimeoutException")
                continue
            except Exception as e:
                print(e)
                break

            for item in divEles:
                date = item.find("div","content").find("p","desc").find_all("span")[2].text
                if date < datetime.date.today().strftime("%Y.%m.%d"):
                    check=False;break

                data = getContents(item.find("span","title").find("a")['href'])
                if not data:
                    continue

                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)

                if result:
                    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                    conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                        putKeyType = getPutKeywordType(putKey,conn,curs)
                        dbResult = insert(conn,'dramameeting',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        insert(conn2,'dramameeting',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        if dbResult:
                            check=False;break
                    finally:
                        conn.close()
                        conn2.close()
    finally:
        driver.quit()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("dramameeting 크롤링 시작")
    for key in dbKey.keys():
        startCrawling()
    print("dramameeting 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
