# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 01:14:54 2023

@author: yang
"""
import requests
import json

url = "https://data.judicial.gov.tw/jdg/api/Auth"
category = "https://opendata.judicial.gov.tw/data/api/rest/categories"

# 設定請求標頭和輸入內容
headers = {
    "Content-Type": "application/json"
}

payload = {
    "user": "input your username",
    "password": "input your password"
}

json_payload = json.dumps(payload)

# 發送POST請求
response = requests.post(url, headers=headers, data=json_payload)
print(response.status_code)
# 拿token
if response.status_code == 200:
    data = response.json()
    print(data)
    if "Token" in data:
        # 驗證通過，取得token
        token = data["Token"]
        print("驗證通過，Token: ", token)
    elif "error" in data:
        # 驗證失敗
        error_message = data["error"]
        print("驗證失敗: ", error_message)
else:
    print("發生錯誤，狀態碼: ", response.status_code)


# 拿完Token就可以先comment掉，不然會重複取


# (1)取得主題分類清單
#   (1-1)基本查詢:取得全部司法院主題分類清單
#       查詢格式: https://opendata.judicial.gov.tw/data/api/rest/categories
#       查詢條件:無
#       查詢輸出:Jason格式
#  主題分類代碼:categoryNo
#  主題分類名稱:categoryName

categoryUrl = "https://opendata.judicial.gov.tw/data/api/rest/categories"

# 發送GET請求
response = requests.get(categoryUrl)

# 解析回應
if response.status_code == 200:
    data = response.json()
    for category in data:
        category_no = category["categoryNo"]
        category_name = category["categoryName"]
        print("主題分類代碼: ", category_no)
        print("主題分類名稱: ", category_name)
else:
    print("發生錯誤，狀態碼: ", response.status_code)



#   (1-2)進階查詢:指定主題分類代碼取得資料源清單
# 查詢格式: https://opendata.judicial.gov.tw/data/api/rest/categories/{categoryNo}/resources
#       查詢條件:categoryNo主題分類代碼
#       查詢輸出:Jason格式

category_no = "001"  # 替換為您要查詢的主題分類代碼
queryUrl = f"https://opendata.judicial.gov.tw/data/api/rest/categories/{category_no}/resources"

# 發送GET請求
response = requests.get(queryUrl)

# 解析回應
if response.status_code == 200:
    data = response.json()
    for item in data:
        dataset_id = item["datasetId"]
        title = item["title"]
        category_name = item["categoryName"]
        filesets = item["filesets"]
        
        print("資料集Id: ", dataset_id)
        print("資料集名稱: ", title)
        print("主題分類名稱: ", category_name)
        
        for fileset in filesets:
            fileset_id = fileset["fileSetId"]
            resource_format = fileset["resourceFormat"]
            resource_description = fileset["resourceDescription"]
            
            print("資料源Id: ", fileset_id)
            print("檔案格式: ", resource_format)
            print("資源描述: ", resource_description)
            
        print("--------------------------------------")
else:
    print("發生錯誤，狀態碼: ", response.status_code)


# (2)以URL存取資料
#   (2-1)基本查詢
# 查詢格式:https://opendata.judicial.gov.tw/api/FilesetLists/{fileSetId}/file
# 查詢條件:fileSetId資料源Id
# 查詢輸出:檔案資料



fileset_id = "38063"  # 替換為您要查詢的資料源Id
dataUrl = f"https://opendata.judicial.gov.tw/api/FilesetLists/{fileset_id}/file"

# 發送GET請求
response = requests.get(dataUrl)

# 解析回應
if response.status_code == 200:
    file_data = response.content
    # 根據您的需求處理檔案資料
    print(file_data)
else:
    print("發生錯誤，狀態碼: ", response.status_code)
