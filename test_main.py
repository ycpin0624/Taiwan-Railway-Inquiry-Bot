import os
import csv
import numpy as np
import pandas as pd
import test_trainQuery
import json

data_input = "8/28 早 彰化 台南".split(' ')
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
unable_element = []

able_to_booking_file = open(
                'replyMessage/able_to_booking.json', 'r', encoding='utf-8')
able_input_file = able_to_booking_file.read()

unable_to_booking_file = open(
                'replyMessage/unable_to_booking.json', 'r', encoding='utf-8')
unable_input_file = unable_to_booking_file.read()
unable_input_data = json.loads(unable_input_file)
unable_to_booking_file.close() # 不可訂票車次顯示父格式

unable_element_file = open('replyMessage/unable_element.json', 'r', encoding='utf-8')
unable_element_input_file = unable_element_file.read()
unable_element_data = json.loads(unable_element_input_file) 
unable_element_file.close() # 不可訂票車次顯示子格式

unable_input_data_count = 0
        
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

able_to_booking_file.close() # 可訂票車次顯示格式

# 產生輸出樣式            
# with open('trainData.csv', encoding='utf-8') as csvfile:
#     rows = csv.DictReader(csvfile)
#     for row in rows: 
#         if(row['訂票'] != '可'): # 不可訂票車次
#             unable_element_data["text"] = row['車種車次']
#             unable_element_data["contents"][1]["contents"][0]["contents"][1]["text"] = row['出發時間'] + \
#                 ' - ' + row['抵達時間']
#             unable_element_data["contents"][1]["contents"][1]["contents"][1]["text"] = row['經由']

#             unable_element.append(unable_element_data)
#             unable_input_data_count += 1
            
#             if unable_input_data_count == 3:
#                 unable_input_data["body"] = unable_element
#                 elements.insert(0, unable_input_data)

#                 unable_input_data_count == 0
#                 unable_element = []

# if unable_input_data_count != 3:
#     unable_input_data["body"] = unable_element
#     elements.insert(0, unable_input_data)

#     unable_input_data_count == 0
#     unable_element = []

output_data = {
    "type": "carousel",
    "contents": elements
}

qureyMessage_file = open(
    'replyMessage/qureyMessage.json', 'w', encoding='utf-8')

json.dump(output_data, qureyMessage_file)

qureyMessage_file.close()

print("Test Success!")