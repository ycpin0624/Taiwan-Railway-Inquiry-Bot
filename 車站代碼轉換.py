# coding = utf-8
import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip111/view"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'lxml')
stationName = soup.find_all('div', class_='traincode_name1')
stationCode = soup.find_all('div', class_='traincode_code1')

with open('車站代碼.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    spamwriter.writerow(['車站', '代碼'])

    for i in range(len(stationName)):
        spamwriter.writerow([stationName[i].text, stationCode[i].text])
