import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import dis
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs


def imgCheck(cnt_id, url):

    print(cnt_id)

    result = cnt_id+'Check(url)'
    return eval(result)

    # return {
    #     'filekuki' : filekukiCheck(url),
    #     'filelon' : filelonCheck(url),
    #     'fileham' : filehamCheck(url),
    #     'applefile' : applefileCheck(url),
    #     'bigfile' : bigfileCheck(url),
    #     'bondisk' : bondiskCheck(url),
    #     'daoki' : daokiCheck(url),
    #     'fileguri' : fileguriCheck(url),
    #     'filehon' : filehonCheck(url),
    #     'fileman' : filemanCheck(url),
    #     'filetour' : filetourCheck(url)
    # }.get(cnt_id, '예외')

    elif cnt_id == 'applefile':
        data = applefileCheck(url)
        return data
    elif cnt_id == 'bigfile':
        data = bigfileCheck(url)
        return data
    elif cnt_id == 'bondisk':
        data = bondiskCheck(url)
        return data
    elif cnt_id == 'daoki':
        data = daokiCheck(url)
        return data

        filecastCheck
        filecityCheck
    elif cnt_id == 'fileguri':
        data = fileguriCheck(url)
        return data
    elif cnt_id == 'fileham':
        data = filehamCheck(url)
        return data
    elif cnt_id == 'filehon':
        data = filehonCheck(url)
        return data

        fileisCheck

        filejoCheck

        filekokCheck
    if cnt_id == 'filekuki':
        data = filekukiCheck(url)
        return data


    elif cnt_id == 'filelon':
        data = filelonCheck(url)
        return data

    elif cnt_id == 'fileman':
        data = filemanCheck(url)
        return data


    elif cnt_id == 'filetour':
        data = filetourCheck(url)
        return data

        gdisk

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
        with requests.Session() as s:
            post_one  = s.get(url)
            soup = bs(post_one.text, 'html.parser')
            cnt_chk = 0
            table = soup.find('table', 'ctnVtbl').find_all('td')[3]

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

def applefileCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        cnt_price = soup.find('div', 'td_point').find('li').text.split('P')[0].strip()
        if soup.find('li', 'icon').find('img'):
            cnt_chkCh = soup.find('li', 'icon').find('img')['title']
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
            if soup2.find('b', class_=None):
                cnt_price = soup2.find('b', class_=None).text.strip().replace(",", "").split("P")[0]
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

def main():
    cnt_id = 'applefile'
    url = 'http://applefile.com/contents/board_view.php?idx=16642687'
    imgCheck(cnt_id,url)
    print(imgCheck(cnt_id,url))

if __name__=='__main__':
    start_time = time.time()

    main()
