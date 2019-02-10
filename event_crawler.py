import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

#load env
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
# Load file from the path.
load_dotenv(dotenv_path)

status = os.getenv('STATUS')
print(status)

# for crawl
req = requests.get("https://okky.kr/articles/event")
html = req.text
soup = BeautifulSoup(html, 'html.parser')
event_titles = soup.select('ul > li > div > h5')

# open SMTP
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()      # say Hello
smtp.starttls()  # TLS 사용시 필요
smtp.login('doobw@likelion.org', os.getenv('PASSWORD'))
 
# main text
msg = MIMEText('본문 테스트 메시지')
# title
msg['Subject'] = '테스트'
# to
msg['To'] = 'qjadn9@naver.com'
# from / to / msg
smtp.sendmail('doobw@likelion.org', 'qjadn9@naver.com', msg.as_string())
 
smtp.quit()


# for title in event_titles:
#     print(title.text)