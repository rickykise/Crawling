import pymysql,time,datetime
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

def put():
     # try:
    # to_email = '"rickykise@naver.com"'
    # fromEmail = 'develop@unionc.co.kr'
    # TitleEmail = '이메일 제목입니다'

    # msg = "\r\n".join([
    #     "From: " + fromEmail,
    #     "To: " + to_email,
    #     "Subject: " + TitleEmail,
    #     "",
    #     "여기에 내용이 들어갑니다"
    # ])

    # msg = '제목 : 메일 보내기 테스트입니다.'
    #
    # ## Daum SMTP
    # conn = SMTP_SSL("smtp.daum.net:465")
    # conn.ehlo()
    #
    # loginId = 'rickykise1'
    # loginPassword = 'duddnchl1125'
    # conn.login(loginId, loginPassword)
    #
    # conn.sendmail(fromEmail, to_email, msg.as_string())
    # conn.close()


    # except Exception as e:
    #     print(str(e))

    # # 세션 생성
    # s = smtplib.SMTP('smtp.daum.net', 465)
    #
    # # TLS 보안 시작
    # s.starttls()
    #
    # # 로그인 인증
    # s.login('rickykise1', 'duddnchl1125')
    #
    # # 보낼 메시지 설정
    # msg = MIMEText('내용 : 본문내용 테스트입니다.')
    # msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'
    #
    # # 메일 보내기
    # s.sendmail("rickykise1@daum.net", "rickykise@naver.com", msg.as_string())
    #
    # # 세션 종료
    # s.quit()

    # 세션 생성
    s = smtplib.SMTP('smtp.daum.net', 465)

    # TLS 보안 시작
    s.starttls()

    # 로그인 인증
    s.login('copyright2232@gmail.com', 'wvwjrmvvpiaiveus')

    # 보낼 메시지 설정
    msg = MIMEText('내용 : 본문내용 테스트입니다.')
    msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'

    # 메일 보내기
    s.sendmail("rickykise1@daum.net", "rickykise@naver.com", msg.as_string())

    # 세션 종료
    s.quit()

if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    put()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
