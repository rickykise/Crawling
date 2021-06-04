import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from webhardFun import *

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    tr = soup.find('table', 'clubfile_fileview_list').find_all('tr')
    cnt_fname = None

    if len(tr) == 2:
        cnt_fname = soup.find('table', 'clubfile_fileview_list').find_all('td', align='left')[1].text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip().split("ㄴ")[1]
    if len(tr) == 3:
        cnt_fname = soup.find('table', 'clubfile_fileview_list').find_all('td', align='left')[2].text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip().split("ㄴ")[1]
    if cnt_fname == None:
        pass

    data = {
        'Cnt_fname' : cnt_fname
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.diskstory.com/clubfile/index.php?start="
    link2 = "&clubid=&bbscode=&list_scale=27&code1="+site+"&p="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            driver.get(link+str(i)+link2)
            i = i+27
            time.sleep(2)
            html = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/table/tbody/tr/td/table').get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                td = item.find_all('td')
                if len(td) != 6:
                    continue
                else:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if item.find('span', 'list_club B').find('img'):
                        img = item.find('span', 'list_club B').find_all('img')
                        if len(img) == 1:
                            if item.find('span', 'list_club B').find('img')['src'].find('tab_icon_19') != -1:
                                continue
                        elif len(img) == 2:
                            if item.find('span', 'list_club B').find_all('img')[0]['src'].find('tab_icon_19') != -1:
                                continue
                    title = item.find('span', 'list_club B').find('a')['title']
                    cnt_vol = item.find_all('td')[3].text.strip()
                    cnt_writer = item.find_all('td')[5].text.strip()
                    subUrl = item.find('span', 'list_club B').find('a')['href'].split('("?')[1].split('");')[0]
                    url = 'http://www.diskstory.com/clubfile/clubfile_view_pop.php?' + subUrl
                    cnt_num = subUrl.split('&idx=')[1]
                    resultData = getContents(url)

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'diskstory',
                        'Cnt_title': title,
                        'Cnt_url': url,
                        'Cnt_price': '0',
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : resultData['Cnt_fname'],
                        'Cnt_regdate' : now,
                        'Cnt_chk': '1'
                    }
                    # print(data)

                    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn.close()
    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("diskstory 크롤링 시작")
    site = ['2','3','10','4']
    for s in site:
        startCrawling(s)
    print("diskstory 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
