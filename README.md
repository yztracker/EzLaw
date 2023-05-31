# 法律關係圖

## 免責聲明

本專案僅供參考和教育目的，並不構成法律意見或建議。使用者應自行承擔使用本專案所產生的一切風險和責任。作者和OpenAI不對本專案的準確性、完整性或可靠性提供任何明示或暗示的保證或擔保。使用者在使用本專案時應謹慎行事並遵守相關法律法規。

如有任何法律問題或疑慮，建議請諮詢專業法律顧問或律師以獲取個別建議。

## **專案簡介**
此專案使用旨在研究如何使用ChatGPT配合prompt engineer來製作出各判決書的法律關係圖。

## **如何使用**

1. 使用ChatGPT摘要判決書
2. 使用判決書的摘要生成法律關係
3. 法律關係轉成可視化圖表程式碼 (此專案使用mermaid.js測試 不排除有更多更好的套件)
4. 開啟**`index.html`**檔案。
5. 在瀏覽器中查看概念地圖。

prompt : **幫我摘要還有告訴我他們之間的法律關係**

<img width="413" alt="Untitled" src="https://github.com/yztracker/EzLaw/assets/39402524/dd19a304-f3d9-4d72-af69-a5a3daa8eb7c">

prompt : **幫我用此法律關係配合mermaid.js生成 概念地图（Concept map）的程式碼 (須包含html)**

## **概念地圖**

以下是法律關係的概念地圖，使用Mermaid.js程式碼生成：

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      mermaid.initialize({
        startOnLoad: true
      });
    });
  </script>
</head>
<body>
  <div class="mermaid">
    graph LR
      A[被告] -- 被起訴 --> B[公訴人]
      A -- 被判處 --> C[有期徒刑貳月]
      C -- 可易科罰金 --> D[新臺幣壹仟元折算壹日]
      B -- 提起公訴 --> E[臺灣士林地方檢察署檢察官]
      E -- 負責審查和起訴 --> F[公訴程序]
  </div>
</body>
</html>
```

## **解釋**

- A代表被告，B代表公訴人。
- A被起訴並被判處有期徒刑貳月。
- C表示有期徒刑貳月，並可將其轉換為罰金。
- B是提起公訴的公訴人。
- E代表臺灣士林地方檢察署的檢察官，負責審查和起訴程序（公訴程序）。

## Todo

- [x]  摘要判決書
- [x]  可視化關係圖表
- [ ]  法律關係圖正確性確認
- [ ]  更好的prompt模板
- [ ]  確認最適合的圖表

## **相依性**

此專案使用了Mermaid.js程式庫，該程式庫用於生成概念地圖。

## **注意事項**

請確保您的瀏覽器支援JavaScript，以確保概念地圖能正確顯示。
