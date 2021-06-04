import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from webhardFun import *
global host

def startCrawling(site):
    i = 0;check = True;cate = '0'
    if site == '0':
        cate = '1'
    else:
        cate = '2'
    link = 'http://www.filenori.com/noriNew/Contents/contentsList.do?data=%7B%22searchType%22%3A%22'+cate+'%22%2C%22etcSearchType%22%3A%22%22%2C%22category%22%3A%220'+site+'%22%2C%22subCategory%22%3A%22%22%2C%22subOption%22%3A%22%22%2C%22searchCategory%22%3A%2202%22%2C%22searchSubCategory%22%3A%22%22%2C%22searchArea%22%3A%2221%22%2C%22searchKeyword%22%3A%22%22%2C%22searchSort%22%3A%225%22%2C%22pageViewRow%22%3A%2220%22%2C%22pageViewPoint%22%3A%22'
    link2 = '%22%2C%22pageTotal%22%3A%2297000%22%2C%22pageBaseID%22%3A%2268117031%22%7D'
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get('https://www.filenori.com/common/html/member/loginForm.html?20181005')
        time.sleep(2)
        print('새로고침중.../')
        driver.refresh()
        time.sleep(2)
        driver.find_element_by_id('userID').send_keys('up555')
        driver.find_element_by_id('userPW').send_keys('djq5555555')
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div/form/ul/li[2]/input').click()
        time.sleep(2)
        while check:
            i = i+1
            if i == 4:
                break
            driver.get(link+str(i)+link2)
            time.sleep(2)
            html = driver.find_element_by_class_name("contents_main").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")

            for item in tr:
                td = item.find_all('td')
                if len(td) < 2:
                    continue
                if item.find('img', alt='19'):
                    continue
                titleCheck = item.find('td')['title']
                title_nullCheck = titleNull(titleCheck)
                cnt_num = item.find('td')['id'].split("c")[1]
                url = "http://www.filenori.com/noriNew/contentsView.do?contentsID="+cnt_num

                # 키워드 체크
                conn = host
                curs = conn.cursor(pymysql.cursors.DictCursor)
                getKey = getKeyword(conn,curs)
                keyCheck = checkTitle(title_nullCheck, getKey)
                if keyCheck['m'] == None:
                    dbResult = insertDB('filenori',titleCheck,title_nullCheck,url)
                    continue
                keyCheck2 = checkTitle2(title_nullCheck, getKey)
                if keyCheck2['m'] == None:
                    dbResult = insertDB('filenori',titleCheck,title_nullCheck,url)
                    continue
                id = item.find('span')['onclick']
                cnt_vol = item.find_all('td')[1].text.strip()
                cnt_price = item.find_all('td')[2].text.replace("캐시","").replace(" ","").replace(",","").strip()
                cnt_writer = item.find_all('td')[4].text.strip()
                title = ''
                cnt_chk = 0
                time.sleep(2)
                driver.execute_script(id)
                time.sleep(2)
                if len(driver.window_handles) == 2:
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)
                    html = driver.find_element_by_id("body_view").get_attribute('innerHTML')
                    soup = BeautifulSoup(html,'html.parser')
                    cnt_chk = 0

                    title = soup.find('li', 'title fl contentsTitle')['title']
                    title_null = titleNull(title)
                    if soup.find('div', 'cooperateIcon'):
                        cnt_chk = 1
                    headers = {
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Cache-Control': 'no-cache',
                        'Connection': 'Keep-Alive',
                        'Content-Length': '19',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Cookie': 'event290=off; noriNID=dXA1NTU%3D; NSHcookie=200907221b0a72d26c6f0003; eventDesignVer=1060; JSESSIONID=8348E9D5CBC5B20A398A3B8E64745CEB',
                        'Host': 'www.filenori.com',
                        'Referer': url,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    Page = {
                        'contentsID': cnt_num
                    }
                    with requests.Session() as s:
                        flist = s.post('http://www.filenori.com/noriNew/contentsFileList.do', headers=headers, data=Page)
                        fsoup = bs(flist.text, 'html.parser')
                        fname = fsoup.find('div')['title']

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'filenori',
                            'Cnt_title': title,
                            'Cnt_title_null': title_null,
                            'Cnt_url': url,
                            'Cnt_price': cnt_price,
                            'Cnt_writer' : cnt_writer,
                            'Cnt_vol' : cnt_vol,
                            'Cnt_fname' : fname,
                            'Cnt_chk': cnt_chk
                        }
                        # print(data)

                        conn2 = host
                        try:
                            curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                            dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                            insertDB('filenori',titleCheck,title_nullCheck,url)
                        except Exception as e:
                            print(e)
                            pass
                        finally :
                            conn2.close()

                elif len(driver.window_handles) == 1:
                    continue
                elif title == '':
                    continue
                else:
                    continue

    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("filenori 크롤링 시작")
    site = ['0','1','2','3','5']
    for s in site:
        startCrawling(s)
    print("filenori 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
