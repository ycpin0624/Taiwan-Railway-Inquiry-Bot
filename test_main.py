import os
import csv
import numpy as np
import pandas as pd
import test_trainQuery
import json

data_input = "8/22 晚 台北 台中".split(' ')
date = data_input[0].split('/')
if len(date[0]) != 4:
    date.insert(0, '2021')
if len(date[1]) != 2:
    date[1] = '0' + date[1]
if len(date[2]) != 2:
    date[2] = '0' + date[2]
ride_date = ''.join(date)

if data_input[1] == '早':
    start_time = '00:01'
    end_time = '12:00'
elif data_input[1] == '中':
    start_time = '12:00'
    end_time = '18:00'
elif data_input[1] == '晚':
    start_time = '18:00'
    end_time = '23:59'
else:
    start_time = '00:01'
    end_time = '23:59'

start_station = data_input[2]
end_station = data_input[3]

test_trainQuery.trainQuery(start_station, end_station,
                    ride_date, start_time, end_time)

record_a = []
record_a.append({
"type": "text",
"text": "非訂位車次",
"weight": "bold",
"size": "xl",
"color": "#0066cc"
})

elements = []

# 產生輸出樣式
with open('trainData.csv', encoding='utf-8') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if(row['訂票'] == '可'): # 可訂票車次
            able_to_booking_file = open(
                'replyMessage/able_to_booking.json', 'r', encoding='utf-8')
            input_file = able_to_booking_file.read()
            input_data = json.loads(input_file)

            input_data["body"]["contents"][0]["text"] = row['車種車次']
            input_data["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = row['出發時間'] + \
                ' - ' + row['抵達時間']
            input_data["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = row['經由']
            input_data["footer"]["contents"][0]["action"]["text"] = "booking-" + row['車種車次']

            elements.append(input_data)
            able_to_booking_file.close()
        else: # 不可訂票車次
            unable_to_booking_file = open(
                'replyMessage/unable_to_booking.json', 'r', encoding='utf-8')
            input_file = unable_to_booking_file.read()
            input_data = json.loads(input_file)

            input_data["body"]["contents"][0]["text"] = row['車種車次']
            input_data["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = row['出發時間'] + \
                ' - ' + row['抵達時間']
            input_data["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = row['經由']

            elements.append(input_data)
            unable_to_booking_file.close()

# flexMessage_a_file = open(
#     'replyMessage/flexMessage_a.json', 'r', encoding='utf-8')
# input_file = flexMessage_a_file.read()
# input_data = json.loads(input_file)
# input_data["body"]["contents"] = elements

# elements.insert(0, input_data)

output_data = {
    "type": "carousel",
    "contents": elements
}

qureyMessage_file = open(
    'replyMessage/qureyMessage.json', 'w', encoding='utf-8')

json.dump(output_data, qureyMessage_file)

qureyMessage_file.close()
