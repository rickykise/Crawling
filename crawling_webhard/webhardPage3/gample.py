import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

LOGIN_INFO = {
    'id': 'up0001',
    'passwd': 'up0001',
    'ret_url': 'http://www.gample.net/',
    'save_chk': ''
}

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0; a = 1;check = True
    with requests.Session() as s:
        login_req = s.post('https://mdb.gample.net/login/new_main_login.php', data=LOGIN_INFO)
        headers = {'Cookie': 'PHPSESSID=a9d80ce4b52965aa868aafdec12d8735; _ga=GA1.2.1701698505.1548046592; _gid=GA1.2.484728526.1548046592; event_num=0; gold_pop_chk=0; period_num=0; ics_sex=0; adult_auth=N; user_rank=0; return_cook_chk=0; vtvuser=%25B3%25D4%252C%2502%2523%2582%25CA%25D8%25AD%255C%25B3%252Cl%257C%2591%25A2-%25A9%25ABf%250CR%25B7%25006N%25F2%2515%2503%2584%2518%25C2%25BFK%25EC%253F%25E6%25DD%25BD%25BC%258A%25C3b%25BE9KV%2507w%251B%25D2%25DA3%2525G%25BE%259A%2589x%25B6r%258E%251D_%251F%2516C%25EB%25DC%2521%25EE%258B%259C%2504%258D%25C8%25FD%2519b%252BJ%259A%2585%25B3%25FC%25F6; V%2dTV=VFSS1.0%7C225763203163265663765773661%7CEBB0D17DF6907DAE525AA3312D7%7C1548052734%7C; VTVMSG=BEADFEFGFHFJBGBOBMALFBEDFFBKAKBEFKBHFNEHBNAGBEFGFHFIFLCLACFKBHBGBGEIAEAHAHBHFNEHFDEHFNFPFOBEFMFKECADFDFNFFFHFEEGFLFCFKEHBEADFEFGFGBEFLBH; VTVID=up0001%7C%7Cup0001%40naver.com%7C1%7Cm%7Cup001%7C0%7C1%7C20191%7C1548052734%7C3173234%7C0%7C0%7C0%7C0%7C0%7C0%7CN%7C%7C%7C%7C0%7C0%7C0; GP_AVATA=10000%7C10000%7C14999%7C24999%7C34999%7C52999%7C10000%7C10000%7C10000%7C10000%7C10000%7C10000%7C24999; GAMPLEID=02ffff0383008400c3fdfc0181018400c3ff500b6b5ea700f7ffefb8bc005400beffff2a2a0144002affff280b00760008ffff812b1c2c0001ffff0123bcf40001ffff555500000055f7f75f5f0800005ffcfca8a8000000a8; GAMPLE_CAFE=00; _gat=1'}
        sys.setrecursionlimit (2000)
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://webhard2.gample.net/index.php?cate_id='+site+'&num_per_page=50&page='
            post_one  = s.post(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            div = soup.find('div', id='bload')
            table = div.find_all('table')[4]
            tr = table.find_all('tr')
            try:
                for item in tr:
                    td = item.find_all('td')
                    if len(td) < 2:
                        continue
                    cnt_vol = item.find('td', align='right').text.strip().replace(" ","")
                    cnt_num = item.find('a', 'bbs_link01')['href'].split("num=")[1].split("&")[0]
                    url = 'http://webhard2.gample.net'+item.find('a', 'bbs_link01')['href'].split("'..")[1].split("','")[0]

                    post_two  = s.get(url, headers=headers)
                    soup = bs(post_two.text, 'html.parser')
                    table = soup.find('td', valign="top").find_all('table')[4]
                    cnt_chk = 0

                    title = soup.find('td', 'gray_b').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    if title.find('제휴') != -1:
                        title = title.split("/제휴")[0]
                        cnt_chk = 1
                    cnt_price = table.find_all('tr')[2].find_all('td')[4].text.split("골드")[0].strip().replace(",","")
                    cnt_writer = table.find_all('tr')[2].find_all('td')[2].text.split("/  ")[1].strip()

                    fname  = s.get(url)
                    soupf = bs(fname.text, 'html.parser')
                    cnt_fname = soupf.find('td', 'ft_12').text.replace("\xa0","").replace("\r","").replace("\n","").strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'gample',
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

                    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    except Exception as e:
                        print(e)
                        # pass
                    finally :
                        conn.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("gample 크롤링 시작")
    site = ['','A01','B01','C01','D01']
    for s in site:
        startCrawling(s)
    print("gample 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
