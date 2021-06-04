import argparse
import datetime,time
from google.cloud import language_v1
from textFun import *

def startCrawling():
    client = language_v1.LanguageServiceClient()

    # with open(movie_review_filename, "r") as review_file:
    #     # Instantiates a plain text document.
    #     content = review_file.read()
    # content = '그저 그럼'

    getText = getTest()
    for t in getText:
        getT = t[0]
        getIdx = t[1]
        getResult = t
        print(getT)

        document = language_v1.Document(content=getT, type_=language_v1.Document.Type.PLAIN_TEXT)
        annotations = client.analyze_sentiment(request={'document': document})

        textType = ''
        score = annotations.document_sentiment.score
        getScore = round(float(score),2)
        magnitude = annotations.document_sentiment.magnitude
        getMagnitude = round(float(magnitude),2)

        # print("점수 : ", getScore)
        # print("규모 : ", magnitude)
        # print('idx : ', getIdx)

        if getScore >= 0.25:
            textType = '좋은글'
        elif getScore <= 0.24 and getScore >= -0.25:
            textType = '보통글'
        elif getScore <= -0.24:
            textType = '나쁜글'

        print(textType)
        print("=================================")

if __name__ == "__main__":
    start_time = time.time()

    print("=================================")
    print('analysis 시작')
    startCrawling()
    print('analysis 끝')
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
