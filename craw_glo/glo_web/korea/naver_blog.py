# 네이버 검색 Open API - 블로그 검색
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
import datetime,pymysql,time

def startCrawling(key, keyItem):
    yesterday = datetime.date.today() - datetime.timedelta(1)
    apiStartNum = 1;
    print("키워드 : "+key)
    cnt_id = keyItem[0]
    cnt_keyword = keyItem[1]
    try:
        while apiStartNum < 1000:
            data = searchNAPI('blog',key,'100',str(apiStartNum),'date')
            if not data: break
            if apiStartNum > data['total']: break
            for item in data['items']:
                item['title'] = setText(item['title'],0) # 제목
                item['description'] = setText(item['description'],1) # 내용
                item['postdate'] = (item['postdate'] != '') and datetime.datetime.strptime(item['postdate'],'%Y%m%d').strftime('%Y-%m-%d') or item['postdate'] #날짜

                if item['postdate'] == '' or item['link'].find('daum') != -1: continue
                title_null = titleNull(item['title'])
                # 키워드 체크
                keyCheck = googleCheckTitle(title_null, key, cnt_id)
                if keyCheck == None:
                    continue

                item['link'] = item['link'].replace("?Redirect=Log&amp;logNo=","/")
                item['link'] = (len(item['link']) > 255) and shortURL(item['link']) or item['link']
                item['bloggername'] = item['bloggername'].replace('님의 블로그','').replace('님의블로그','').replace('공식 블로그','').replace('공식블로그','').strip()
                if item['link'] is False: continue

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'naver',
                    'cnt_title': item['title'],
                    'cnt_title_null': title_null,
                    'host_url' : item['link'],
                    'host_cnt': '1',
                    'site_url': item['link'],
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'southkorea',
                    'cnt_writer': item['bloggername'],
                    'origin_url': '',
                    'origin_osp': ''
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)

            apiStartNum = apiStartNum + 100

    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeywordNaver()

    print("네이버 블로그 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("네이버 블로그 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
