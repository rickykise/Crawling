import urllib.request,re
import pymysql,time,datetime
from commonFun import *
from selenium import webdriver
from selenium.webdriver.common.by import By

def setData(url,num,driver):
    driver.execute_script("window.open('"+url+"');")
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after)
    contents = driver.find_element(By.XPATH,'//*[@id="writeContents"]').text.replace("\n","").replace("\t","").replace("\xa0", "")
    datech = driver.find_element(By.XPATH,'/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td/div[1]').text.replace('\n',' ').replace('\t',' ').strip()
    dateche = datech.split("Date : ")[1].split(" l Hit")[0]
    date = datetime.datetime.strptime(dateche, "%y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M:%S')

    data=None
    info = driver.find_element(By.XPATH,'/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td/div[1]').text.strip().split('l')
    try:
        data = {
            'title' : driver.find_element(By.XPATH,'/html/body/table[1]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[3]/td').text.strip(),
            'url' : url,
            'contents' : setText(contents,0),
            'date': date,
            'writer': '익명',
            'ip': info[0].replace('IP : ','').strip(),
            'board_number': num
        }
        print(data)
    except:
        pass
    finally:
        driver.close()
    return data

def startCrawling(key):
    i = 0;check = True;paramKey = None
    encText = urllib.parse.quote(key)
    link = "http://www.oeker.net/g_search.php#gsc.tab=0&gsc.q="+encText+"#gsc.tab=0&gsc.q="+encText+"&gsc.sort=date&gsc.page="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            print(i,'페이지')
            if i > 10:
                break
            driver.get(link+str(i))
            allEles = driver.find_elements(By.CLASS_NAME, 'gsc-webResult')
            for item in allEles:
                time.sleep(3)
                try:
                    item.find_element(By.CLASS_NAME,'gsc-richsnippet-showsnippet-label').click()
                    infobox = driver.find_elements(By.CLASS_NAME,'gsc-richsnippet-individual-snippet-box')
                    if len(infobox) == 0:
                        continue

                    href = driver.find_element(By.CLASS_NAME,'gsc-richsnippet-popup-box-title-url').text
                    num = href.split("&wr_id=")[1]

                    data = setData(href,num,driver)

                    if data['date'] < datetime.date.today().strftime('%Y-%m-%d'):
                        check = False;break

                    driver.switch_to_window(driver.window_handles[0])
                    if not data: continue
                except Exception as e:
                    print(e)
                    continue
                finally:
                    driver.find_element(By.CLASS_NAME,'gsc-richsnippet-popup-close-button').click()

                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if result is False: continue

                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                try:
                    putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'oeker',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'oeker',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check = False;break
                finally :
                    conn.close()
                    conn2.close()
    except:
        pass
        
    finally:
        driver.quit()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("외방커뮤니티 크롤링 시작")
    for key in dbKey.keys():
        print("키워드 : ",key)
        startCrawling(key)
    print("외방커뮤니티 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
