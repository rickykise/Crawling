# encar 검색
import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'community_data'
        data = {
            'community_name': args[0],
            'community_title': args[1],
            'community_content': args[2],
            'community_writer': args[3],
            'community_writer_IP': args[4],
            'writeDate': args[5],
            'title_key': '벤츠',
            'keyword': '벤츠',
            'keyword_type': '',
            'url': args[6],
            'board_number': args[7],
            'createDate': now,
            'updateDate':now
        }
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        # print(sql, list(data.values()))
        curs.execute(sql, list(data.values()))
        conn.commit()
    except Exception as e:
        if e.args[0] != 1062:
            print("===========에러==========\n에러 : ",e,"\n",args,"\n===========에러==========")
        else:
            result = True
            conn.rollback()
    finally:
        return result

def startCrawling():
    link = 'http://www.encar.com/mg/search.do?searchText=%BA%A5%C3%F7'
    check = True; paramKey = None; insertNum =0

    while check:
        textHtml = requests.get(link).text
        soup = BeautifulSoup(textHtml,'html.parser')
        divall = soup.find('div','contents').find('div', 'mgz_inner').find_all("div", class_='thmnil_cnt')
        for items in divall:
            ul = items.find('ul', 'thmnil_list_pt').find_all('li')
            for item in ul:
                conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item.find('span', 'smry').find('strong','tit_smry').text
                contents = item.find('span', 'smry').find('span','cnt_smry').text.replace("\n","").replace("\t","")
                dateCheck = item.find('span', 'smry').find('span', 'cat').text.strip()
                datetime.datetime.strptime(dateCheck, "%Y.%m.%d.").strftime('%Y-%m-%d %H:%M')
                date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d.").strftime('%Y-%m-%d %H:%M')
                href = 'http://www.encar.com' + item.find('a')['href'].split("&searchText=벤츠")[0]
                html = requests.get(href).text
                tags = BeautifulSoup(html,'html.parser')
                writer = tags.find('div', 'txt_view_info').find('span', 'repter').text
                board_number = href.split("&postid=")[1]

                data = {
                    'title' : title,
                    'url' : href,
                    'writer': writer,
                    'board_number': board_number,
                    'contents' : contents,
                    'date': date
                }
                # print(data)
                conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn,'encar',data['title'],data['contents'],data['writer'],'',data['date'],data['url'],data['board_number'])
                    if dbResult:
                        check=False
                finally :
                    conn.close()
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    conn.close()

    print("encar 크롤링 시작")
    startCrawling()
    print("encar 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
