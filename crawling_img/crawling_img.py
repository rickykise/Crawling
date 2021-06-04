# 이미지 캡쳐
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from tkinter.filedialog import askopenfilename
import requests
import pandas as pd
import pyautogui
import subprocess
# 이미지 저장
import datetime,time,pymysql
import os

def deleteRow():
	conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
	try:
		sql = "(SELECT 'portal',portal_idx as idx,portal_name as name,thumbnail FROM portal_data WHERE textType = '나쁜글' and portal_type!='score' and thumbnail is not Null)\
		        UNION ALL (SELECT 'media',media_idx as idx,media_name as name,thumbnail FROM media_data WHERE textType = '나쁜글' and thumbnail is not Null)\
		        UNION ALL (SELECT 'community',community_idx as idx,community_name as name,thumbnail FROM community_data WHERE textType = '나쁜글' and thumbnail is not Null);"
		with conn.cursor() as curs:
		    tArr = []
		    curs.execute(sql)
		    returnValue = curs.fetchall()
		    arr = list(returnValue)
		    for idx,val in enumerate(arr):
		        temp = list(val)
		        tArr.append([i for i in temp])

		if not tArr: return

		import os
		path_dir = 'c:\img\\'
		file_list1 = os.listdir(path_dir)
		for idx,filename in enumerate(file_list1):
			full_filename = os.path.join(path_dir, filename)
			ext = os.path.splitext(full_filename)[-1]
			if ext == '.zip':
				del file_list1[idx]
		file_list2 = []
		for f in file_list1:
			if len(file_list2) == 0:
				file_list2 = os.listdir('D:\img\\'+f)
			else:
				file_list2.extend(os.listdir('D:\img\\'+f))

		noimg = []

		for item in tArr:
			if len(item[3].split('/')) != 3:
				continue
			checkName = item[3].split('/')[2]
			if all(checkName != s for s in file_list2):
				noimg.append(item)
		if noimg:
			for item in noimg:
				with conn.cursor() as curs:
					sql = "UPDATE "+item[0]+"_data SET thumbnail=NULL WHERE thumbnail=%s and "+item[0]+"_name=%s;"
					curs.execute(sql,(item[3],item[2]))
					conn.commit()
	finally:
		conn.close()

def get_save(num, url, savefile):
	# print('get_save :',num, url, savefile)
	print('실행')
	print(url)
	if url.find("dcinside") != -1:
		print('dc패스')
		pass
	chromeOptions = webdriver.ChromeOptions()
	chromeOptions.add_argument("disable-infobars")
	driver = webdriver.Chrome('C:\python36\driver\chromedriver.exe', chrome_options=chromeOptions)
	driver.set_window_position(0, 0) # 크롬 창 왼쪽 위 위
	driver.set_window_size(1080, 1748) # 크롬 창 사이즈
	# driver.set_window_size(1898, 796)
	# driver.set_window_size(1200, 1748) # 크롬 창 사이즈

	# alert창 체크
	try:
		driver.get(url)
		WebDriverWait(driver, 1).until(EC.alert_is_present())
		driver.quit()
		print('alert창이 있어 건너뜁니다.')
		return
	except TimeoutException:
		# print('TimeoutException')
		pass

	import pyscreenshot
	try:
		driver.execute_script("window.scrollTo(0, 0);")
		if url.find("inven") != -1: driver.execute_script("window.scrollTo(0, 700);");time.sleep(1)
		# elif url.find("dcinside") != -1:
		# 	print('dc패스')
		# 	pass
			# pyautogui.hotkey('ctrl', '-')
			# time.sleep(2)
			# pyautogui.typewrite(['right', 'right'])
			# time.sleep(2)
		im = pyscreenshot.grab(bbox=(0, 0, 1080, 1918))
		# im = pyscreenshot.grab(bbox=(0, 0, 1200, 1918))
		# im = pyscreenshot.grab(bbox=(0, 0, 1891, 965))
		if not os.path.isdir(savefile): im.save(savefile)
		im.close()
		print(time.asctime(), ': ', savefile, '을 저장하였습니다.')
		print(savefile)
		dis = subprocess.call("pscp -pw sms@unionc "+savefile+" root@49.247.5.169:/usr/local/img/"+datetime.datetime.now().strftime('%Y-%m-%d')+"/", shell=True)
		print(dis)
	except Exception as e:
		print('pyscreenshot Error')
		print(e)
		pass
	finally:
		driver.quit()

def getTable():
	conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')

	try:
		sqlArr = {
			"portal":["portal_name","portal_idx","portal_data","and portal_type!='score'"],
			"media":["media_name","media_idx","media_data",""],
			"community":["community_name","community_idx","community_data",""]
		}
		result = []
		for item in sqlArr:
			updateArr = []
			today = datetime.datetime.now().strftime('%Y-%m-%d')
			sql = "SELECT url,"+sqlArr[item][0]+","+sqlArr[item][1]+",createDate FROM "+sqlArr[item][2]+" WHERE thumbnail is Null and not url like '%g-enews%' and not url like '%cp.news.search%' and DATE(updateDate) = CURDATE() and textType='나쁜글' "+sqlArr[item][3]+" ORDER BY "+sqlArr[item][1]+" desc;"
			# sql = "SELECT url,"+sqlArr[item][0]+","+sqlArr[item][1]+",createDate FROM "+sqlArr[item][2]+" WHERE thumbnail is Null and "+sqlArr[item][0]+" != 'dcinside' and not url like '%g-enews%' and not url like '%cp.news.search%' and DATE(updateDate) >= '"+today+" 00:00:00' and textType='나쁜글' "+sqlArr[item][3]+" ORDER BY "+sqlArr[item][1]+" desc;"

			with conn.cursor() as curs:
				curs.execute(sql)
				returnValue = curs.fetchall()
				arr = list(returnValue)
				for idx,val in enumerate(arr):
					temp = list(val)
					thumbnail = "/"+today+"/"+temp[1]+"_"+str(temp[2])+temp[3].strftime('%Y%m%d')+".jpg"
					updateArr.append([thumbnail,temp[2],temp[0],sqlArr[item][2]])

			for val in updateArr:
				with conn.cursor() as curs:
					sql = "UPDATE "+sqlArr[item][2]+" SET thumbnail=%s WHERE "+sqlArr[item][1]+"=%s and thumbnail is Null;"
					curs.execute(sql,(val[0],val[1]))
					conn.commit()
			if len(result) < 1:
				result = updateArr
			else:
				result.extend(updateArr)
		return result
	except Exception as e:
		print(e)
	finally:
		conn.close()

def mkdir():
	dirname = 'C:\img\\'+datetime.datetime.now().strftime('%Y-%m-%d')
	if not os.path.isdir(dirname):
		os.mkdir(dirname)

def main():
	mkdir()
	rArr = getTable()

	if rArr:
		print("나쁜 게시글 :",len(rArr))
		for idx,item in enumerate(rArr):
			url = item[2]
			filename = item[0]
			typeName = item[0]
			if url.find('dcinside') != -1:
				continue
			get_save(idx,url,'c:/img'+filename)

		deleteRow()
	print('완료되었습니다.')

if __name__=='__main__':
	main()
    # 부득이하게 찍는 중간에 프로그램 끝났으면 deleteRow()해주기
	# deleteRow()
