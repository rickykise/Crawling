# timeforum 검색
import datetime,pymysql,time
import sys,os
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
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

def startCrawling(key):
    print("키워드 : ", key)
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        i = 0;
        link = 'http://www.timeforum.co.kr/index.php?mid=FreeBoard&search_target=title_content&search_keyword='+key+'&page='
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        html = driver.find_element_by_class_name("board_list").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find('table').find("tbody").find_all("tr",class_=False)

        for item in tr:
            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            title = item.find('td', 'title').find_all('a')[0].text
            writer = item.find('td', 'author').find('a').text
            timech = item.find('td', 'time').text
            href = 'http://www.timeforum.co.kr' + item.find('td', 'title').find_all('a')[0]['href']
            board_number = href.split("&document_srl=")[1]
            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_class_name("docInner").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            dateCheck = tags.find('div', 'read_header').find('span', 'time').text.strip()
            datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M").strftime('%Y-%m-%d %H:%M')
            date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M").strftime('%Y-%m-%d %H:%M')
            contents = tags.find('div', 'read_body').text.replace("\n","").replace("\t","").replace("\xa0", "")
            timecheck = timech.find(':')
            if timecheck == -1: check=False;break
            print(timech)

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
                dbResult = insert(conn,'timeforum',data['title'],data['contents'],data['writer'],'',data['date'],data['url'],data['board_number'])
                if dbResult:
                    check=False
            finally :
                conn.close()

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    conn.close()

    print("timeforum 크롤링 시작")
    startCrawling('벤츠')
    print("timeforum 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
