# 페이스북 크롤링
import requests,re
import pymysql
import datetime,time
import pymysql
import os,sys
from datetime import date, timedelta
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from facebookFun import *

def startCrawling():
    content_check = '';pageKey = '롯데시네마';sns_subcontent = ''
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome("c:\python36\driver\chromedriver", options=chrome_options)
        driver.get('https://www.facebook.com/pg/LotteCinema.kr/posts/')
        time.sleep(3)
        for i in range(2):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            except:
                pass
        try:
            driver.find_element_by_xpath('//*[@id="expanding_cta_close_button"]').click()
        except:
            pass
        html = driver.find_elements_by_class_name("_1xnd")[0].get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        div =  soup.find_all("div", "_4-u2")

        for item in div:
            try:
                if item.find("div","_1dwg").find("div","_5pbx"):
                    sns_content = item.find("div","_1dwg").find("div","_5pbx").text.strip()
                    sns_content = remove_emoji(sns_content)
                    if content_check == sns_content:
                        continue
                    content_check = sns_content
                    urlEle = item.find("abbr").parent
                    abbr = urlEle.find('abbr')
                    url = (urlEle['href'].find('https://www.facebook.com') == -1) and 'https://www.facebook.com'+urlEle['href'] or urlEle['href']
                    if url.find('photos') != -1:
                        url = url.split('&__')[0]
                    else:
                        url = url.split('?__')[0]
                    writeDate = settingDate(abbr)
                    beforelast = str(date.today() - timedelta(days=6))
                    if writeDate < beforelast:
                        continue

                    if url.find('photos/a') != -1:
                        url = item.find('a', '_3hg-')['href']
                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")

                    if url.find('videos') != -1:
                        text = str(soup)
                        if text.find('조회') != -1:
                            view_cnt = text.split('class="_1vx9"><span>조회')[1].split('회')[0].replace(',', '').strip()
                        else:
                            view_cnt = 0
                        like_cnt = text.split(',reactors:{count:')[1].split('}')[0].replace(',', '').strip()
                        reply_cnt = text.split('comment_count:{total_count:')[1].split('}')[0].replace(',', '').strip()
                    else:
                        cnt_num = url.split('posts/')[1]
                        stext = str(soup)
                        text = stext.split('subscription_target_id:"'+cnt_num)[1]
                        view_cnt = 0
                        like_cnt = text.split('},reaction_count')[1].split('}')[0].split('count:')[1].replace(',', '').strip()
                        reply_cnt = text.split('comment_count:{total_count:')[1].split('}')[0].replace(',', '').strip()

                    if item.find('span', '_355t'):
                        share_cnt = item.find('span', '_355t').text.split('공유')[1].strip()
                        if share_cnt.find('.') != -1 and share_cnt.find('천') != -1:
                            share_cnt = share_cnt.split('천')[0].replace('.', '')+'00'
                        elif share_cnt.find('천') != -1:
                            share_cnt = share_cnt.split('천')[0]+'000'
                        elif share_cnt.find('.') != -1 and share_cnt.find('만') != -1:
                            share_cnt = share_cnt.split('만')[0].replace('.', '')+'000'
                        elif share_cnt.find('만') != -1:
                            share_cnt = share_cnt.split('만')[0]+'0000'
                        else:
                            share_cnt = share_cnt.split('회')[0]
                    else:
                        share_cnt = 0

                    data = {
                        'sns_content' : sns_content,
                        'sns_subcontent' : sns_subcontent,
                        'url' : url,
                        'like_cnt' : like_cnt,
                        'reply_cnt' : reply_cnt,
                        'share_cnt' : share_cnt,
                        'view_cnt' : view_cnt,
                        'writeDate' : writeDate
                    }
                    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    create1 = datetime.datetime.now().strftime('%Y-%m-%d %H:00:00')
                    create2 = datetime.datetime.now().strftime('%Y-%m-%d %H:59:59')
                    GetCreateDate = getCreateDate(url,create1,create2,conn,curs)
                    if GetCreateDate == False:
                        getView = getSearchView(url,conn,curs)
                        getLike = getSearchLike(url,conn,curs)
                        getReply = getSearchReply(url,conn,curs)

                        gview_cnt = int(view_cnt) - getView
                        glike_cnt = int(like_cnt) - getLike
                        greply_cnt = int(reply_cnt) - getReply
                        GetSubcontents = getSubcontents(url,conn,curs)

                        insert(conn,pageKey,sns_content,GetSubcontents,url,like_cnt,reply_cnt,share_cnt,view_cnt,writeDate)
                        insert2(pageKey,url,gview_cnt,glike_cnt,greply_cnt,writeDate)
            except:
                continue
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("롯데시네마 크롤링 시작")
    startCrawling()
    print("롯데시네마 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
