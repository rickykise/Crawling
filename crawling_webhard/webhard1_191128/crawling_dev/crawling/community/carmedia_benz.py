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
    print("키워드 : 벤츠")
    i = 0;
    link = 'http://www.carmedia.co.kr/index.php?mid=news&act=IS&where=document&search_target=title&is_keyword=벤츠&page='
    check = True; paramKey = None; insertNum = 0

    while check:
        i = i+1
        textHtml = requests.get(link+str(i)).text
        soup = BeautifulSoup(textHtml,'html.parser')
        li = soup.find('div', 'has-sub content').find('ul', 'searchResult').find_all('li')

        for item in li:
            title = item.find('dl').find('a').text
            href = item.find('dl').find('a')['href']
            writer = item.find('address').find('strong').text
            date = item.find('address').find('span', 'time').text.strip()
            board_number = href.split("/")[3]
            contents = item.find('dl').find('dd').text.replace("\n","").replace("\t","")

            data = {
                'title' : title,
                'url' : href,
                'writer': writer,
                'board_number': board_number,
                'contents' : contents,
                'date': date
            }
            # if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
            if data['date'] < '2018-04-09': check=False;break
            print(data)

            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                dbResult = insert(conn,'carmedia',data['title'],data['contents'],data['writer'],'',data['date'],data['url'],data['board_number'])
                if dbResult:
                    return False
            finally :
                conn.close()
        return True
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    conn.close()

    print("carmedia 크롤링 시작")
    startCrawling()
    print("carmedia 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
