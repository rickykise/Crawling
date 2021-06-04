import pymysql,time,datetime
import smtplib
from email.mime.text import MIMEText

def put():
    # sendEmail = "rickykise@naver.com"
    # recvEmail = "develop@unionc.co.kr"
    # password = "duddnchlC81311!"
    #
    # smtpName = "smtp.naver.com" #smtp 서버 주소
    # smtpPort = 587 #smtp 포트 번호
    #
    # text = "매일 내용"
    # msg = MIMEText(text) #MIMEText(text , _charset = "utf8")
    #
    # msg['Subject'] = "이것은 메일제목"
    # msg['From'] = sendEmail
    # msg['To'] = recvEmail
    # print(msg.as_string())
    #
    # s=smtplib.SMTP(smtpName , smtpPort) #메일 서버 연결
    # s.starttls() #TLS 보안 처리
    # s.login(sendEmail , password) #로그인
    # s.sendmail("rickykise1@daum.net", recvEmail, msg.as_string()) #메일 전송, 문자열로 변환하여 보냅니다.
    # s.close() #smtp 서버 연결을 종료합니다.

    sendEmail = "rickykise1@daum.net"
    recvEmail = "rickykise@naver.com"

    smtpName = "smtp.daum.net" #smtp 서버 주소
    smtpPort = 465 #smtp 포트 번호

    text = "매일 내용"
    msg = MIMEText(text) #MIMEText(text , _charset = "utf8")

    msg['Subject'] = "이것은 메일제목"
    msg['From'] = sendEmail
    msg['To'] = recvEmail
    print(msg.as_string())

    s=smtplib.SMTP(smtpName , smtpPort) #메일 서버 연결
    s.starttls() #TLS 보안 처리
    s.login("rickykise1" , "duddnchl1125") #로그인
    s.sendmail(sendEmail, recvEmail, msg.as_string()) #메일 전송, 문자열로 변환하여 보냅니다.
    s.close() #smtp 서버 연결을 종료합니다.

if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    put()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
