import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def imgCheck(cnt_id, url):
    data = {
        'Cnt_price': 0,
        'Cnt_chk': 0
    }
    try:
        result = cnt_id+'Check(url)'
        return eval(result)
    except Exception as e:
        return data

def yesfileCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('div', 'td_point').find('li', 'text').text.replace(" ","").replace(",","").strip().split("P")[0]
        if soup.find('div', 'td_point').find('img'):
            img = soup.find('div', 'td_point').find('img')['title']
            if img.find('제휴') != -1:
                cnt_chk = 1

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
        LOGIN_INFO = {
            'userid': 'up0001',
            'userpw': 'up0001',
            'backupr': 'Lw==',
            'todo': 'login_exec'
        }
        with requests.Session() as s:
            login_req = s.post('https://www.tple.co.kr/login/', data=LOGIN_INFO)
            cnt_chk = 0

            cnt_num = url.split("idx=")[1]
            Page = {
                'idx': cnt_num,
                'source': 'W',
                'todo': 'viewFile'
            }
            url2 = 'http://www.tple.co.kr/storage/index.php'
            post_two  = s.post(url2, data=Page)
            tags2 = bs(post_two.text, 'html.parser')
            if tags2.find('td', 'textLeft').find('img'):
                cnt_chk = 1

            returnValue = []

            td = tags2.find_all('td', 'textRight')
            for item in td:
                price = item.text.strip()
                if price.find('P') != -1:
                    cnt_price = int(price.split("P")[0].replace(",",""))
                    returnValue.append(cnt_price)
            for i in range(int(int(len(td)) / 2)-1):
                cnt_price = returnValue[i]+cnt_price

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
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': 'appLogin=false; PHPSESSID=4513ea4563f87af45d1c741c755bb76a; log100=20190122; _ga=GA1.2.1070817977.1548124083; _gid=GA1.2.1882185260.1548124083; think_result=0; shacipher=Y; is_ctrl=Y; m_grade=1; mid=AvW14mtZM1qL1fJ2GITOhXQIdHDBrOCK2ZrmYSdgK2IKuZfVzCFenSbMnejn7xoCEB4DHWrPRmlFJLgNW1yQ1xMDSIffZSWpPXCkipajc3QUFkXX36T0TvaKcWc519lM; nick=up0001; Usr=up0001; total_cash=0; cmn_cash=0; bns_cash=0; coupon=0; memo_cnt=0; LogChk=Y; _not100=Y; cidprt=Y; logtime=1548124086; logip=1028813252; vr=1'
        }
        with requests.Session() as s:
            post_two  = s.post(url, headers=headers)
            soup = bs(post_two.text, 'html.parser')
            table = soup.find('table', 'table2')
            cnt_chk = 0

            cnt_price = table.find('td').text.replace(" ", "").replace(",", "").replace('→','').split("P")[0].strip()
            if cnt_price.find('→') != -1:
                cnt_price = cnt_price.split('→')[1].strip()
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
        with requests.Session() as s:
            LOGIN_INFO = {
                'Frame_login': 'Ok',
                'keep': 'Y',
                'm_id': 'ZOhYtq6KHTEXRwEs0tjSlWGGUzDJPNvcW/oMxnK83L0=||lsuyIuZ76b7f0ac762978a0ae3a6a3976ebc186',
                'm_pwd': 'r5t/n0w7k7K8HvtGE49ASQ==||UXTFpJW3fed63a92591a5c75de52e4634c1ee21',
                'view_login': 'N'
            }
            login_req = s.post('https://ssl.smartfile.co.kr/member/loginCheck.php', data=LOGIN_INFO)
            headers2 = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Host': 'smartfile.co.kr',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            r = s.get(url, headers=headers2)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            table = soup.find('table', summary='컨텐츠정보표').find('tbody')
            cnt_chk = 0

            cnt_price = table.find_all('td')[2].find('span').text.strip().split("P")[0].replace(",","")
            if table.find_all('td')[2].find('img'):
                jehu = table.find_all('td')[2].find('img')['title']
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

def shareboxCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        table = soup.find('table', 'view_tb')
        cnt_chk = 0

        cnt_price = table.find_all('td')[1].text.strip().split("P")[0].replace(",","")
        if soup.find('div', 'view_bx').find('div', 'tit').find('li', 'tit_le2'):
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
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
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

