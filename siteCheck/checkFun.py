import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

# osp_url 가져오는 함수
def getHostUrl():
    with conn.cursor() as curs:
        sql = "select host_url, cnt_del_date, cnt_osp from cnt_f_list where cnt_del_act = 1 and cnt_chk!=4 and cnt_osp = 'qmi777';"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in returnValue:
                returnValue[key].append(result[i][1])
                returnValue[key].append(result[i][2])
            else:
                returnValue.update({key:[result[i][1],result[i][2]]})
        # print(returnValue)

        return returnValue

# cnt_f_list DB 업데이트 함수
def dbUpdate(checkNum,now,host_url):
    if checkNum == 1:
        # print('삭제')
        sql = "update cnt_f_list set cnt_chk=4, cnt_regdate2=%s, cnt_dend_act=1, cnt_dend_date=%s where host_url=%s;"
        curs.execute(sql,(now,now,host_url))
        conn.commit()
    else:
        # print('유지')
        sql = "update cnt_f_list set cnt_regdate2=%s where host_url=%s;"
        curs.execute(sql,(now,host_url))
        conn.commit()

def ospCheck(cnt_id, url):
    checkNum = 0
    if cnt_id == '135mov':
        cnt_id = 'mov'
    elif cnt_id == '381668.com':
        cnt_id = 'com'
    elif cnt_id == '55cn':
        cnt_id = 'cn'
    elif cnt_id == '5kpw':
        cnt_id = 'kpw'
    elif cnt_id == '6080n':
        cnt_id = 'n'

    cnt_id = cnt_id.replace('.', '').replace('-', '')

    try:
        result = cnt_id+'Check(url)'
        return eval(result)
    except Exception as e:
        return checkNum

def phimchatCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        check_url = soup.find('iframe')['src']

        r = requests.get(check_url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        check_url2 =  soup.find('iframe')['src']
        r = requests.get(check_url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Видео заблокировано по требованию правообладателя') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def movCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('此影片已经删除') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def comCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('404 Not Found') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def cnCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        print(text)
        if text.find('This process is automatic') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def kpwCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('sorry') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def nCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('404 Not Found') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def bosku21Check(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('404 !') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def daditvCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        # print(text)
        # if text.find('This process is automatic') != -1:
        #     checkNum = 1
        # else:
        #     checkNum = 0

    except:
        checkNum = 0

    return checkNum

def dizilostCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        if soup.find('div',  id='vast'):
            checkNum = 0
        else:
            checkNum = 1

    except:
        checkNum = 0

    return checkNum

def doramatvCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Ой, ой, страничка') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def doubiekanCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('404 Not') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def dramakuCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Copyright infringement') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def dramaserial21Check(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('404') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def dududyCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('获取数据失败') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def filmoserialruCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('404 Not Found') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def fullphimCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Oh no!') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def haitumCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('抱歉，未找到相关页') != -1:
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def hayhdCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        if soup.find('div', 'block servers'):
            checkNum = 0
        else:
            checkNum = 1
    except:
        checkNum = 0

    return checkNum

def hitseriesCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('404 Not Found') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def huphimCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        if soup.find('div', 'play-detail'):
            checkNum = 0
        else:
            checkNum = 1
    except:
        checkNum = 0

    return checkNum

def kekedianyingCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        if soup.find('ul', 'stui-content__playlist'):
            checkNum = 0
        else:
            checkNum = 1
    except:
        checkNum = 0

    return checkNum

def kenhphimCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        if soup.find('div', 'episodes'):
            checkNum = 0
        else:
            checkNum = 1
    except:
        checkNum = 0

    return checkNum

def kordramasCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Nothing Here') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def mfilmCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Không tìm thấy') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def ngonphimCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        check_url = soup.find('iframe')['src']
        r = requests.get(check_url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        check_url2 =  soup.find('iframe')['src']
        r = requests.get(check_url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Видео заблокировано по требованию правообладателя') != -1:
            checkNum = 1
        elif text.find('404'):
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def nontondramaCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Nothing Found') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def nungsubCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Error 404') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def omberbagiCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Page not found') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def ongtvCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Trang bạn tìm') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def pangzitvCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('requested was not found') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def phimtronCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        if soup.find('div', 'col-md-3 col-xs-3 m-l-20 m-r-20'):
            div = soup.find('div', 'col-md-3 col-xs-3 m-l-20 m-r-20')
            sub_url = div.find('a')['href']

            r = requests.get(sub_url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)
            if text.find('404 Not Found') != -1:
                checkNum = 1
            else:
                checkNum = 0
        else:
            checkNum = 1
    except:
        checkNum = 0

    return checkNum

def phimviethanCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        check_url = soup.find('iframe')['src']
        r = requests.get(check_url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        check_url2 =  soup.find('iframe')['src']
        r = requests.get(check_url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Видео заблокировано по требованию правообладателя') != -1:
            checkNum = 1
        elif text.find('404'):
            checkNum = 1
        else:
            checkNum = 0

    except:
        checkNum = 0

    return checkNum

def phimvuihdCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Lỗi 404') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def qmi777Check(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('此影片已经删除') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def rapphim18Check(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        if soup.find('div', 'server'):
            checkNum = 0
        else:
            checkNum = 1
    except:
        checkNum = 0

    return checkNum

def tiktokvideodownCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('此影片已经删') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def tv5boxCheck(url):
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR',
        'Connection': 'Keep-Alive',
        'Host': 'www.tv5box.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    try:
        r = requests.get(url, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('此影片') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def tv99Check(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('你找的影片已經遺失了') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def ulatmovieCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Not Found') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def vxiaomiidcnCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('系统提示') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def woliakanCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('您请求的资源未') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum

def xemphimCheck(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        if soup.find('div', 'server'):
            checkNum = 0
        else:
            checkNum = 1
    except:
        checkNum = 0

    return checkNum

def xuongphim18Check(url):
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('Phần này chưa có dữ liệu hoặc') != -1:
            checkNum = 1
        else:
            checkNum = 0
    except:
        checkNum = 0

    return checkNum
