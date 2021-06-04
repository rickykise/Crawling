import requests,re
import pymysql,time,datetime
import urllib.parse
from commonFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 :",key)
    paging = 1;paramKey = None
    encText = urllib.parse.quote(key.replace(' ',''),encoding="euc-kr")
    link = "http://web.humoruniv.com/search/search.html?section=humoruniv&order=uptime&search_text="+encText+"&page="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while True:
            driver.get(link+str(paging))
            time.sleep(3)
            html = driver.find_element_by_name("search_form").find_elements_by_tag_name("table")[1].find_elements_by_tag_name("div")[1].get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            table = list(soup.find_all("table",cellpadding="5"))
            if len(table) < 1: break

            for i in table:
                td = i.find("td",valign="top")
                url = td.find("a")['href']
                soup = None

                with requests.Session() as s:
                    s.mount(url, HTTPAdapter(max_retries=Retry(total=5, status_forcelist=[500, 503])))
                    r = s.get(url)
                    soup = BeautifulSoup(r.content.decode('euc-kr','replace'),"html.parser")
                    info = soup.find("table",id="profile_table")

                try:
                    info = soup.find("table",id="profile_table").find_all("td")[1].find("table")
                    contents = soup.find("div",id="wrap_body")
                except AttributeError:
                    continue

                title = info.find_all("td")[0].find("span",id="ai_cm_title").get_text(strip=True)
                contents = contents.get_text(strip=True)

                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(title,contents,dbKey[key]['add'],dbKey[key]['del'],paramKey)

                if result is False: continue

                ipTdate = info.find_all("td")[2].find("div",id="if_date").find_all("span")
                ip = ipTdate[0].get_text(strip=True)
                contents = setText(contents,0)
                data = {
                    'title' : title,
                    'url' : url,
                    'contents' : remove_emoji(contents),
                    'date': (ip.find(".xxx") != -1) and ipTdate[1].get_text(strip=True) or ip,
                    'writer': info.find_all("tr")[1].find("span","hu_nick_txt").get_text(strip=True),
                    'ip': (ip.find(".xxx") != -1) and ip or ' ',
                    'board_number': info.find_all("td")[2].find("div",id="content_info").find("span").get_text(strip=True)
                }
                # print(data)
                if data['date'] < datetime.datetime.now().strftime('%Y-%m-%d'): paging=11;break

                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'humoruniv',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'humoruniv',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        paging=11;break
                finally :
                    conn.close()
                    conn2.close()
            p = re.compile('\d+')
            pageCount = int(p.match(driver.find_element_by_xpath("/html/body/div[2]/div/form/table[2]/tbody/tr/td[1]/table[2]/tbody/tr/td/span").text.split("/")[1].strip()).group())
            paging = paging+1
            pageCount = (pageCount < 10) and pageCount or 10
            if pageCount < paging:break
    except:
        pass
    finally :
        driver.close()


if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("웃긴대학 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '레디 플레이어 원':
        #     startCrawling(k)
        startCrawling(k)
    print("웃긴대학 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
