import requests
from bs4 import BeautifulSoup
import json
import os

# 카테고리와 관련된 이름 정의
categories = {
    '10026': '기획 전략',
    '10027': '법무 사무 총무',
    '10028': '인사 HR',
    '10029': '회계 세무',
    '10030': '마케팅 광고 MD',
    '10031': '개발 데이터',
    '10032': '디자인',
    '10033': '물류 무역',
    '10034': '운전 운송 배송',
    '10035': '영업',
    '10036': '고객상담 TM',
    '10037': '금융 보험',
    '10038': '식 음료',
    '10039': '고객서비스 리테일',
    '10040': '엔지니어링 설계',
    '10041': '제조 생산',
    '10042': '교육',
    '10043': '건축 시설',
    '10044': '의료 바이오',
    '10045': '미디어 문화 스포츠',
    '10046': '공공 복지 자'
}

# 기본 URL 설정
base_url = "https://www.jobkorea.co.kr"

def unique_filename(directory, filename):
    """ 기존 파일명이 있을 경우 새로운 파일명 생성 """
    base_name, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_name}_{counter}{extension}"
        counter += 1

    return new_filename

def mask_company_name(text, company_name):
    """ 회사명을 [MASK]로 대체 """
    return text.replace(company_name, "[MASK]")

def crawl_category(category_id, category_name):
    category_folder = os.path.join('company_data', category_name)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    for page in range(1, 50):
        print(f"Processing Category: {category_name}, Page: {page}")
        url = f"{base_url}/Starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&schPart={category_id}&schWork=1&schEduLevel=3&isSaved=1&Page={page}"
        
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        company_tags = soup.find_all('a', href=True)

        if not company_tags:
            print(f"Page {page} is empty, skipping.")
            continue

        company_list = []
        for tag in company_tags:
            name_tag = tag.find('span', class_='titTx')
            if name_tag:
                company_name = name_tag.get_text(strip=True)
                company_link = f"{base_url}{tag['href']}"
                company_list.append({'name': company_name, 'link': company_link})

        for company in company_list:
            print(f"Processing Company: {company['name']}")

            target_response = requests.get(company['link'], headers={'User-Agent': 'Mozilla/5.0'})
            target_soup = BeautifulSoup(target_response.content, 'html.parser')
            qa_list = []

            questions = target_soup.select('dl.qnaLists dt')
            answers = target_soup.select('dl.qnaLists dd')

            for q, a in zip(questions, answers):
                question_text = q.get_text(strip=True)
                answer_text = mask_company_name(a.get_text(strip=True), company['name'])
                qa_list.append({'Question': question_text, 'Answer': answer_text})

            safe_company_name = company['name'].replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
            original_filename = f"{safe_company_name}.json"
            unique_file_name = unique_filename(category_folder, original_filename)
            file_path = os.path.join(category_folder, unique_file_name)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'Company': company['name'],
                    'Link': company['link'],
                    'QnA': qa_list
                }, f, ensure_ascii=False, indent=4)

            print(f"Saved to: {file_path}")

    print(f"Category '{category_name}' data extraction complete.\n")

# 결과를 저장할 폴더 생성
base_output_folder = 'company_data'
if not os.path.exists(base_output_folder):
    os.makedirs(base_output_folder)

# 모든 카테고리에 대해 크롤링 실행
for category_id, category_name in categories.items():
    crawl_category(category_id, category_name)

print("All categories data extraction complete.")