def qdownCheck(url):
    try:
        with requests.Session() as s:
            post_two  = s.get(url)
            c = post_two.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
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
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        cnt_chk = 0;cnt_price = 0;returnValue = []

        ul = str(soup.find('ul', 'dnld_lstcon'))
        li = soup.find('ul', 'dnld_lstcon').find_all('li')

        for item in li:
            if item.find('span', 'packet'):
                cnt_price = int(item.find('span', 'packet').text.strip().replace(',', '').split("P")[0])
            returnValue.append(cnt_price)
        for i in range(len(li)-1):
            cnt_price = returnValue[i]+cnt_price

        if soup.find('div', 'dnld_lstbtn').find('span', 'cine'):
            span = soup.find('div', 'dnld_lstbtn').find('span', 'cine').text.strip()
            if span.find('제휴콘텐츠') != -1:
                cnt_chk = 1

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
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().replace(",","")
        if soup.find('div', 'ctvTitle').find('h2').find('img'):
            img = soup.find('div', 'ctvTitle').find('h2').find('img')['src']
            if img.find('icon_partnership') != -1:
                cnt_chk = 1

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def mfileCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('span', id='chkPacket').text.replace(",","").strip()
        if soup.find('td', 'td_tit').find('img'):
            aaa = soup.find('td', 'td_tit').find('img')['src']
            if aaa.find('icon_alli') != -1:
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
        with requests.Session() as s:
            post_two  = s.get(url)
            soup = bs(post_two.text, 'html.parser')
            view = soup.find('table', 'view_tb')
            cnt_chk = 0

            cnt_price = view.find_all('td')[1].text.strip().replace(",","").split("P")[0]
            if soup.find('li', 'tit_le2'):
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
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().split("P")[0].replace(",","")
        if soup.find('p', 'careMsg'):
            cnt_chkCh = soup.find('p', 'careMsg').text.strip()
            if cnt_chkCh.find('제휴') != -1:
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
            LOGIN_INFO = {
                'Frame_login': 'Ok',
                'idSave': '0',
                'm_id': 'up0001',
                'm_pwd': 'up0001',
                'm_pwd_load': '',
                'm_pwd_pass': '',
                'x': '27',
                'y': '29'
            }
            login_req = s.post('https://g-disk.co.kr/member/loginCheck2.php', data=LOGIN_INFO)
            cnt_num = url.split("idx=")[1]
            url2 = 'http://g-disk.co.kr/contents/view_top.html?idx='+cnt_num
            r = requests.get(url2)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            table = soup.find_all('table', cellpadding='0')[10]
            text = str(soup)
            cnt_chk = 0

            cnt_price = table.find_all('span')[2].text.strip().replace(" ","").replace(",","").strip().split('P')[0]
            if text.find('저작권자와의 제휴를') != -1:
                cnt_chk = 1
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
        token = ''
        with requests.Session() as s:
            Page = {
                'act': 'get_token'
            }
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'http://www.filekok.com',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            login_token = s.post('http://www.filekok.com/ajax_controller.php', data=Page, headers=headers)
            soup = bs(login_token.text, 'html.parser')
            text = str(soup)
            token = text.split('{"result":"')[1].split('","')[0]

            LOGIN_INFO = {
                    'browser': 'pc',
                    'isSSL': 'Y',
                    'mb_id': 'up0001',
                    'mb_pw': 'up0001',
                    'repage': 'reload',
                    'token': token,
                    'url': '/main/module/loginClass.php',
                    'url_ssl': 'https://ssl.filekok.com/loginClass.php'
            }
            login_req = s.post('https://ssl.filekok.com/loginClass.php', data=LOGIN_INFO, headers=headers)
            post_one  = s.post(url, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            cnt_chk = 0

            cnt_price = soup.find_all('td', 'txt')[4].text.replace("\n","").replace("\t","").replace(" ","").replace(",","").strip().split(" / ")[1].split("P")[0]
            if soup.find('span', 'half_arrow'):
                cnt_price = soup.find_all('b', class_=False)[2].text.strip().replace(",","").split("P")[0]
            if soup.find_all('td', 'txt')[4].find('img'):
                jehu = soup.find_all('td', 'txt')[4].find('img')['alt']
                if jehu == '제휴컨텐츠':
                    cnt_chk= 1
            if soup.find('span', 'half_arrow'):
                jehu = str(soup)
                if jehu.find('alt="제휴컨텐츠"') != -1:
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
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find_all('td', 'black_a_s')[2].find('font').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(",","").strip().split("P")[0]
        if cnt_price.find('↓') != -1:
            cnt_price = soup.find_all('td', 'black_a_s')[2].find_all('font')[1].text.replace("\n","").replace("\t","").replace("\xa0", "").replace(",","").strip().split("P")[0]
        if soup.find('td', 'brown_b').find('img'):
            img = soup.find('td', 'brown_b').find('img')['src']
            if img.find('icon/icon_join_info2') != -1:
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
        with requests.Session() as s:
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

            cnt_check = soup.find('td', 'pad_left5').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip()
            cnt_pricecheck = cnt_check.count('P')
            if cnt_pricecheck == 1:
                cnt_price = soup.find('td', 'pad_left5').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("/")[1].split("P")[0]
            else:
                cnt_price = soup.find('td', 'pad_left5').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("P")[1].split("P")[0]
            if soup.find('li', 'tit_le2'):
                cnt_chk = 1
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
        cnt_num = url.split("idx=")[1]
        url2 = "https://filecity.kr/html/view2.html"
        with requests.Session() as s:
            idx = {
                'idx': cnt_num,
                'link': 'list',
                'type': 'layer'
            }
            post_two  = s.post(url2, data=idx)
            soup = bs(post_two.text, 'html.parser')
            cnt_chk = 0

            cnt_price = soup.find('li', 'point02').find('span', 'num').text.strip().replace(",","")
            div = soup.find('div', 'cont_info clearfix')
            if div.find('ul', 'clearfix icon_alliance'):
                cnt_chk = 1
            if div.find('ul', 'clearfix icon_sale'):
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
        cnt_num = url.split("view/")[1].split("/")[0]
        urlSub = 'http://filecast.co.kr/www/contents/view/'+cnt_num
        r = requests.get(urlSub)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('span', 'txt_blue txt_block').find('b').text.replace(",","").strip()
        ico = soup.find('span', 'ico_partner')['class']
        try:
            if ico[1] == 'on':
                cnt_chk = 1
        except:
            cnt_chk = 0
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
        r = requests.get(url)
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

def filemanCheck(url):
    try:
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
            post_one  = s.get(url)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)
            tr = soup.find('table', cellspacing='1').find_all('tr')[1]
            cnt_chk = 0

            cnt_price = tr.find_all('td')[6].text.strip().replace("\n","").replace("\t","").replace(" ","").split("P")[0]
            if text.find('저작권자와의 제휴') != -1:
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
        LOGIN_INFO = {
            'Frame_login': 'Ok',
            'idSave': '1',
            'm_id': 'up0001',
            'm_pwd': 'up0001',
            'sReturnUri': 'http%3A%2F%2Ffilehon.com%2F',
            'x': '22',
            'y': '25'
        }
        with requests.Session() as s:
            login_req = s.post('http://filehon.com/member/loginCheck.php', data=LOGIN_INFO)
            post_one  = s.get(url)
            soup = bs(post_one.text, 'html.parser')
            cnt_chk = 0
            table = soup.find('table', 'ctnVtbl').find_all('td')[4]

            cnt_price = table.find('span', 'price').text.strip().replace(",","")
            if table.find('img'):
                cnt_chk = 1
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
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().replace(",","")
        if soup.find('p', 'careMsg'):
            cnt_chkCh = soup.find('p', 'careMsg').text.strip()
            if cnt_chkCh.find('제휴') != -1:
                cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def daokiCheck(url):
    try:
        r = requests.get('http://oradisk.com/')
        c = r.content
        soup = bs(c.decode('euc-kr','replace'), 'html.parser')
        captcha_aes = soup.find('input', id='captcha_aes')['value']
        LOGIN_INFO = {
            'Frame_login': 'Ok',
            'captcha_aes': captcha_aes,
            'fromsite': 'oradisk',
            'idSave': '0',
            'm': '',
            'm_id': 'up0001',
            'm_pwd': 'up0001'
        }
        with requests.Session() as s:
            login_req = s.post('http://daoki.com/member/loginCheck.php', data=LOGIN_INFO)
            cnt_num = url.split('idx=')[1].split('&')[0]
            aes = url.split('aes=')[1]
            url2 = 'http://daoki.com/contents/view_top_filedown_new.html?idx='+cnt_num+'&aes='+aes

            post_two  = s.get(url2)
            c = post_two.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            text = str(soup).split("<!-- 파일 리스트 종료 -->")[1].split("-->")[0]
            cnt_chk = 0

            cnt_price = text.split('bold;">')[1].split("</span>")[0].replace(",","")
            jehu = soup.find_all('table')[5].find_all('td')[2].find('img')['src']
            if jehu.find('allri_icon') != -1:
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
        cnt_chk = 0
        td = soup.find('td', 'infotable_td2')
        text = str(td)

        cnt_price = soup.find('td', 'infotable_td2').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(" ", "").replace(",","").strip().split("P")[0]
        if text.find('제휴') != -1:
                cnt_chk = 1
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
        cnt_num = url.split('co_id=')[1]
        url2 = 'http://www.bigfile.co.kr/content/content_sub.php?co_id='+cnt_num
        r = requests.get(url2, cookies = {'addOpenedCookie':'co_id'})
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('li', 'gm ar02').text.split(" 캐시")[0].replace(",","").strip()
        if soup.find('div', 'ssc_cnt_titles'):
            if soup.find('span', 'con_ico'):
                span = soup.find('span', 'con_ico')
                text = str(span)
                if text.find('cooperation_icon') != -1:
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

