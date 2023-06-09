from bs4 import BeautifulSoup
import requests
import json
import re

# 爬取網頁
url = "https://law.moeasmea.gov.tw/ailt/modules/forum/details/?topic_id=38333"
r = requests.get(url)
r.encoding = 'utf-8'  # 根據網頁編碼設定，這個例子中是 'utf-8'

# 解析網頁
soup = BeautifulSoup(r.text, "html.parser")


# 提取分類
category = soup.find("div", class_="dwqa-breadcrumbs").find_all("a")[-1].text.strip()

# 提取標題
title = soup.find("h2").text.strip()

# 提取問題
question = soup.find("div", class_="topic_content").find("p").text.strip()
processed_question = re.sub(r"\s+", " ", question)

# 提取回答
answer = soup.find("div", class_="answer-feedback").find("p").text.strip()
processed_answer = re.sub(r"\s+", " ", answer)

# 字典
result = {
    "category": category,
    "title": title,
    "question": processed_question,
    "answer": processed_answer
}
print(result)
