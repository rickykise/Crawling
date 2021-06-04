import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from youtube_fun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key, keyItem):
    print("키워드 : ",key)
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];a=1;updateNum = 0;insertNum = 0
    try:
        link = "https://www.youtube.com/results?search_query="+key+"&sp=CAM%253D"
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        driver.set_window_position(0, 0)
        driver.set_window_size(1210, 1050)
        time.sleep(3)
        while(True):
            height = driver.execute_script("return document.body.scrollHeight")
            a = a+1
            time.sleep(1)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            if a==10:
                break
        html = driver.find_element_by_id("contents").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        ytd = soup.find_all('ytd-video-renderer', 'ytd-item-section-renderer')

        for item in ytd:
            div = item.find("div", id="meta")
            if div.find('h3', id='video-title'):
                continue

            elif div.find('h3', 'title-and-badge'):
                video_time = item.find('span', 'ytd-thumbnail-overlay-time-status-renderer')['aria-label']
                title = div.find('h3', 'title-and-badge').text.strip()
                title = remove_emoji(title)
                title_null = titleNull(title)

                # 제목 체크
                googleCheck = googleCheckTitle(title_null, key, cnt_id)
                if googleCheck == None:
                    continue
                url = 'https://www.youtube.com'+div.find('h3', 'title-and-badge').find('a')['href']
                cnt_writer = div.find('div', id='container').find('a').text.strip()

                # cnt_writer 체크
                writerGet = getWriter()
                writerCheck = checkWriter(cnt_writer, writerGet)
                if writerCheck['m'] != None:
                    continue

                channel_link = 'https://www.youtube.com'+div.find('div', id='container').find('a')['href']
                divGet = div.find('div', id='metadata-line').text.strip()
                view_count = divGet.split('조회수')[1].split('회')[0].strip()
                write_date = divGet.split(view_count+'회')[1].strip()

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'youtube',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'unitedstates',
                    'cnt_writer': cnt_writer,
                    'origin_url': channel_link,
                    'origin_osp': view_count,
                    'site_p_img': video_time,
                    'site_r_img': write_date,
                    'cnt_keyword_nat': k_nat
                }
                # print(data)
                # print("=================================")

                dbResult = insertALLKey(data)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeywordYoutube()

    print("youtube_web 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("youtube_web 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
