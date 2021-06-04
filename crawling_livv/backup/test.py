import pymysql,time,datetime
import random

def startCrawling():
    # day = datetime.datetime.now(tz=pytz.utc)
    # Live_num = str(day).split(' ')[1].split('.')[0].replace(':', '').replace('+', '').replace('.', '')
    Live_num = 'Live'+datetime.datetime.now().strftime('%Y%m%d')+str(random.randint(1000, 9999))
    # day = datetime.utcnow()
    print(Live_num)
    # Live_num = day.valueOf()
    # print(Live_num)
    # 1610350016883
    # 2021012248455
    # 0520145692180000
    # 044219522177
    # 2021-01-11 16:26:56


if __name__=='__main__':
    startCrawling()
