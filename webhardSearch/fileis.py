import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key):
    i = 0;check = True
    print(key)
    encText = urllib.parse.quote(key)
    with requests.Session() as s:
        link = 'http://fileis.com/contents/search.php?category1=&s_column=title&sCode='+encText+'&emCopy=N&s_word='+encText
        while check:
            i = i+1
            if i == 30:
                break
            try:
                r = requests.get(link)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                table = soup.find_all('table', 'boardtype1')[1]
                tr = table.find('tbody').find_all('tr', 'bbs_list')

                for item in tr:
                    cnt_num = item['data-idx']
                    url = "http://fileis.com/contents/view.htm?idx=" + cnt_num
                    headers = {
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Referer': 'http://fileis.com/contents/index.htm',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Cookie': '_ga=GA1.2.1547453409.1547110039; _gid=GA1.2.2142846955.1547110039; 1d67d4faecf228042770ca9c7c28f634=YTE3YWNkNTYzNmI4YjIyYjkwNGQyZWE1NmY0NmIzZTE%3D; 92b0eb816645a04605a0caee3c08e6f2=NjEuODIuMTEzLjE5Ng%3D%3D; openedIdx=a%3A4%3A%7Bi%3A13713476%3Bi%3A1547166743%3Bi%3A13700884%3Bi%3A1547166947%3Bi%3A12993257%3Bi%3A1547168937%3Bi%3A13050837%3Bi%3A1547168955%3B%7D'
                    }

                    post_one  = s.get(url, headers=headers)
                    soup = bs(post_one.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('title').text.strip()
                    if title.find(key) != -1:
                        break
                    title_null = titleNull(title)
                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('fileis',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('fileis',title,title_null,url)
                    #     continue
                    cnt_check = soup.find('td', 'pad_left5').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip()
                    cnt_vol = soup.find('td', 'pad_left5').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip().split("/")[0]
                    cnt_pricecheck = cnt_check.count('P')
                    if cnt_pricecheck == 1:
                        cnt_price = soup.find('td', 'pad_left5').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("/")[1].split("P")[0]
                    else:
                        cnt_price = soup.find('td', 'pad_left5').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("P")[1].split("P")[0]
                    cnt_fname = soup.find('div', 'ftb_name').text.strip()
                    cnt_writer = soup.find('span', 'bold mar_rig5').text.strip()
                    if soup.find('li', 'tit_le2'):
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'fileis',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                pass

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("fileis 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("fileis 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
