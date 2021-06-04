import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
import pymysql
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def imgCheck(cnt_id, url):
    result = cnt_id+'Check(url)'
    return eval(result)

def yesfileCheck(url):
    try:
        with requests.Session() as s:
            post_two  = s.get(url)
            content = post_two.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            cnt_chk = 0

            if soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[1].find('span'):
                cnt_price = soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[1].text.split('P')[0].replace(",","").strip()
                cnt_chk = 1
            else:
                cnt_price = soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[1].text.split('P')[0].replace(",","").strip()

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def wediskCheck(url):
    try:
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        with requests.Session() as s:
            post_two  = s.post(url, headers=headers)
            content = post_two.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)
            cnt_chk = 0

            if soup.find('div', id='contents_ttl'):
                cnt_price = soup.find('div', id='contents_ttl').find_all('p')[1].text.split('/')[1].split('캐시')[0].replace(",","").strip()
                if text.find('icon_partnership') != -1:
                    cnt_chk = 1
            else:
                cnt_chk = 2

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def tpleCheck(url):
    try:
        with requests.Session() as s:
            cnt_num = url.split('idx=')[1]
            url2 = 'http://www.tple.co.kr/storage/index.php?todo=view&source=W&idx='+cnt_num
            post_one  = s.get(url2)
            soup = bs(post_one.text, 'html.parser')
            cnt_chk = 0

            if soup.find('table', 'divNoticeTable'):
                cnt_chk = 2
            else:
                if soup.find('div', 'noticeArea'):
                    text = soup.find('div', 'noticeArea').text.strip()
                    if text.find('제휴업체') != -1:
                        cnt_chk = 1

            Page = {
                'idx': cnt_num,
                'source': 'W',
                'todo': 'viewFile'
            }
            url3 = 'http://www.tple.co.kr/storage/index.php'
            post_two  = s.post(url3, data=Page)
            soup2 = bs(post_two.text, 'html.parser')

            cnt_price = soup2.find('td', 'textRight').text.strip().split("P")[0].replace(",","")

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def todiskCheck(url):
    try:
        headers = {
            'Origin': 'http://m.todisk.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': 'appLogin=false; PHPSESSID=4513ea4563f87af45d1c741c755bb76a; log100=20190122; _ga=GA1.2.1070817977.1548124083; _gid=GA1.2.1882185260.1548124083; think_result=0; shacipher=Y; is_ctrl=Y; m_grade=1; mid=AvW14mtZM1qL1fJ2GITOhXQIdHDBrOCK2ZrmYSdgK2IKuZfVzCFenSbMnejn7xoCEB4DHWrPRmlFJLgNW1yQ1xMDSIffZSWpPXCkipajc3QUFkXX36T0TvaKcWc519lM; nick=up0001; Usr=up0001; total_cash=0; cmn_cash=0; bns_cash=0; coupon=0; memo_cnt=0; LogChk=Y; _not100=Y; cidprt=Y; logtime=1548124086; logip=1028813252; vr=1'
        }
        with requests.Session() as s:
            cnt_num = url.split('idx=')[1].split('&')[0]
            baseCnt = url.split('eidx=')[1]
            url2 = 'http://www.todisk.com/_main/popup.php?doc=bbsInfo&idx='+cnt_num+'&eidx='+baseCnt
            post_two  = s.post(url2, headers=headers)
            soup = bs(post_two.text, 'html.parser')
            table = soup.find_all('table', 'table2')[1]
            cnt_chk = 0

            cnt_price = table.find('td').text.strip().replace(" ", "").replace(",", "").split("P")[0]
            if table.find('td').find('img'):
                cnt_chk = 1

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def smartfileCheck(url):
    try:
        LOGIN_INFO = {
            'email_tail': 'naver.com',
            'id': 'enjoy11@naver.com',
            'id_nm': 'enjoy11',
            'login_backurl': '',
            'mode': 'login_exec',
            'pw': 'enjoy11',
            'saved_pw': 'Y',
            'ssl_mobile_flg': '0',
            'wmode': 'noheader'
        }

        headers = {
            'Origin': 'http://m.smartfile.co.kr',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        with requests.Session() as s:
            login_req = s.post('http://m.smartfile.co.kr/member/login.html', data=LOGIN_INFO, headers=headers)
            cnt_num = url.split('idx=')[1]
            url2 = 'http://m.smartfile.co.kr/ajax/ajax.left.php'
            Page = {
                'idx': cnt_num
            }
            post_two  = s.post(url2, headers=headers, data=Page)
            content = post_two.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            cnt_chk = 0

            cnt_price = soup.find('div', 'info').find_all('p')[1].find('span').text.split("P")[0].replace(",","").strip()
            if soup.find('div', 'info').find('p').find('font'):
                cnt_chk = 1

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def shareboxCheck(url):
    try:
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://m.sharebox.co.kr',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        with requests.Session() as s:
            post_two = s.get(url, headers=headers)
            content = post_two.content
            soup = bs(content.decode('utf-8','replace'), 'html.parser')
            cnt_chk = 0

            cnt_price = soup.find('div', 'viewn_won').text.replace(",","").split('P')[0].strip()
            jehu = soup.find('li', 'btn_playinfoL').text.strip()
            if jehu == '제휴':
                cnt_chk = 1

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def sediskCheck(url):
    try:
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Referer': 'http://sedisk.com/storage.php',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'ACEFCID=UID-5C22F965D514161EE9381054; _ga=GA1.2.1287727625.1545974475; ptn=ksc0110; ACEUCI=1; _gid=GA1.2.1421021257.1547447786; evLayer=N; _gat=1'
        }
        with requests.Session() as s:
            cnt_num = url.split('idx=')[1].split('&')[0]
            url2 = 'http://sedisk.com/storage.php?act=view&idx=' + cnt_num
            post_two  = s.post(url2, headers=headers)
            soup = bs(post_two.text, 'html.parser')
            cnt_chk = 0

            cnt_price = soup.find('span', 'b_price').text.strip().split("P")[0].replace(",","")
            if soup.find_all('td', 'point_vol')[2].find('img'):
                img = soup.find_all('td', 'point_vol')[2].find('img')['src']
                if img.find('ico_jehu2') != -1:
                    cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

