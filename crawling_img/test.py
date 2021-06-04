import subprocess
import datetime,time,pymysql

def main():
    chromeOptions = webdriver.ChromeOptions()
	chromeOptions.add_argument("disable-infobars")
	driver = webdriver.Chrome('C:\python36\driver\chromedriver.exe', chrome_options=chromeOptions)
	driver.set_window_position(0, 0) # 크롬 창 왼쪽 위 위
	driver.set_window_size(1080, 1748) # 크롬 창 사이즈

	# alert창 체크
	try:
		driver.get("https://www.naver.com/")
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
		im = pyscreenshot.grab(bbox=(0, 0, 1080, 1918))
		if not os.path.isdir(savefile): im.save(savefile)
		im.close()
		print(time.asctime(), ': ', "C:\Users\YW\Desktop\crawling_img\test.jpg", '을 저장하였습니다.')
		dis = subprocess.call("pscp -pw sms@unionc C:\Users\YW\Desktop\crawling_img\test.jpg root@49.247.5.169:/usr/local/img/"+datetime.datetime.now().strftime('%Y-%m-%d')+"/", shell=True)
		print(dis)
	except Exception as e:
		print('pyscreenshot Error')
		print(e)
		pass
	finally:
		driver.quit()

if __name__=='__main__':
	main()
