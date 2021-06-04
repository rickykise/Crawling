import pymysql,time,datetime

def startCrawling():
    # now = datetime.datetime.now().strftime('%H:%M:%S')
    now = "18:01:01"
    if now > '18:00:00':
        print('6시 넘었어!')
    else:
        print("아직 낮이야!")


if __name__=='__main__':
    start_time = time.time()

    startCrawling()
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
