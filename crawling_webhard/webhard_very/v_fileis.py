import requests,re
import pymysql,time,datetime
import pyautogui
import datetime
import subprocess
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from webhardFun import *

def startCrawling():
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True;osp_id = 'fileis'
    getKey = getKeyword(osp_id,conn,curs)
    Osp_id=getKey[0];userId=getKey[1];userPw=getKey[2];key=getKey[3]
    getAd = getAdmin(Osp_id,conn,curs)
    admin_id=getAd[0];admin_pw=getAd[1]

    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now2 = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        driver.get('http://fileis.com/index.php')
        time.sleep(2)
        driver.find_element_by_id('m_id').send_keys(userId)
        driver.find_element_by_id('m_pwd').send_keys(userPw)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="btn_login"]').click()
        time.sleep(2)

        driver.get('http://fileis.com/contents/search.php?category1=&s_column=title&sCode=&emCopy=N&s_word='+key+'&viewList=Y')
        html = driver.find_element_by_id("contentsListWrap").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find_all('tr', 'bbs_list')
        for item in tr:
            idx = soup.find_all('tr', 'bbs_list')[i].find('input')['value']
            time.sleep(2)
            driver.execute_script("ContentsDownload.do_down('"+idx+"', 'unioncon', '');return false;")
            time.sleep(2)
            buy_Date = now
            try:
                alert = Alert(driver)
                alert.accept()
                i = i+1
                print('얼럿창 있음 :',i)
            except:
                break

        time.sleep(5)
        pyautogui.hotkey('enter')
        time.sleep(2)
        dis = subprocess.call("taskkill /im FileisDown.exe", shell=True)
        time.sleep(2)

        driver.get('http://cp.fileis.com/')
        time.sleep(2)
        driver.find_element_by_name('vcID').send_keys(admin_id)
        driver.find_element_by_name('vcPwd').send_keys(admin_pw)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="LoginCorner"]/form/table/tbody/tr[1]/td[3]/input').click()
        time.sleep(2)

        driver.get('http://cp.fileis.com/log/purchaseLog.php?aRight=&search=nContentNo&keyword='+idx+'&sDate='+now2+'&eDate='+now2)
        html = driver.find_element_by_xpath('/html/body/table[2]').get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find_all('tr')
        if len(tr) != 1:
            for a in range(1,len(tr)+1):
                buyer = soup.find_all('tr')[a].find_all('td')[5].text.strip()
                if buyer == userId:
                    ACC_Cnt_ID = soup.find_all('tr')[a].find_all('td')[3].text.strip()
                    ACC_Seller = soup.find_all('tr')[a].find_all('td')[4].text.strip()
                    ACC_Cnt_Title = soup.find_all('tr')[a].find_all('td')[6].text.strip()
                    ACC_pay = soup.find_all('tr')[a].find_all('td')[7].text.split('원')[0].replace(",","").strip()
                    ACC_Admin_Date = soup.find_all('tr')[a].find_all('td')[8].text.strip()
                    ACC_Admin_State = 1
                    break
                else:
                    continue
            dateCh1 = buy_Date.split(' ')[0].strip()
            dateCh2 = ACC_Admin_Date.split(' ')[0].strip()
            if dateCh2 != dateCh1:
                ACC_Cnt_ID = None
                ACC_Seller = None
                ACC_Cnt_Title = None
                ACC_pay = None
                ACC_Admin_Date = None
                ACC_Admin_State = 0
        else:
            ACC_Cnt_ID = None
            ACC_Seller = None
            ACC_Cnt_Title = None
            ACC_pay = None
            ACC_Admin_Date = None
            ACC_Admin_State = 0

        data = {
            'ACC_Cnt_ID' : ACC_Cnt_ID,
            'ACC_Seller' : ACC_Seller,
            'ACC_Cnt_Title' : ACC_Cnt_Title,
            'ACC_pay' : ACC_pay,
            'ACC_Admin_Date': ACC_Admin_Date,
            'ACC_Admin_State': ACC_Admin_State
        }
        print(data)

        conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
        try:
            curs2 = conn2.cursor(pymysql.cursors.DictCursor)
            dbResult = insert(conn2,Osp_id,idx,userId,buy_Date,data['ACC_Cnt_ID'],data['ACC_Seller'],data['ACC_Cnt_Title'],data['ACC_pay'],data['ACC_Admin_Date'],data['ACC_Admin_State'])
        except Exception as e:
            print(e)
            pass
        finally :
            conn2.close()

    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("v_fileis 크롤링 시작")
    startCrawling()
    print("v_fileis 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
