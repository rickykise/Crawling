import re
import pymysql,time,datetime
import time,datetime
from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from openpyxl import load_workbook
conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

# 댓글 가져오는 함수
def getReply():
    result = None
    with conn.cursor() as curs:
        # sql = "select reply_content from reply_data where textType = '나쁜글' order by createDate desc limit 500;"
        sql = "SELECT s_text, s_idx FROM `union`.text_sep;"
        curs.execute(sql)
        result = curs.fetchall()

        return result

# 평점 가져오는 함수
def getScore():
    result = None
    with conn.cursor() as curs:
        sql = "SELECT textType, text FROM textType_data order by text_idx desc;"
        curs.execute(sql)
        result = curs.fetchall()

        return result

# okt = Okt()
# text = '재미없음'
# sep = okt.morphs(text)
# print(sep)
# text 분석 함수
def textCheck(score,text,check_text):
    okt = Okt()
    train_x, test_x, train_y, test_y = train_test_split(text, score, test_size=0.2, random_state=0)
    tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1, 2), min_df=1, max_df=50)
    tfv.fit(train_x)
    tfv_train_x = tfv.transform(train_x)

    clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='auto')
    params = {'C': [1,3,5,7,9]}
    grid_cv = GridSearchCV(clf, param_grid=params, cv=4, scoring='accuracy', verbose=1, iid=False, n_jobs=-1)
    grid_cv.fit(tfv_train_x, train_y)

    # print(grid_cv.best_params_)
    # print(grid_cv.best_score_)

    # tfv_test_x = tfv.transform(test_x)
    # grid_cv.best_estimator_.score(tfv_test_x, test_y)
    # print(grid_cv.best_estimator_.score(tfv_test_x, test_y)) 정확도

    # check_list = []
    # check_list.append(check_text)

    my_review = tfv.transform(check_text)
    testPrint = grid_cv.best_estimator_.predict(my_review)

    return testPrint

def autoTextUpdate(data):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = 'update `union`.text_sep set s_texttype=%s where s_idx=%s;'
        curs.execute(sql,(data['textType'],data['community_idx']))
        conn.commit()
    finally:
        conn.close()

# def getExcel():
#     wb = load_workbook('text_test.xlsx', read_only=True)
#     ws = wb.get_sheet_by_name("Sheet2")
#     for r in ws.rows:
#         a = r[0].value
#         b = r[1].value
#         if a == '좋은글':
#             score.append('좋은글')
#             text.append(b)
#         elif a == '관심글':
#             score.append('관심글')
#             text.append(b)
#         elif a == '기타글':
#             score.append('기타글')
#             text.append(b)
#         elif a == '나쁜글':
#             score.append('나쁜글')
#             text.append(b)
