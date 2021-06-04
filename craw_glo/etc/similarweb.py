import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from similarwebFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'D_IID=848FC57A-DBB8-339B-AE10-CDC46AF882BD; visitor_id597341=431039842; visitor_id597341-hash=dcefb153ae2b869f42f472231e0e4da151a1ba727c7e9bb1b72446eab055797550c1f5f22878d79ad1ac5e71b7aba8a4e059f23c; _pk_id.1.8c7a=edf8a81e364f5dfd.1573627070.3.1573635836.1573635836.; D_ZID=760A0FF5-9835-325C-BADC-E77F5C199CC6; D_SID=61.82.113.196:XprVPN1yQqY+/Z7knrcX2SSxtgTUwksgYW9EbmH/zqo; D_UID=4742943C-F08B-3C77-B655-98C1A3784BE2; sw-data-rerun-popup-dismissed=1; D_HID=B872419C-7010-39BB-80B8-BFD3A6955321; D_ZUID=5F278462-F20E-3017-A827-2617934854ED; .AspNetCore.Antiforgery.xd9Q-ZnrZJo=CfDJ8LTRIxy8S0hBnwYCB_ha7SWADl1jxGRz30CDuw28x1H1-LY2IKd2c0IR21PznpKVUzxh4rnpeoZQmnXsVOgiC0dyJGXTGBeOabSeO77pfshG1-dq9HUM-_gwQ1tZ-I9AAN2sXXfBubFzd4V4BF2kDw4; loyal-user={%22date%22:%222019-11-13T05:56:26.703Z%22%2C%22isLoyal%22:true}; _pk_ses.1.8c7a=*; sc_is_visitor_unique=rx8617147.1573635875.BCBAD79FC7A34FDECB297238C752A048.4.2.2.2.2.2.2.2.2; sgID=c25cf6ec-252c-b08c-cc33-f2f9ac00bc13; _vwo_uuid_v2=D21C928FF75C4A0242E85C52FB8B0CE38|9f6b1d7491593adbf09a9bd3e97607b6; _gcl_au=1.1.40413100.1573624587; _hjid=353106c7-4404-4cc1-873d-f0cc80b5e320; _gat=1; intercom-id-e74067abd037cecbecb0662854f02aee12139f95=2bbbe9fc-cd0a-4f25-9192-cc9819851b6b; _gid=GA1.2.1510066645.1573624586; locale=en-us; _ga=GA1.2.1030011671.1573624586; _pk_id.1.fd33=2d68f4654d1cb9a8.1573624587.3.1573635875.1573635858.; _pk_ses.1.fd33=*; mp_7ccb86f5c2939026a4b5de83b5971ed9_mixpanel=%7B%22distinct_id%22%3A%20%2216e6355a1c1bb-0ddd9dc691ebc7-51a2f73-2a3000-16e6355a1c28d6%22%2C%22%24device_id%22%3A%20%2216e6355a1c1bb-0ddd9dc691ebc7-51a2f73-2a3000-16e6355a1c28d6%22%2C%22sgId%22%3A%20%22c25cf6ec-252c-b08c-cc33-f2f9ac00bc13%22%2C%22site_type%22%3A%20%22Lite%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fwebsite%2Ftvwang02.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.similarweb.com%22%2C%22session_id%22%3A%20%22b4c860ef-67f6-4c26-a44f-818976531b78%22%2C%22session_first_event_time%22%3A%20%222019-11-13T09%3A04%3A18.389Z%22%2C%22url%22%3A%20%22https%3A%2F%2Fwww.similarweb.com%2Fwebsite%2Fnaver.com%22%2C%22is_sw_user%22%3A%20false%2C%22language%22%3A%20%22en%22%2C%22section%22%3A%20%22website%22%2C%22entity_name%22%3A%20%22naver.com%22%2C%22entity_id%22%3A%20%22naver.com%22%2C%22page_number%22%3A%20%221%22%2C%22main_category%22%3A%20%22News_and_Media%22%2C%22sub_category%22%3A%20%22%22%2C%22first_time_visitor%22%3A%20false%2C%22last_event_time%22%3A%201573635875191%7D',
    'Host': 'www.similarweb.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

