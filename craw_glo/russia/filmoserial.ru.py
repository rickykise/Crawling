import requests
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'http://filmoserial.ru/page/{}/?s=%D0%9A%D0%BE%D1%80%D0%B5%D1%8F&x=0&y=0'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div',id = 'content').find('ol').find_all('li')

        try:
            for item in li:
                url = item.find('h4').find('a')['href']
                titleSub = item.find('h4').find('a').text
                title_check = titleNull(titleSub)
                imgUrl = item.find('img')['src']
                # 이미지 체크
                img_chk = 0
                getIMG = getImage()
                imgCheck = imageCheck(imgUrl, getIMG)
                if imgCheck == None:
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']
                    otoImg = ''
                    cnt_cate = 0
                    img_chk = 0
                else:
                    cnt_id = imgCheck['i']
                    cnt_keyword = imgCheck['k']
                    otoImg = imgCheck['m']
                    cnt_cate = imgCheck['c']
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        img_chk = 1
                    else:
                        img_chk = 2

                urlArr = [url]
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                pageList = soup.find(lambda tag: tag.name=='p' and tag.has_attr('style') and tag.has_attr('id') and tag.text.find('Страницы:') != -1)

                if pageList:
                    urlArr.extend([i['href'] for i in pageList.find_all('a')])

                for url in urlArr:
                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    playNumList = soup.find('ol','group').find('div','').find_all(lambda tag: tag.name=='p' and tag.has_attr('style') == True and tag.has_attr('id') == False and (tag.text.find('серия') != -1 or tag.text.find('субтитры') != -1 or tag.text.find('озвучка') != -1))
                    playVideoList = soup.find('ol','group').find('div','').find_all(lambda tag: tag.name=='p' and len(tag.findChildren("iframe")) != 0 and len(tag.findChildren("em")) == 0)
                        
                    for item,item2 in zip(playNumList,playVideoList):
                        title = titleSub + '_' + item.text.strip()
                        title_null = titleNull(title)

                        
                        for iframe in item2.find_all('iframe'):
                            host_url = iframe['src']
                            if host_url.find('https') == -1:
                                host_url = 'https:'+host_url
                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'filmoserial.ru',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'russia',
                                'cnt_writer': '',
                                'cnt_cate': cnt_cate,
                                'site_p_img': imgUrl,
                                'site_r_img': otoImg,
                                'site_img_chk': img_chk
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("filmoserial.ru 크롤링 시작")
    startCrawling()
    print("filmoserial.ru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
