import smtplib
from email.mime.text import MIMEText

def put():
    fromaddr = "develop@unionc.co.kr"
    toaddr = ["sms@unionc.co.kr", 'siteen@unionc.co.kr', "kdh7342@unionc.co.kr"]
    msg = "test입니다."
    id = "rickykise1"
    password="duddnchl1125"

    smtp = smtplib.SMTP_SSL('smtp.daum.net:465')
    smtp.login(id, password)
    msg = MIMEText(msg)
    msg['Subject'] = "test메세지 입니다.2"
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)
    smtp.sendmail(fromaddr, toaddr, msg.as_string())
    smtp.quit()

if __name__=='__main__':
    print("test 크롤링 시작")
    put()
    print("test 크롤링 끝")
    print("=================================")
