import pymysql,time,datetime
import urllib.parse
from urllib.parse import quote
import sys, os
# from percentcoding import quote, unquote
def startCrawling():



    str = '유아인'
    key = urllib.parse.quote(str.encode('cp949'))

    print(key)
    print('=======================================')




    # str = u'캐슬'
    # key = urllib.parse.quote(str.encode('utf-8'))
    # print(key)
    #
    # str1 = '%EC%BA%90%EC%8A%AC'
    # url = urllib.parse.quote(str1)
    # print(url)
    #
    # str2 = '%C4%B3%BD%BD'
    # url2 = urllib.parse.quote(str2)
    # print(url2)





if __name__=='__main__':
    start_time = time.time()

    startCrawling()
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
