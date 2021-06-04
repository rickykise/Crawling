import subprocess
import datetime,time

def startCrawling():
    # C:\Users\user\Desktop\crawling_dev\cgv_test/test.py
    dis = subprocess.call("C:\\Users\\user\\Desktop\\crawling_dev\\cgv_test/test.py", shell=True)

if __name__=='__main__':
    start_time = time.time()

    print("cgv 크롤링 시작")
    startCrawling()
    print("cgv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
