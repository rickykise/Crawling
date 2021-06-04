import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key):
    i = 0;check = True
    # print(key)
    encText = urllib.parse.quote(key)
    # getKey = getKeywordW()
    with requests.Session() as s:
        while check:
            if i == 30:
                break
            Data = {
                'p': str(i),
                'search': key,
                'search_keyword': 'all',
                'search_type': 'all'
            }
            # print(str(i))
            i = i+1
            headers = {
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'filemong.com',
                'Referer': 'https://filemong.com/contents/list.html?search_type=all&search_keyword=all&section=&search='+encText,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'X-Requested-With': 'XMLHttpRequest'
            }

            try:
                link = 'https://filemong.com/contents/search_ajax.php'
                post_one  = s.post(link, headers=headers, data=Data)
                soup = bs(post_one.text, 'html.parser')
                li = soup.find('ul', 'content-list').find_all('li')
                if len(li) < 2:
                    # print('게시글 없음')
                    break

                for item in li:
                    title = item.find('strong', 'ctit').text.strip()
                    # print(title)
                    title_null = titleNull(title)
                    check_num = item.find('a', 'ctitle')['onclick']
                    if check_num.find('page_open') != -1:
                        cnt_num = item.find('a', 'ctitle')['onclick'].split('page_open(')[1].split(',')[0].strip()
                        url = 'https://www.filemong.com/contents/info_ajax.php?bbs_idx='+cnt_num

                        # 키워드 체크
                        # keyCheck = checkTitle(title_null, getKey)
                        # if keyCheck['m'] == None:
                        #     dbResult = insertDB('filemong',title,title_null,url)
                        #     continue

                        cnt_price = item.find('div', 'pay').text.replace(",","").replace('P', '').strip()
                        cnt_writer = item.find('div', 'name').text.strip()
                        cnt_vol = item.find('div', 'byte').text.strip()

                        Data2 = {
                            'bbs_idx': cnt_num,
                            'moveicon': 'Y'
                        }

                        link = 'https://filemong.com/contents/info_ajax.php'
                        post_one  = s.post(link, headers=headers, data=Data2)
                        soup2 = bs(post_one.text, 'html.parser')
                        cnt_chk = 0

                        cnt_fname = soup2.find('tbody', id='flist_s').find('td').text.strip()
                        if soup2.find('table', 'v-info').find('span', 'badge0'):
                            jehu = soup2.find('table', 'v-info').find('span', 'badge0').text.strip()
                            if jehu == '제휴':
                                cnt_chk = 1

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'filemong',
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
                continue

if __name__=='__main__':
    start_time = time.time()

    print("filemong 크롤링 시작")
    # getKey = ['ORIGINALS','PERSON OF INTEREST','PRETTY LITTLE LIARS','SHAMELESS','MENTALIST','GILMORE GIRLS','CLOSER','COLD CASE','FRIENDS','FRINGE']
    getKey = ['FRIENDS','ORIGINALS','PERSON OF INTEREST','PRETTY LITTLE LIARS','SHAMELESS','MENTALIST','GILMORE GIRLS','CLOSER','COLD CASE','FRINGE']
    for key in getKey:
        startCrawling(key)
    print("filemong 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
