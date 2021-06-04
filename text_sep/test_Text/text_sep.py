import datetime,time
from textFun import *
from openpyxl import load_workbook
from konlpy.tag import Okt

# 2:좋은글
# 1:관심글
# 0:나쁜글

def startCrawling():
    try:
        getST = getScore()
        score, text = [], []
        for s in getST:
            textType = '';a = s[0];b = s[1]
            if a == '2':
                score.append('2')
                text.append(b)
            elif a == '1':
                score.append('1')
                text.append(b)
            elif a == '0':
                score.append('0')
                text.append(b)

        getText = getReply()
        textGo = []
        textIdx = []
        for t in getText:
            getT = t[0]
            getIdx = t[1]
            textGo.append(getT)
            textIdx.append(getIdx)
        test_check = textCheck(score, text, textGo)

        for i in range(len(test_check)):
            if test_check[i] == '2':
                textType = '좋은글'
            elif test_check[i] == '1':
                textType = '관심글'
            elif test_check[i] == '0':
                textType = '나쁜글'

            # print(textGo[i])
            data = {
                'textType': textType,
                'community_idx': textIdx[i]
            }
            # print(data)
            # print("=================================")

            dbUpResult = autoTextUpdate(data)
    except:
        pass

if __name__=='__main__':
    start_time = time.time()

    print("=================================")
    print('text_sep 시작')
    startCrawling()
    print('text_sep 끝')
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
