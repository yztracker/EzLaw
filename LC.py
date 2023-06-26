from langchain.embeddings import CohereEmbeddings

from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import TextLoader
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from typing import Callable, Dict, List, Optional, Union
from pathlib import Path
import json




# load my data
loader = JSONLoader("../EzLaw/usecase/企業人事制度.json")
documents = loader.load()


#load file from directory
# loader = DirectoryLoader('../EzLaw/usecase/',  show_progress=True, loader_cls=UnstructuredMarkdownLoader)
# documents = loader.load()
print(len(documents))
# load pdf
# loader = PyPDFLoader("./126297.pdf")
# pages = loader.load_and_split()


# split the long text 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, separators=[" ", ",", "\n"])
# texts = []  # 用于存储拆分后的文本

# for index, document in enumerate(documents):
#     print(f"Processing document at index {index}:")
#     print(type(document))
#     print(document)  # 检查 document 的内容

#     try:
#         result = text_splitter.split_documents(document)
#         texts.extend(result)
#     except Exception as e:
#         print(f"Error occurred at index {index}: {e}")
#         # 处理异常，可以选择跳过当前文档继续处理下一个文档，或者进行其他处理

#     print("Finished processing document")


texts = text_splitter.split_documents(documents)

persist_directory = 'lawcases'  

embeddings = CohereEmbeddings(cohere_api_key="")

# db index
db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
db.persist()
# db = None

# db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

retriever = db.as_retriever(search_type= "similarity" , search_kwargs={ "k" : 2 }) 


prompt_template = """       Pretend you are GPT-4 model , Act an encyclopedia of Taiwan law expertise. 
       I will present a legal situation for which you will provide advice and relevant legal provisions, and make it understandable to the general public. 
       Please only provide advice related to this situation. Based on the specific sections from the documentation, 
       also please note that because the document has a lot of contact information like "如有其他問題可來電或線上諮詢，電話諮詢不收費。P.S.在這邊回覆,系統不會通知我們,所以請直接來電喔" etc., please do not mention any contact information
       answer the question only using that information. Please be aware that if there are any updates to the legal provisions, 
       please reference the most current content. Your output must be in Chinese(Tradition). If you are uncertain or the answer is not 
       explicitly written in the documentation, please respond with "I'm sorry, I cannot assist with this."
      


{context}

Question: {question}
Answer in Chinese(Tradition):"""

QA_PROMPT1 = """假設你是GPT-4模型，請你扮演一個精通台灣法律的專家。
現在我們即將參加相關國家考試，我將提供一些法律問題，你需要提供相對應的解答。請只針對這種問題提供建議。答案大部分會在題目的前面如果是選擇題就會是ABCD，根據文檔中內容回答問題，只使用文檔中的資訊。

你的輸出必須是繁體中文(zh-tw)。如果你不確定，或者答案沒有明確寫在文檔中，請回答：“對不起，我無法提供協助。”

上下文: {context}
问题: {question}
请给出答案："""

QA_PROMPT = """假設你是GPT-4模型，請你扮演一個精通台灣法律的專家。
我將提供一個法律情境，你需要提供相關建議和法律規定。請只針對這種情況提供建議。根據文檔中的具體條款回答問題，只使用文檔中的信息。

請注意，如果法律規定有任何更新，請參考最新內容。你的輸出必須是繁體中文(zh-tw)。如果你不確定，或者答案沒有明確寫在文檔中，請回答：“對不起，我無法提供協助。”

上下文: {context}
问题: {question}
请给出答案："""


PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}

llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613")
llm.model_kwargs = {
  'temperature': 0.7,
  'max_tokens': 500,
  # other settings...
}


qa = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs=chain_type_kwargs)

questions = [
  "甲因居留簽證延期申請遭駁回，雖已經提起訴願，惟提起訴願案 2 個月後尚未決定前已收到某市 政府警察局限期離境之命令，惟其仍有繼續居留照顧幼小子女之必要，其依法得提起何種救濟？ ",
]

# 存取陣列元素
for question in questions:


    query = question
    result = qa({"query": query})
    print(result)


    question = result['query']
    answer = result['result']

    formatted_text = f"問題：{question}\n回答：{answer}\n\n" 
    with open('result.txt', 'a', encoding='utf-8') as file:
        file.write(formatted_text)
