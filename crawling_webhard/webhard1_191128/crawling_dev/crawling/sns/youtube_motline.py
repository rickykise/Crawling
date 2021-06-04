# 유튜브 크롤링
import requests,re
import pymysql,time,datetime
from snsFun import *
from bs4 import BeautifulSoup

# # DB 저장하는 함수
# def insert(conn,*args):
#     import pymysql
#     import datetime
#     result = False
#     try:
#         curs = conn.cursor(pymysql.cursors.DictCursor)
#         now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         tableName = 'sns_data'
#         data = {
#             'sns_name': 'youtube',
#             'sns_title': args[0],
#             'sns_content': args[1],
#             'sns_writer': '모트라인',
#             'like_cnt': 0,
#             'reply_cnt': 0,
#             'share_cnt': 0,
#             'view_cnt': args[2],
#             'writeDate': args[3],
#             'title_key': '벤츠',
#             'keyword': '벤츠',
#             'url': args[4],
#             'createDate': now,
#             'updateDate':now
#         }
#
#         placeholders = ', '.join(['%s'] * len(data))
#         columns = ', '.join(data.keys())
#         sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
#         # print(sql, list(data.values()))
#         curs.execute(sql, list(data.values()))
#         conn.commit()
#     except Exception as e:
#         # if e.args[0] == 1062: break
#         if e.args[0] == 1062:
#             sql = "UPDATE" +tableName+ "SET view_cnt=%s, updateDate=%s WHERE url=%s;"
#             curs.execute(sql,(data['view_cnt'],data['updateDate'],data['url']))
#         else:
#             pass
#     finally:
#         return result

#크롤링 함수
def startCrawling():
    print("키워드 : 벤츠")
    link = 'https://www.youtube.com/user/motline2013/videos'
    check = True; paramKey = None; insertNum = 0; updateNum = 0

    while check:
        textHtml = requests.get(link).text
        soup = BeautifulSoup(textHtml, 'html.parser')
        if soup.find('ul','channels-browse-content-grid').find_all("div",class_='yt-lockup-content') == None: check = False; break
        div = soup.find('ul','channels-browse-content-grid').find_all("div",class_='yt-lockup-content')

        for item in div:
            # title = item.find('h3', 'yt-lockup-title ').text.split("-")[0].split("[모트라인] ")[1].replace("\n","").replace("\t","")
            view = item.find('ul', 'yt-lockup-meta-info').find_all('li')[0].text.split("조회수 ")[1].split("회")[0]
            view_cnt = int(''.join(list(filter(str.isdigit,view))))
            href = 'https://www.youtube.com'+ item.find('a')['href']
            print(href)
            html = requests.get(href).text
            tags = BeautifulSoup(html,'html.parser')
            dateCheck = tags.find('strong','watch-time-text').text.split(": ")[1].strip()
            datetime.datetime.strptime(dateCheck, "%Y. %m. %d.").strftime('%Y-%m-%d')
            date = datetime.datetime.strptime(dateCheck, "%Y. %m. %d.").strftime('%Y-%m-%d %H:%M')
            content = tags.find('p', id="eow-description").text.replace("\n","").replace("\t","")
            like = tags.find('span', 'like-button-renderer ').find('span', 'yt-uix-button-content').text
            like_cnt = int(''.join(list(filter(str.isdigit,like))))

            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'sns_name': 'youtube',
                    'sns_title': item.find('h3', 'yt-lockup-title ').text.split("-")[0].split("[모트라인] ")[1].replace("\n","").replace("\t",""),
                    'sns_content' : content,
                    'sns_writer': '모트라인',
                    'like_cnt': like_cnt,
                    'reply_cnt': 0,
                    'share_cnt': 0,
                    'view_cnt' : view_cnt,
                    'writeDate' : date,
                    'title_key': '벤츠',
                    'keyword': '벤츠',
                    'url' : href,
                    'createDate': now,
                    'updateDate': now
                }
                # if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
                # if data['writeDate'] < '2018-04-15': check=False;break
                # print(data)
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                curs.execute(sql, list(data.values()))
                conn.commit()
            except Exception as e:
                # if e.args[0] == 1062: break
                if e.args[0] == 1062:
                    sql = "UPDATE sns_data SET like_cnt=%s, view_cnt=%s, updateDate=%s WHERE url=%s;"
                    curs.execute(sql,(data['like_cnt'],data['view_cnt'],data['updateDate'],data['url']))
                    conn.commit()
                    updateNum = updateNum+1
                else:
                    pass
            finally :
                conn.close()
        return True
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("유튜브 모트라인 크롤링 시작")
    startCrawling()
    print("유튜브 모트라인 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))

# if __name__=='__main__':
#     startCrawling()
