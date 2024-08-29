import re
import os
import json
import hashlib

def mask_company_names(text, company_names):
    # 회사명과 그 뒤에 붙는 텍스트를 처리하기 위한 정규 표현식 패턴 생성
    pattern = r'(' + '|'.join(re.escape(name) for name in company_names) + r')'
    
    # 회사명을 [MASK]로 대체
    masked_text = re.sub(pattern, "company", text)

    matches = re.findall(pattern, text)
    
    
    print("MASKED WORDS : " , len(matches))
    return masked_text

def save_masked_text(qa_dict, filename ,directory):
    if not os.path.exists(directory):
        os.makedir(directory)

    file_path = os.path.join(directory, filename)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(qa_dict, json_file, ensure_ascii = False, indent = 4)

def remove_duplicate_files(directory):
    # 해시값과 파일명을 저장할 딕셔너리
    file_hashes = {}

    # 디렉토리 내 모든 파일을 순회
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            # 파일 내용 읽기
            with open(file_path, 'rb') as file:
                file_content = file.read()
                # 파일 내용의 해시값 계산 (SHA-256 사용)
                file_hash = hashlib.sha256(file_content).hexdigest()

            # 동일한 해시값이 존재하면 해당 파일 삭제
            if file_hash in file_hashes:
                print(f"Duplicate file found and removed: {filename}")
                os.remove(file_path)
            else:
                # 해시값을 딕셔너리에 저장
                file_hashes[file_hash] = filename

def rename_files_in_order(directory):
    # 파일 목록을 가져와 정렬 (파일 목록은 파일명에 따라 오름차순으로 정렬됨)
    files = sorted(os.listdir(directory))

    # 순차적으로 번호를 붙여가며 파일명 변경
    for idx, filename in enumerate(files, start=1):
        # 파일 경로 생성
        old_file_path = os.path.join(directory, filename)

        # 확장자 분리
        file_ext = os.path.splitext(filename)[1]

        # 새 파일명 생성 (0001, 0002, ...)
        new_filename = f"{idx:05}{file_ext}"
        new_file_path = os.path.join(directory, new_filename)

        # 파일명 변경
        os.rename(old_file_path, new_file_path)
        print(f"Renamed: {filename} -> {new_filename}")

    print("File renaming complete.")

def delete_empty_files(directory):
    # 디렉토리 내 모든 파일을 순회
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # 파일인지 확인하고, 크기가 0인 경우 삭제
        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
            os.remove(file_path)
            print(f"Deleted empty file: {filename}")

    print("Empty file deletion complete.")

def split_to_qa_pairs(text):
    # Remove leading/trailing whitespace and split text into questions
    questions = re.split(r'\d+\.\D', text.strip())[1:]
    
    # Convert to dictionary
    qa_dict = {}
    for i, q in enumerate(questions):
        # Split question and answer by finding the next question number
        parts = re.split(r'(\d+\.\s+)', q, maxsplit=1)
        question = f"{i + 1}. {parts[0].strip()}"
        answer = parts[1].strip() if len(parts) > 1 else ''
        qa_dict[question] = answer
    
    return qa_dict

import re

def parse_text(text):
    # 질문과 대답을 저장할 리스트
    questions_and_answers = []

    # 정규식으로 질문과 대답을 분리
    pattern = re.compile(r"(\d+\.\s.*?)\n(.*?)(?=\n\d+\.|\Z)", re.DOTALL)
    matches = pattern.findall(text)

    for match in matches:
        question, answer = match
        questions_and_answers.append({
            'question': question.strip(),
            'answer': answer.strip()
        })

    return questions_and_answers

