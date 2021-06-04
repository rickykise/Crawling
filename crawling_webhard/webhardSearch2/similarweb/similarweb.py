import requests,re
import pymysql,time,datetime
import urllib.parse
import os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'D_IID=133BC5E2-953A-3111-A85C-CAE4813DBAB9; sgID=39194ffd-59b5-4400-9f95-9e7483ceca36; visitor_id597341=338679422; loyal-user={%22date%22:%222019-04-02T00:33:51.890Z%22%2C%22isLoyal%22:true}; visitor_id597341-hash=21431e7e563035f439758cd460a369137fb9a9802eec69357f97c2f451cdca73d9bdcdfb362e773df986c15d6de404992943270b; D_ZID=AFF8EBD8-4296-379C-9BCE-B63F195D0220; D_SID=61.82.113.196:XprVPN1yQqY+/Z7knrcX2SSxtgTUwksgYW9EbmH/zqo; D_UID=EE18C99B-578F-3BAC-89A2-92117FD8FF7F; D_HID=60295E10-B7B6-3938-9C45-7796025B7A25; D_ZUID=D97297C8-C333-3DE5-9257-1569473DC6A7; .AspNetCore.Antiforgery.xd9Q-ZnrZJo=CfDJ8O3KJbQZozVFjBEXXPUInFKaIg-IIYa1cHwLAlRZ6GEh5nIvXQg6dNNfXRf3KEgXppz_cYElKTfAtrtI8UkRTXJruhOlOFsDkVCl1k-oM2-OIegFQ63lAF0t9QK0YusOXVXgS6YMHtlNiYU7nFLAz34; user_num=nowset; sc_is_visitor_unique=rx8617147.1554166805.DE348C5DD6D84FBBCFBACAD487F426AC.1.1.1.1.1.1.1.1.1; _vwo_uuid_v2=DC9065B1B9C420277558FF8FB2B7A3445|a0cca7b858ba9c8b582a3f5a599cf383; _vis_opt_s=2%7C; _gcl_au=1.1.1051355508.1554165232; _vwo_uuid=DC9065B1B9C420277558FF8FB2B7A3445; intercom-id-e74067abd037cecbecb0662854f02aee12139f95=3c4fc047-0c28-46b7-8053-32701d1c5ea5; _vwo_ds=3%3Aa_0%2Ct_0%3A0%241554165232%3A59.9169413%3A%3A%3A277_0; _gid=GA1.2.667180529.1554165232; _ga=GA1.2.735837927.1554165232; _fbp=fb.1.1554165232095.317230997; _pk_id.1.fd33=5624267b7a649823.1554165232.1.1554166805.1554165232.; _pk_ses.1.fd33=*; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%22169db776e7e5c9-0efa28145572368-51a2f73-2a3000-169db776e7f61d%22%2C%22%24device_id%22%3A%20%22169db776e7e5c9-0efa28145572368-51a2f73-2a3000-169db776e7f61d%22%2C%22sgId%22%3A%20%227cc762f9-7040-4ba0-935f-1f4e08f51969%22%2C%22Site%20Type%22%3A%20%22Lite%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22session%20ID%22%3A%20%229660f9a5-80c1-44f9-a09e-9ca3ebe301d9%22%2C%22section%22%3A%20%22website%22%2C%22last%20event%20time%22%3A%201554166804744%7D; _gat=1; _vis_opt_test_cookie=1; _gat_UA-42469261-1=1',
    'Host': 'www.similarweb.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(osp, url):
    i = 0;check = True
    with requests.Session() as s:
        link = "https://www.similarweb.com/website/" + url
        post_one  = s.get(link, headers=headers)
        soup = bs(post_one.text, 'html.parser')
        if soup.find('div', id='distilIdentificationBlock'):
            print('에러')
            time.sleep(15)
        else:
            osp_id = osp
            osp_g_rank = soup.find_all('div', 'websiteRanks-valueContainer js-websiteRanksValue')[0].text.replace(',', '').strip()
            osp_k_rank = soup.find_all('div', 'websiteRanks-valueContainer js-websiteRanksValue')[1].text.replace(',', '').strip()
            osp_v_str = soup.find('span', 'engagementInfo-valueNumber js-countValue').text.strip()
            total = osp_v_str.replace('K', '').replace('M', '')
            if osp_v_str.find('M') != -1:
                osp_v_total = int(float(total) * 10000)
            else:
                osp_v_total = int(float(total) * 1000)

            data = {
                'osp_id' : osp_id,
                'osp_g_rank' : osp_g_rank,
                'osp_k_rank': osp_k_rank,
                'osp_v_total': osp_v_total,
                'osp_v_str': osp_v_str
            }
            # print(data)

            conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='sms@unionc',db='otogreen',port=3306,charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                dbResult = insertInfo(conn,data['osp_id'],data['osp_g_rank'],data['osp_k_rank'],data['osp_v_total'],data['osp_v_str'])
                dbDelete(osp_id,conn,curs)
            except Exception as e:
                print(e)
                pass
            finally :
                conn.close()
            time.sleep(15)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl()
    print("similarweb 크롤링 시작")
    for o, u in getUrl.items():
        startCrawling(o, u[0])
    print("similarweb 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
