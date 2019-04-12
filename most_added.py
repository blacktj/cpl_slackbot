#yahoo transaction trends
import pandas as pd
import smtplib
import requests

from bs4 import BeautifulSoup
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

today = date.today()
yesterday = today - timedelta(1)

gmail_user = '---'
gmail_password = '---'

def remove_non_ascii_1(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

url = 'https://baseball.fantasysports.yahoo.com/b1/buzzindex?date=' + str(yesterday) + '&pos=ALL&src=combined&bimtab=A&sort=BI_A&sdir=1'
data = requests.get(url)

content = data.text
soup = BeautifulSoup(''.join(content), "lxml")

most_added = []
for tables in soup.find_all('tbody'):
    for row in tables.find_all('tr'):
        detail = (row.get_text(strip=True, separator='|').split('|'))
        if detail[0] == 'New Player Note' or detail[0] == 'Player Note' or detail[0] == 'No new player Notes' and len(detail) > 3:
            temp = [remove_non_ascii_1(detail[1]),detail[2],detail[len(detail)-4],detail[len(detail)-3],detail[len(detail)-2],detail[len(detail)-1]]
            most_added.append(temp)
        else:
            next
df_most_added_today = pd.DataFrame(most_added, columns = ['player_name', 'team_pos', 'drops', 'adds', 'trades', 'total_moves'])


sent_from = gmail_user
to = '---'
subject = 'Most Added Players Today'
email = "{df}"
text = email.format(df=df_most_added_today.to_html())


msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = sent_from
msg['To'] = to
part1 = MIMEText(text, 'html')
msg.attach(part1)

# Send the message via local SMTP server.
s = smtplib.SMTP("smtp.gmail.com:587")
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.starttls()
s.login(gmail_user, gmail_password)
s.sendmail(sent_from, to, msg.as_string())
s.quit()