# 전달 데이터
def startCrawling(osp_url):
    i = 0;check = True;countNum = 0
    now = datetime.datetime.now().strftime('%Y-%m-'+'01')
    countNum = countNumget(now, osp_url)
    if countNum >= 1:
        pass
    url = osp_url.replace('https://', '').replace('http://', '').replace('www.', '')
    dot = url.count('.')
    if dot == 2:
        if dot == 2:
            if url.find('co.kr') == -1:
                url = url.split('.')[1]
    with requests.Session() as s:
        link = "https://www.similarweb.com/website/" + url
        post_one  = s.get(link, headers=headers)
        soup = bs(post_one.text, 'html.parser')
        if soup.find('div', id='distilIdentificationBlock'):
            s.close()
            print('에러')
            print('link: '+link)
            print("=================================")
            # time.sleep(2400)
        else:
            try:
                osp_g_rank = soup.find_all('div', 'websiteRanks-valueContainer js-websiteRanksValue')[0].text.replace(',', '').strip()
                if osp_g_rank == 'N/A':
                    pass
                osp_c_rank = soup.find_all('div', 'websiteRanks-valueContainer js-websiteRanksValue')[1].text.replace(',', '').strip()
                osp_nat = soup.find_all('div', 'websiteRanks-header')[1].find('div', 'websiteRanks-name').text.strip()
                osp_nat = change_Nat(osp_nat)

                try:
                    osp_v_str = soup.find('span', 'engagementInfo-valueNumber js-countValue').text.strip()
                    if osp_v_str.find('M') != -1:
                        total = float(osp_v_str.replace('M', ''))*1000000
                        osp_v_total = str(total).split('.')[0]
                    elif osp_v_str.find('K') != -1:
                        total = float(osp_v_str.replace('K', ''))*1000
                        osp_v_total = str(total).split('.')[0]
                    elif osp_v_str.find('B') != -1:
                        total = float(osp_v_str.replace('B', ''))*1000000000
                        osp_v_total = str(total).split('.')[0]

                    returnValue = []
                    traffic = soup.find('div', 'countries-list').find_all('div', 'accordion-group')
                    for item in traffic:
                        if item.find('a'):
                            country = item.find('a').text.strip()
                        else:
                            country = item.find('span', 'country-name').text.strip()
                        value = item.find('span', 'js-countValue').text.strip()
                        traffic_value = country+'_'+value
                        returnValue.append(traffic_value)
                    osp_traffic = ", ".join(returnValue)
                except:
                    osp_v_total = ''
                    osp_v_str = ''
                    osp_traffic = ''
                now = datetime.datetime.now().strftime('%Y-%m-%d')

                data = {
                    'osp_state': '1',
                    'osp_nat': osp_nat,
                    'osp_g_rank': osp_g_rank,
                    'osp_c_rank': osp_c_rank,
                    'osp_v_total': osp_v_total,
                    'osp_v_str': osp_v_str,
                    'osp_traffic': osp_traffic,
                    'osp_url': osp_url,
                    'osp_regdate': now
                }
                # update
                print(data)
                print("=================================")
                # dbUpResult = similarwebUpdate(data)

                osp_also = soup.find('section', 'alsoVisitedSection').find('div', 'websitePage-engagementInfo').find_all('div', 'websitePage-listUnderline')
                for item in osp_also:
                    osp_url = "https://"+item.find('a')['href'].split('website/')[1]
                    dot = osp_url.count('.')
                    if dot == 2:
                        if osp_url.find('co.kr') != -1:
                            osp_id = item.find('a')['href'].split('website/')[1].split('.')[0]
                        else:
                            osp_id = item.find('a')['href'].split('website/')[1].split('.')[1].split('.')[0]
                    else:
                        osp_id = item.find('a')['href'].split('website/')[1].split('.')[0]

                    data = {
                        'osp_id': osp_id,
                        'osp_url' : osp_url
                    }
                    # insert
                    print(data)
                    print("=================================")
                    s.close()
                    # dbInResult = similarwebInsert(data)

                # time.sleep(2400)
            except:
                # time.sleep(2400)
                s.close()
                pass

if __name__=='__main__':
    start_time = time.time()
    getUrl = getOspTR()

    print("similarweb 크롤링 시작")
    for u in getUrl:
        startCrawling(u)
    print("similarweb 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
