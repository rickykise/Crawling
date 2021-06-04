# 이미지 캡쳐
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from tkinter.filedialog import askopenfilename
import requests
import pandas as pd
# 이미지 저장
import datetime,time,pymysql
import os
def getTable():
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT url FROM `union`.dint_list where d_idx >= 5648 order by d_idx asc;"
            curs.execute(sql)
            result = curs.fetchall()
            a = [i[0] for i in result]
        finally:
            conn.close()
            return a


def main():
	# mkdir()
	getUrl = getTable()

	for u in getUrl:
		print(u)
		print('=================')
		# url = item[2]
		# get_save(idx,url,'c:/img'+filename)
	# print('완료되었습니다.')

if __name__=='__main__':

	main()
