from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import os
import csv
import numpy as np
import pandas as pd


def querybytime(start_station, end_station, option, ride_date, start_or_endTime,
                start_time, end_time, train_type_list, early_bird_button, gobytime_data):
    gobytime_chrome = webdriver.Chrome(
        './chromedriver', chrome_options=options)
    gobytime_chrome.get(
        "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")  # 依時刻

    startStation = gobytime_chrome.find_element_by_id('startStation')  # 出發站
    endStation = gobytime_chrome.find_element_by_id('endStation')  # 抵達站
    option_btn = gobytime_chrome.find_elements_by_xpath(
        '//*[@id="queryForm"]/div[1]/div[1]/div[5]/div[2]/label' + '[' + option + ']')  # 轉乘條件

    rideDate = gobytime_chrome.find_element_by_id('rideDate')  # 日期
    startOrEndTime = gobytime_chrome.find_element_by_id(
        'startOrEndTime' + start_or_endTime)  # 查詢條件
    startTime = gobytime_chrome.find_element_by_id('startTime')  # 時段起
    endTime = gobytime_chrome.find_element_by_id('endTime')  # 時段迄

    trainTypeList = gobytime_chrome.find_element_by_xpath(
        '//*[@id="queryForm"]/div[1]/div[3]/div[1]/div[2]/label' + '[' + train_type_list + ']')  # 車種

    earlyBirdButton = gobytime_chrome.find_element_by_xpath(
        '//*[@id="queryForm"]/div[1]/div[3]/div[2]/div[2]/label')  # 限定早享車次(優惠)

    startStation.send_keys(start_station)
    endStation.send_keys(end_station)
    option_btn[0].click()
    rideDate.send_keys(ride_date)
    startOrEndTime.click()
    startTime.send_keys(start_time)
    endTime.send_keys(end_time)
    trainTypeList.click()

    if early_bird_button == 1:
        earlyBirdButton.click()

    submit = gobytime_chrome.find_element_by_xpath(
        '//*[@id="queryForm"]/div[1]/div[3]/div[3]/input')  # 查詢
    submit.submit()

    gobytime_soup = BeautifulSoup(gobytime_chrome.page_source, 'lxml')
    gobytime_html = gobytime_soup.find_all('tr', class_='trip-column')

    for data in gobytime_html:
        dict = {}
        train_number = data.find('a').text
        dict['train_number'] = train_number
        location = data.find_all('span', class_='location')
        dict['from'] = location[0].text
        dict['to'] = location[1].text
        imformation = data.find_all('td')
        dict['departure_time'] = imformation[1].text
        dict['arrive_time'] = imformation[2].text
        dict['take_time'] = imformation[3].text
        dict['type'] = imformation[4].text
        dict['audlt_ticket'] = imformation[6].find('span').text
        dict['child_ticket'] = imformation[7].find('span').text
        dict['senior_ticket'] = imformation[8].find('span').text
        if train_number[0:2] != '區間':
            dict['booking'] = '可'
        else:
            dict['booking'] = ''
        gobytime_data.append(dict)

    gobytime_chrome.quit()


# 查詢列車時刻
options = Options()
options.add_argument("--disable-notifications")

start_station = input('')
end_station = input('抵達站：')
ride_date = input('日期：(YYYY/MM/DD)')
start_or_endTime = input('時段起迄：(1. 查詢出發時間/2. 查詢抵達時間)')
start_time = input('時間起：(HH:MM)')
end_time = input('時間迄：(HH:MM)')

# start_station = '彰化'
# end_station = '新竹'
# ride_date = '2021/02/20'
# start_or_endTime = '1'
# start_time = '07:00'
# end_time = '12:00'
option = '1'
early_bird_button = 2
gobytime_data = []

start_station = start_station.replace('台', '臺', 1)
end_station = end_station.replace('台', '臺', 1)
with open('車站代碼.csv', newline='') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if row['車站'] == start_station:
            start_station = row['代碼']
        if row['車站'] == end_station:
            end_station = row['代碼']

train_type_list = str(1)
querybytime(start_station, end_station, option, ride_date, start_or_endTime,
            start_time, end_time, train_type_list, early_bird_button, gobytime_data)


with open('指定列車資料.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    spamwriter.writerow(
        ['車種車次', '出發站', '抵達站', '日期', '始發站', '終點站', '出發時間', '抵達時間', '行駛時長', '經由', '全票', '孩童票', '敬老票', '訂票'])

    for data in gobytime_data:
        spamwriter.writerow([data['train_number'], start_station, end_station, ride_date, data['from'], data['to'], data['departure_time'], data['arrive_time'],
                             data['take_time'], data['type'], data['audlt_ticket'], data['child_ticket'], data['senior_ticket'], data['booking']])