import json
def applefileCheck(url):
    cnt_chk = 0
    cnt_num = url.split('idx=')[1].strip()
    try:
        data3 = {
            'idx': cnt_num,
            'type': 'info'
        }
        ajax_url = 'https://www.applefile.com/module/contents/view.php'
        r = requests.post(ajax_url, data=data3)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        text = str(soup).split('</p>')[0].strip()
        json_obj = json.loads(text)

        jehu = json_obj['chkcopy']
        if jehu == 'Y':
            cnt_chk = 1
        cnt_price = json_obj['cash'].replace(",","")
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filekukiCheck(url):
    LOGIN_INFO = {
        'passwd': 'up0001',
        'useridorig': 'up0001'
    }
    cookies = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}
    try:
        with requests.Session() as s:
            login_req = s.post('https://www.filekuki.com/db/db_login.jsp', data=LOGIN_INFO, cookies=cookies)
            post_one  = s.get(url, cookies=cookies)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            cnt_chk = 0
            table = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")

            cnt_price = table.split("쿠키")[0].replace(",","").strip()
            if soup.find('img', alt='특별할인'):
                priceCh = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
                cnt_price = priceCh.split("→")[1].split("쿠키")[0].strip()

            if soup.find('img', alt='제휴'):
                cnt_chk = 1
            if text.find('filename') == -1:
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
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://www.filekok.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    try:
        with requests.Session() as s:
            Data = {
            'act': 'get_token'
            }
            token_req = s.post('http://www.filelon.com/ajax_controller.php', data=Data, headers=headers)
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
            login_req = s.post('https://ssl.filelon.com/loginClass.php', data=LOGIN_INFO, headers=headers)

            post_two  = s.get(url, headers=headers)
            soup2 = bs(post_two.text, 'html.parser')
            table = soup2.find_all('table', 'pop_base')[1]
            cnt_chk = 0

            cnt_price = table.find('td', 'txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("/")[1].split("P")[0]
            if table.find('b', class_=None):
                cnt_price = table.find('b', class_=None).text.strip().replace(",", "").split("P")[0]
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

def filehamCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c.decode('euc-kr','replace'),"html.parser")
        text = str(soup)
        cnt_chk = 0

        price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip()
        if price.find('\n') != -1:
            cnt_price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip().split("\n")[1].split("P")[0].replace(",","")
        else:
            cnt_price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip().split("P")[0].replace(",","")
        if soup.find('img', src='http://wimg.fileham.com/popup/new/dc_title_al.png'):
            cnt_chk = 1
        elif text.find("<script>location.href='/main/popup") != -1:
            cnt_chk = 2
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def dodofileCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c.decode('euc-kr','replace'),"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('span', 'b_price').text.strip().replace(",","").replace(" ","").split("P")[0]
        if soup.find('span', 'pl10').find('img'):
            jehu = soup.find('span', 'pl10').find('img')['src']
            if jehu.find('jehu.gif') != -1:
                cnt_chk = 1
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filesunCheck(url):
    try:
        with requests.Session() as s:
            post_two  = s.get(url)
            soup2 = bs(post_two.text, 'html.parser')
            cnt_chk = 0

            if soup2.find('img', 'allianceicon'):
                cnt_chk = 1
            cnt_price = soup2.find('span', 'pointSize').text.strip()
            if cnt_price.find("→") != -1:
                cnt_price = cnt_price.replace(" ","").replace(",","").split("→")[1].split("P")[0]
            else:
                cnt_price = cnt_price.replace(" ","").replace(",","").split("P")[0]
    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filemaruCheck(url):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'ko-KR',
        'Cache-Control' : 'no-cache',
        'Connection' : 'Keep-Alive',
        'Cookie': 'PHPSESSID=79p4oijitdr2tsnpkko5lnvbd3; G_ENABLED_IDPS=google; ch-veil-id=76952a55-ffad-4b56-b22d-8493e05dbc70; ch-session-37430=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiIzNzQzMC02MDQ1YWU0ZjUzNDkxNTE2ODhkYSIsImlhdCI6MTYxNTE3OTM0MywiZXhwIjoxNjE3NzcxMzQzfQ.tjOwff9ZpVOR3fMYSjT-0TORI7N_mC3bpR17nWm1B_o; m_grade=1; loginVer=60; upid=1993412; mid=0719i619a7193a19f6198719b619c719j6195919d919h919e9190a191719971927199719; nick=do.2; Usr=dkdl1748%40naver.com; ungrade=0; adult=1; total_cash=1920; cmn_cash=1880; bns_cash=40; coupon=0; memo_cnt=0; LogChk=Y',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host' : 'www.filemaru.com',
        'Referer' : 'http://www.filemaru.com/',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'X-Requested-With': 'XMLHttpRequest'
    }

    cnt_num = url.split('idx=')[1].strip()
    Page = {
        'ci': '79p4oijitdr2tsnpkko5lnvbd3',
        'idx': cnt_num
    }
    try:
        with requests.Session() as s:
            post_one  = s.post('https://www.filemaru.com/proInclude/ajax/view.php', data=Page, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            cnt_chk = 0

            cnt_price = text.split('filePoint" : "')[1].split('"')[0].replace(",","")
            jehu = text.split('fileAllianceChk" : "')[1].split('"')[0]
            if jehu == "Y":
                cnt_chk = 1

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

def filemongCheck(url):
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'crossCookie=bar; PHPSESSID=ogiikktergbpef071apso79hv2',
        'Host': 'filemong.com',
        'Referer': 'https://filemong.com/contents/list.html?section=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        with requests.Session() as s:
            cnt_num = url.split('idx=')[1].strip()
            Data2 = {
                'bbs_idx': cnt_num
            }

            with requests.Session() as s:
                link2 = 'https://filemong.com/contents/info_ajax.php'
                post_two  = s.post(link2, headers=headers, data=Data2, allow_redirects=False)
                soup = bs(post_two.text, 'html.parser')
                cnt_chk = 0

                if soup.find('table', 'v-info').find('span', 'badge0'):
                    jehu = soup.find('table', 'v-info').find('span', 'badge0').text.strip()
                    if jehu == '제휴':
                        cnt_chk = 1
                    cnt_price = soup.find('table', 'v-info').find_all('td')[3].text.split('제휴')[1].replace(',', '').replace('p', '').strip()
                else:
                    cnt_price = soup.find('table', 'v-info').find_all('td')[3].text.replace(',', '').replace('p', '').strip()

    except:
        cnt_price = 0
        cnt_chk = 2

    data = {
        'Cnt_price': cnt_price,
        'Cnt_chk': cnt_chk
    }
    return data

# def main():
#     cnt_id = 'filemaru'
#     url = 'http://www.filemaru.com/proInclude/ajax/view.php?idx=16746936'
#     data = imgCheck(cnt_id,url)
#     print(cnt_id)
#     print(data)
#
# if __name__=='__main__':
#     start_time = time.time()
#     main()
