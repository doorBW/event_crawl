#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

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

mail_html = "<html><head><body>"+datetime.today().strftime("%Y/%m/%d %H:%M:%S")+"<br>"  # YYYY/mm/dd HH:MM:SS 형태의 시간 출력

mail_html += "<h1>NEWS</h1>"
# for news crawl
req = requests.get("https://okky.kr/articles/news")
html = req.text
soup = BeautifulSoup(html, 'html.parser')
news_titles = soup.select('div#list-article > div.panel > ul > li > div > h5 > a')
news_titles_date = soup.select('div#list-article > div.panel > ul > li > div.list-group-item-author > div > div > div.date-created > span')
for i in range(5):
    mail_html += "<h4><a href='https://okky.kr"+news_titles[i].get('href')+"'>"+news_titles[i].text.strip()+"</a> _ "+news_titles_date[i].text.strip()+"</h4>"
mail_html += "<h3><a href='https://okky.kr/articles/news'>뉴스 관련글 모두 보기</a></h3><br><br>"


mail_html += "<h1>EVENTS</h1>"
# for event crawl
req = requests.get("https://okky.kr/articles/event")
html = req.text
soup = BeautifulSoup(html, 'html.parser')
event_titles = soup.select('div#list-article > div.panel > ul > li > div > h5 > a')
event_titles_date = soup.select('div#list-article > div.panel > ul > li > div.list-group-item-author > div > div > div.date-created > span')
for i in range(3):
    mail_html += "<h4><a href='https://okky.kr"+event_titles[i].get('href')+"'>"+event_titles[i].text.strip()+"</a> _ "+event_titles_date[i].text.strip()+"</h4>"
mail_html += "<h3><a href='https://okky.kr/articles/event'>이벤트 관련글 모두 보기</a></h3>"


mail_html += "</body></head></html>"
print(mail_html)

# open SMTP
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()      # say Hello
smtp.starttls()  # TLS 사용시 필요
smtp.login('doobw@likelion.org', os.getenv('PASSWORD'))
 
# main html
msg = MIMEText(mail_html,'html')
# title
msg['Subject'] = 'OKKY 커뮤니티 News & Event 상위 글'
# from
msg['From'] = os.getenv("FROM")
# to
msg['To'] = os.getenv("TO")
# from / to / msg
smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
 
smtp.quit()