# 모바일url없음
def qdownCheck(url):
    try:
        with requests.Session() as s:
            post_two  = s.get(url)
            c = post_two.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)
            cnt_chk = 0

            cnt_price = soup.find('td', 'infotable_td2').text.replace(" ","").replace(",","").split("P")[0].strip()
            if soup.find('td', 'infotable_td2').find('img'):
                jehu = soup.find('td', 'infotable_td2').find('img')['title']
                if jehu == '제휴':
                    cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def pdpopCheck(url):
    if url.find('m.pdpop') != -1:
        try:
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cache-Control': 'no-cache',
                'Connection': 'Keep-Alive',
                'Content-Length': '88',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'pdpopnet=0; connect_log=Y; _ga=GA1.2.1597594914.1553564520; _gid=GA1.2.1381734089.1553564520; _gat=1; cookie_id=up0001; age=45; auth=1; adult=1; uid=24412936; id=up0001%40pdpop.com; name=%EC%84%9C%EB%AF%BC%EC%8A%B9; clubsex=2; nickname=up0001; ero_birth=751031; ero_sex=2; domain=pdpop.com; PDPOP=LGbkAwc7pmb0BvWxLKEyVwgmBwL6VeaZipKQhlV7pmbmBvW1nJDvB3Z6BQbvZwD0ZGV5ZmLvB3Z6ZwbvnJDvB3Z6ZGL6VaIjZQNjZHOjMUOipP5wo20vB3Z6AwbvpTSmp3qxVwgmBwL0BvWyLmpmZQLkLwywZwt1ZQR1ZGZ5MzL3AQDmZGV0A2L4BTD1ZTSvZTEuAQyvZQp4AmDlZGHjBGZkBJR5AwIxAmuwVwgmBwD6Vz5uoJHvB3Z6BGbv7VFp66%2B87Vd5VwgmBwt6Vz5cL2ghLJ1yVwgmBwL6VaIjZQNjZFV7pmb1BvWfMKMyoPV7pmbkBvV5VwgmBwL6VzufMKMyoPV7pmblBvVjZFV7pmb1BvWvnKW0nPV7pmbkZQbvZGx3AF0kZP0mZFV7pmbmBvWuM2HvB2x6AQH7pmb1BvWuMUIfqPV7nGbkB3Z6AQbvLKI0nPV7nGbkB3Z6Zmbvp2I4VwgcBwV7pmb1BvWyoJScoPV7pmblZGbvpKqypwRlZmENpKqypwRlZmDhL29gVwgmBwL6VzEioJScovV7pmb5BvWjMUOipP5wo20vB3Z6ZGZ6VaOlo2McoTIsnJ1uM2HvB047sD%3D%3D; PHPSESSID=auuho4fi50um40trrf8h7equ60; changepay_notice=Y',
                'Host': 'm.pdpop.com',
                'Referer': 'http://m.pdpop.com',
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
                'X-Requested-With': 'XMLHttpRequest'
            }
            with requests.Session() as s:
                cnt_num = url.split('idx=')[1].split('&')[0]
                Data = {
                    'doc': 'board_view',
                    'idx': cnt_num,
                    'mPage': '1'
                }
                post_two  = s.get(url, headers=headers, data=Data)
                soup = bs(post_two.text, 'html.parser')
                text = str(soup)
                div = soup.find('div', 'list').find_all('input')
                cnt_chk = 0;cnt_price = 0;returnValue = []

                if text.find('본 자료에는 제휴 컨텐츠') != -1:
                    cnt_chk = 1
                for item in div:
                    if cnt_chk == 1:
                        cnt_price = int(item['packet'])
                    else:
                        cnt_price = int(item['packet1'])
                    returnValue.append(cnt_price)
                for i in range(len(div)-1):
                    cnt_price = returnValue[i]+cnt_price

        except:
            cnt_price = 0
            cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def ondiskCheck(url):
    try:
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Referer': 'http://m.ondisk.co.kr',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        with requests.Session() as s:
            cnt_num = url.split('idx=')[1]
            url2 = 'http://m.ondisk.co.kr/api/content/view.php?idx='+cnt_num
            post_two  = s.post(url2, headers=headers)
            content = post_two.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            textJ = str(soup)
            jsonString = json.loads(textJ)
            textJson = str(jsonString)
            cnt_chk = 0

            cnt_price = textJson.split("'sale_point': '")[1].split("',")[0].replace(",","")
            jehu = textJson.split("'is_rights': '")[1].split("',")[0]
            if jehu == 'Y':
                cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def megafileCheck(url):
    try:
        LOGIN_INFO = {
            'login_backurl': '',
            'loginid': 'up0001',
            'passwd': 'up0001',
            'site': 'megafile.co.kr',
            'type': '',
            'url': 'http://m.megafile.co.kr/'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        with requests.Session() as s:
            login_req = s.post('http://m.megafile.co.kr/user/login_process.php', data=LOGIN_INFO)

            post_two = s.get(url, headers=headers)
            c = post_two.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            div = soup.find('div', id='fileinfo_text')
            cnt_chk = 0

            cnt_price = div.find_all('div')[1].text.strip().split('캐시')[1].replace(",","")
            if soup.find('div', 'filetitle').find('img'):
                jehu = soup.find('div', 'filetitle').find('img')['src']
                if jehu.find('icon_copyright2') != -1:
                    cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def me2diskCheck(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
        }
        with requests.Session() as s:
            post_two  = s.get(url, headers=headers)
            soup = bs(post_two.text, 'html.parser')
            div = soup.find('div', 'vimgbx2')
            cnt_chk = 0

            cnt_price = div.find_all('span', 'mar_left10')[1].text.replace(",","").split("P")[0].strip()
            if div.find_all('span', 'mar_left10')[1].find('img'):
                jehu = div.find_all('span', 'mar_left10')[1].find('img')['src']
                if jehu.find('affily') != -1:
                    cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def kdiskCheck(url):
    try:
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://m.kdisk.co.kr',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Referer': 'http://m.kdisk.co.kr/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'PCID=15475363414190116198676; _ga=GA1.3.2038327300.1547536342; blind_advisory=1; keep_query_string=%2Findex.php; _co_t=1548906834; _gid=GA1.3.91246515.1548906850; app_version=0; pageCookie-sub_cate=; pageCookie-search=; pageCookie-sort=; js_evtBnnrNewYear_20190131=true; layerListGuide=true; adult_not=y; pageCookie-adult_not=y; is_rights=y; pageCookie-is_rights=y; id_save=up0001; auto_login=D8GwPTvB2r%2BxyX70F3aYIGSdrKoUaVZyj1QHWaAFaww%3D; mid=0a191a191a191a19h619c619; nick=up0001; cmn_cash=0; bns_cash=0; coupon=0; login_last=1548914611; Lidx=%241%24juuefmpQ%24scUv8XmFxAyQOuZxwUvdq0; charge=no; pageCookie-page_type=; Intro_domain_chk=m.kdisk.co.kr; gnbRolling-posX=0; pageCookie-page=; pageCookie-search_type=; RefUrl=%2F%3Fcate%3DALL%26is_rights%3Dy%26adult_not%3Dy%26idx%3D11825110; pageCookie-cate=ALL; pageCookie-idx=11825110'
        }
        with requests.Session() as s:
            cnt_num = url.split('idx=')[1]
            url2 = 'http://m.kdisk.co.kr/api/content/view.php?idx='+cnt_num
            post_two  = s.post(url2, headers=headers)
            c = post_two.content
            soup2 = bs(c.decode('euc-kr','replace'), 'html.parser')
            text = str(json.loads(str(soup2)))
            cnt_chk = 0

            cnt_price = text.split("point': '")[1].split("', '")[0].replace(",","").strip()
            jehu = text.split("is_rights': '")[1].split("', '")[0].strip()
            if jehu == 'Y':
                cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def gdiskCheck(url):
    try:
        with requests.Session() as s:
            cnt_num = url.split('idx=')[1].split('&category')[0]
            url2 = 'http://g-disk.co.kr/contents/view_top.html?idx='+cnt_num
            r = requests.get(url2)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)
            cnt_chk = 0

            table = soup.find_all('table', cellpadding='0')[10]
            cnt_price = table.find_all('span')[2].text.strip().replace(",","").strip().split('P')[0]
            if text.find('판매자') != -1:
                if text.find('저작권자와의 제휴를') != -1:
                    cnt_chk = 1
            else:
                cnt_chk = 2
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filetourCheck(url):
    try:
        cnt_num = url.split('contents/')[1]
        url2 = 'http://www.filetour.com/front/contents/'+cnt_num
        r = requests.get(url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        table = soup.find('table', 'show_table')
        cnt_chk = 0

        cnt_price = soup.find('span', 'red-txt bold-txt').text.replace(" ","").replace(",","").strip().split('P')[0]
        if table.find('span', 'b_blue_btn disp_ibl'):
            jehu = table.find('span', 'b_blue_btn disp_ibl').text.strip()
            if jehu == '제휴':
                cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filenoriCheck(url):
    try:
        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Connection': 'Keep-Alive',
            'Cookie': 'JSESSIONID=037D42999513B9AFF91DB9E57C331A9B; mEventDesignVer=1060',
            'Host': 'm.filenori.com',
            'Referer': 'http://m.filenori.com/Mobile/home.do',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        with requests.Session() as s:
            post_two  = s.get(url, headers=headers)
            content = post_two.content
            soup = bs(content.decode('utf-8','replace'), 'html.parser')
            text = str(soup)
            cnt_chk = 0

            cnt_price = soup.find('span', id='contentsPrice').text.split('캐시')[0].replace(',', '').strip()
            if soup.find('span', 'pshipIcon'):
                jehu = soup.find('span', 'pshipIcon').text.strip()
                if jehu == '제휴':
                    cnt_chk = 1
            if text.find('존재하지 않는 컨텐츠') != -1:
                cnt_chk = 2
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filemanCheck(url):
    try:
        with requests.Session() as s:
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Cookie': 'PHPSESSID=vdp7ctdanms3iqh6u5h7ngckf5; 07099283cfc31f2d473bf5b4628ab3a6=dXAwMDAx',
                'Host': 'm.fileman.co.kr',
                'Referer': 'http://m.fileman.co.kr/',
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
            }

            headers2 = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Cookie': 'PHPSESSID=cc7prkncvotlnfidibd3cbcfd5; 07099283cfc31f2d473bf5b4628ab3a6=dXAwMDAx',
                'Host': 'fileman.co.kr',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            LOGIN_INFO = {
                'Frame_login': 'Ok',
                'idSave': '0',
                'm_id': 'up0001',
                'm_pwd': 'up0001',
                'x': '37',
                'y': '29'
            }
            with requests.Session() as s:
                login_req = s.post('https://fileman.co.kr/member/loginCheck.php', data=LOGIN_INFO)
                post_one  = s.get(url, headers=headers)
                content = post_one.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                li = soup.find('li', 'Choice_Contents_Simple_Text').text.strip()
                cnt_price = li.split("포인트")[1].split("P")[0].strip().replace(",","")

                cnt_num = url.split('idx=')[1]
                url2 = 'http://fileman.co.kr/contents/view_top.html?idx='+cnt_num+'&amp;page='
                post_two  = s.get(url2, headers=headers2)
                content = post_two.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                text = str(soup)
                cnt_chk = 0

                if soup.find('span', 'main_title'):
                    if text.find('저작권자와의 제휴') != -1:
                        cnt_chk = 1
                else:
                    cnt_chk = 2
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filelonCheck(url):
    try:
        pcHeaders = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://www.filelon.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        with requests.Session() as s:
            Data = {
                'act': 'get_token'
            }
            token_req = s.post('http://www.filelon.com/ajax_controller.php', data=Data, headers=pcHeaders)
            soup = bs(token_req.text, 'html.parser')
            token = str(soup).split('"result":"')[1].split('","')[0]

            LOGIN_INFO = {
                'browser': 'pc',
                'isSSL': 'Y',
                'mb_id': 'up0001',
                'mb_pw': 'up0001',
                'repage': 'reload',
                'token': token,
                'url': '/main/module/loginClass.php',
                'url_ssl': 'https://ssl.filelon.com/loginClass.php'
            }
            login_req = s.post('https://ssl.filelon.com/loginClass.php', data=LOGIN_INFO, headers=pcHeaders)

            cnt_num = url.split('idx=')[1]
            url2 = 'http://www.filelon.com/main/popup.php?doc=bbsInfo&idx='+cnt_num

            post_two  = s.get(url2, headers=pcHeaders)
            soup2 = bs(post_two.text, 'html.parser')
            table = soup2.find_all('table', 'pop_base')[1]
            cnt_chk = 0

            cnt_price = table.find('td', 'txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("/")[1].split("P")[0]
            if table.find('span', 'price_arrow'):
                cnt_price = soup2.find_all('b', class_=None)[2].text.strip().replace(",", "").split("P")[0]
            if table.find('td', 'txt').find('span', 'ic_alliance'):
                jehu = table.find('td', 'txt').find('span', 'ic_alliance').text.strip()
                if jehu == '제휴':
                    cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filekukiCheck(url):
    try:
        LOGIN_INFO = {
            'passwd': 'up0001',
            'useridorig': 'up0001'
        }
        cookies = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}
        with requests.Session() as s:
            login_req = s.post('https://www.filekuki.com/db/db_login.jsp', data=LOGIN_INFO, cookies=cookies)
            cnt_num = url.split('id=')[1]
            url2 = 'http://www.filekuki.com/popup/kukicontview.jsp?id=' + cnt_num
            post_one  = s.get(url2, cookies=cookies)
            soup = bs(post_one.text, 'html.parser')

            table = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
            cnt_price = table.split("쿠키")[0].replace(",","").strip()
            if soup.find('img', alt='특별할인'):
                priceCh = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
                cnt_price = priceCh.split("→")[1].split("쿠키")[0].strip()

            if soup.find('th', scope='col'):
                cnt_chk = 0
                if soup.find('p', 'ico_coop'):
                    if soup.find('p', 'ico_coop').find('img', alt='제휴'):
                        cnt_chk = 1
            else:
                cnt_chk = 2
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filekokCheck(url):
    try:
        Page = {
            'act': 'get_token'
        }
        Cookie = {
            'check_cookie_skidSafeFlag': 'Y'
        }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://www.filekok.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        token = ''
        with requests.Session() as s:
            login_req = s.post('http://m.filekok.com/ajax_controller.php', data=Page, headers=headers)
            soup = bs(login_req.text, 'html.parser')
            text = str(soup)
            token = text.split('"result":"')[1].split('","')[0]

        LOGIN_INFO = {
            'browser': 'm',
            'isSSL': 'Y',
            'mb_id': 'up0001',
            'mb_pw': 'up0001',
            'repage': 'reload',
            'token': token,
            'url': '/main/module/loginClass.php',
            'url_ssl': 'https://ssl.filekok.com/loginClass.php'
        }
        with requests.Session() as s:
            login_req = s.post('https://ssl.filekok.com/loginClass.php', data=LOGIN_INFO, headers=headers)
            cnt_num = url.split('idx=')[1].split('&mSec')[0]
            url2 = "http://www.filekok.com/main/popup.php?doc=bbsInfo&idx="+cnt_num
            post_two  = s.post(url2, headers=headers)
            soup = bs(post_two.text, 'html.parser')
            cnt_chk = 0

            cnt_price = soup.find_all('td', 'txt')[4].text.replace("\n","").replace("\t","").replace(" ","").replace(",","").strip().split(" / ")[1].split("P")[0]
            if soup.find_all('td', 'txt')[4].find('img'):
                jehu = soup.find_all('td', 'txt')[4].find('img')['alt']
                if jehu == '제휴컨텐츠':
                    cnt_chk= 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filejoCheck(url):
    try:
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        with requests.Session() as s:
            post_two  = s.post(url, headers=headers)
            content = post_two.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            div = soup.find('div', 'datatext')
            cnt_chk = 0

            label = div.find('ul').find_all('li')[2].find('label').text.strip()
            if div.find('ul').find_all('li')[2].find('strike'):
                cnt_price = div.find('ul').find_all('li')[2].find('font').text.strip().replace(",","").split('P')[0]
            else:
                cnt_price = div.find('ul').find_all('li')[2].text.split(label)[1].strip().replace(",","").split('P')[0]
            if div.find('ul').find_all('li')[2].find('img'):
                img = div.find('ul').find_all('li')[2].find_all('img')
                if len(img) == 1:
                    jehu = div.find('ul').find_all('li')[2].find('img')['src']
                    if jehu.find('icon_affily') != -1:
                        cnt_chk = 1
                elif len(img) == 2:
                    jehu1 = div.find('ul').find_all('li')[2].find_all('img')[0]['src']
                    jehu2 = div.find('ul').find_all('li')[2].find_all('img')[1]['src']
                    if jehu1.find('icon_affily') != -1 or jehu2.find('icon_affily') != -1:
                        cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def fileisCheck(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
        }
        with requests.Session() as s:
            post_one  = s.get(url, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            div = soup.find('div', 'vimgbx2')
            cnt_chk = 0

            cnt_price = div.find_all('span', 'mar_left10')[1].text.replace(",","").split("P")[0].strip()
            if div.find('img', 'mar_left5'):
                img = div.find('img', 'mar_left5')['src']
                if img.find('icon_rp') != -1:
                    cnt_price = div.find('span', 'mar_left5').text.replace(",","").split("P")[0].strip()
                if img.find('icon_affily') != -1:
                    cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filehonCheck(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
        }
        with requests.Session() as s:
            post_one  = s.get(url, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            cnt_chk = 0

            cnt_price = soup.find('p', 'movie_price').text.split("가격")[1].split("P")[0].replace(",","").strip()
            if soup.find('i', 'icon_alliance'):
                jehu = soup.find('i', 'icon_alliance').text.strip()
                if jehu == '제휴':
                    cnt_chk = 1
            if text.find('삭제된 자료') != -1:
                cnt_chk = 2
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filehamCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        cnt_chk = 0

        cnt_price = soup.find('span', 'mar_left5').text.strip().split('P')[0].replace(",","")
        if soup.find('span', 'vp_img_evt'):
            jehu = soup.find('span', 'vp_img_evt').text.strip()
            if jehu == '제휴':
                cnt_chk = 1
        if text.find('삭제된 게시물') != -1:
            cnt_chk = 2
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def fileguriCheck(url):
    try:
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        with requests.Session() as s:
            post_one  = s.get(url, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            cnt_price = soup.find('dd', id='dc_point').text.strip().split('P')[0].replace(",","")

            result = getTitle(url)
            title = result[0][0]
            writer = result[0][1]
            url2 = 'http://m.fileguri.com/index.php?mode=content&cate=&search='+title
            post_two  = s.get(url2, headers=headers)
            soup = bs(post_two.text, 'html.parser')
            cnt_chk = 0

            div = soup.find('div', 'cont_txtlist')
            if div.find('li', 'nodata'):
                cnt_chk = 2
            else:
                li = div.find('ul').find_all('li')
                for item in li:
                    cnt_writer = item.find_all('span', 'greyfont')[1].text.strip()
                    if cnt_writer == writer:
                        if item.find('span', 'bullet icon_img'):
                            cnt_chk = 1
                    else:
                        continue
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filecityCheck(url):
    try:
        with requests.Session() as s:
            cnt_num = url.split('idx=')[1]
            idx = {
                'idx': cnt_num,
                'link': 'list',
                'type': 'layer'
            }
            url2 = "https://filecity.kr/html/view2.html"
            post_two  = s.post(url2, data=idx)
            soup = bs(post_two.text, 'html.parser')
            cnt_chk = 0

            cnt_price = soup.find('li', 'point02').find('span', 'num').text.strip().replace(",","")
            if soup.find('ul', 'clearfix icon_alliance') or soup.find('ul', 'clearfix icon_alliance '):
                cnt_chk =1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filecastCheck(url):
    try:
        cnt_num = url.split('data=')[1]
        url2 = 'http://filecast.co.kr/www/contents/view/'+cnt_num
        r = requests.get(url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('span', 'txt_blue txt_block').find('b').text.replace(",","").strip()
        ico = soup.find('span', 'ico_partner')['class']
        if ico[1] == 'on':
            cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def bondiskCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'fileinfo_textarea')
        cnt_chk = 0

        price = div.find_all('li', 'info_a')[1].text.strip()
        if price.find('제휴') != -1:
            cnt_chk = 1
        cnt_price = price.split('P')[0].replace(",","")
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def bigfileCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        if soup.find('div', 'tit_view').find('span', 'bt_cp'):
            cnt_chk = 1
        cnt_price = soup.find('ul', 'file_summary').find_all('li')[2].find('strong').text.replace(" ","").split('캐시')[0].strip()
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def applefileCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'fileinfo_textarea')
        cnt_chk = 0

        price = div.find_all('li', 'info_a')[1].text.strip()
        if price.find('제휴') != -1:
            cnt_chk = 1
        cnt_price = price.split('P')[0].replace(",","")
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

# 타이틀 가져오는 함수
conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)
def getTitle(url):
    with conn.cursor() as curs:
        sql = "SELECT cnt_title, cnt_writer FROM cnt_mobile where cnt_url = %s;"
        curs.execute(sql,(url))
        result = curs.fetchall()

        returnValue = []
        for i in range(len(result)):
            result = result[i]
            returnValue.append(result)
        # print(returnValue)

        return returnValue

# def main():
#     cnt_id = 'fileguri'
#     url = 'http://m.fileguri.com/index.php?mode=cont_detail&idx=9622298&curr_page=3&isDetail=y&cate=MVO&adult_not=y'
#     data = imgCheck(cnt_id,url)
#     print(cnt_id)
#     print(data)
#
# if __name__=='__main__':
#     start_time = time.time()
#
#     main()
#     print("--- %s seconds ---" %(time.time() - start_time))
#     print("=================================")
