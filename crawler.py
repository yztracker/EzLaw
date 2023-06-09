from bs4 import BeautifulSoup
import requests
import json
import re

# 定義起始和結束的 topic_id 範圍
start_topic_id = 37333
end_topic_id = 38333

# 循環爬取每個 topic_id 的文章
for topic_id in range(start_topic_id, end_topic_id+1):
    # 構造 URL
    url = f"https://law.moeasmea.gov.tw/ailt/modules/forum/details/?topic_id={topic_id}"
    
    # 發送請求並解析網頁
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 提取分類
    category_elem = soup.find("div", class_="dwqa-breadcrumbs")
    category = category_elem.find_all("a")[-1].text.strip() if category_elem else ""
    
    # 提取標題
    title_elem = soup.find("h2")
    title = title_elem.text.strip() if title_elem else ""
    
    # 提取問題
    question_elem = soup.find("div", class_="topic_content")
    question = question_elem.find("p").text.strip() if question_elem else ""
    processed_question = re.sub(r"\s+", " ", question)
    
    # 提取回答
    answer_elem = soup.find("div", class_="answer-feedback")
    answer = answer_elem.find("p").text.strip() if answer_elem else ""
    processed_answer = re.sub(r"\s+", " ", answer)
    
    # 如果 answer 是空白，跳過該項目
    if not answer:
        continue
    
    # 建立字典
    result = {
        "category": category,
        "title": title,
        "question": processed_question,
        "answer": processed_answer
    }
    
    # 將結果保存為 JSON 檔案
    filename = f"{category}.json"
    with open(filename, "a", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
        f.write("\n")

    #續寫模式    
    # filename = f"{category}.json"
    # with open(filename, "a", encoding="utf-8") as f:
    #     json.dump(result, f, ensure_ascii=False)
    #     f.write("\n")

    # 如果結果成功收集，則輸出相應的 topic_id
    if category and title and question and answer:
        print(f"成功爬取 topic_id: {topic_id}")

print("爬取完成並保存為不同的 JSON 檔案")
