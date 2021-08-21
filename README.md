# 臺鐵列車時刻查詢 LINE 機器人: 以查詢指定日期與車站之列車資料.

![](images/QR.png)

請用 QR Code 掃描並且加入為好友.

## 主要功能:

目前僅支援顯示指定列車資訊，包括車次, 時間, 山海線, 與可否訂票, 並以圖像訊息回應

![](images/trainBot.gif)

訂票功能已開發，往後將陸續上載，且歡迎建議新功能。

## 資料來源:

[臺鐵官網-列車時刻查詢](https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime)

## 目前問題:
- 檔案處理量過大，造成 response time 過長
- 新式樣回應 message Bug: 查詢數目大於10筆將無法顯示
