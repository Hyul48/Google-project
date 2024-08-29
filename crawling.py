import numpy as numpy
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
from datetime import date
from tqdm import trange

#   page_no = 1
url = "https://www.jobkorea.co.kr/Starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&schPart=10027&schWork=1&schEduLevel=3&isSaved=1&Page=1"

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})

soup = bs(response.content, 'html.parser')
target_link = soup.find('span', class_='titTx', text="한국증권금융(주)").parent['href']


full_url = f"https://www.jobkorea.co.kr{target_link}"
# print(full_url)

target_respose = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
target_soup = bs(target_respose.text, 'html.parser')


#회사명
company_tag = target_soup.find('a', title='기업 홈 이동')
company_name = company_name = company_tag.get_text(strip=True)
print(company_name)

# 질문과 답변을 담을 리스트
qa_list = []

# <dl> 태그 안의 모든 <dt>와 <dd> 태그를 찾기
questions = target_soup.select('dl.qnaLists dt')
answers = target_soup.select('dl.qnaLists dd')

# 각 질문과 답변을 순회하면서 텍스트 추출
for q, a in zip(questions, answers):
    question_text = q.find('span', class_='tx').get_text(strip=True)
    answer_text = a.find('div', class_='tx').get_text(strip=True)
    qa_list.append({'Question': question_text, 'Answer': answer_text})

# 결과 출력
for i, qa in enumerate(qa_list, 1):
    print(f"Q{i}: {qa['Question']}")
    print(f"A{i}: {qa['Answer']}\n")