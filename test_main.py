import os
import csv
import numpy as np
import pandas as pd
import test_trainQuery
import json

data_input = "8/30 12 15 彰化 台中".split(' ')
date = data_input[0].split('/')
if len(date[0]) != 4:
    date.insert(0, '2021')
if len(date[1]) != 2:
    date[1] = '0' + date[1]
if len(date[2]) != 2:
    date[2] = '0' + date[2]
ride_date = ''.join(date)

start_time = data_input[1] + ':00'
end_time = data_input[2] + ':00'

start_station = data_input[3]
end_station = data_input[4]

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
output_messages = []
alt_text = "查詢成功！"

able_to_booking_file = open(
                'replyMessage/able_to_booking.json', 'r', encoding='utf-8')
able_input_file = able_to_booking_file.read() # 可訂票車次顯示格式

unable_to_booking_file = open(
                'replyMessage/unable_to_booking.json', 'r', encoding='utf-8')
unable_input_file = unable_to_booking_file.read() # 不可訂票車次顯示格式

input_data_count = 0
        
# 產生輸出樣式
with open('trainData.csv', encoding='utf-8') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if(row['訂票'] == '可'): # 可訂票車次
            able_input_data = json.loads(able_input_file)
            able_input_data["body"]["contents"][0]["text"] = row['車種車次']
            able_input_data["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = row['出發時間'] + \
                ' - ' + row['抵達時間']
            able_input_data["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = row['經由']
            able_input_data["footer"]["contents"][0]["action"]["text"] = "booking-" + row['車種車次']

            elements.append(able_input_data)
        else: # 不可訂票車次
            unable_input_data = json.loads(unable_input_file)
            unable_input_data["body"]["contents"][0]["text"] = row['車種車次']
            unable_input_data["body"]["contents"][1]["contents"][0]["contents"][1]["text"] = row['出發時間'] + \
                ' - ' + row['抵達時間']
            unable_input_data["body"]["contents"][1]["contents"][1]["contents"][1]["text"] = row['經由']

            elements.append(unable_input_data)
        
        input_data_count += 1

        if input_data_count == 10:
            output_data = {
                "type": "carousel",
                "contents": elements
            }

            output_messages.append(output_data)
            elements = []
            input_data_count = 0

if input_data_count != 0:
    output_data = {
        "type": "carousel",
        "contents": elements
    }

    output_messages.append(output_data)
    elements = []
    input_data_count = 0

# qureyMessage_file = open(
#     'replyMessage/qureyMessage.json', 'w', encoding='utf-8')
# json.dump(output_data, )
# qureyMessage_file.close()

print(len(output_messages))

print("Test Success!")