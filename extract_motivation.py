import json
import glob
import os

def extract_support_motivation(file_pattern):
    # 파일 경로로 접근하여 JSON 파일 불러오기
    files = glob.glob(file_pattern, recursive=True)  # recursive=True로 하위 폴더도 검색
    
    result_dict = {}
    
    # 각 파일을 순회하며 처리
    for file in files:
        print(f"Processing file: {file}")  # 처리 중인 파일 출력
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 파일이 제대로 읽혔는지 확인
                if not isinstance(data, dict):
                    print(f"Skipping file {file}: not a dictionary")
                    continue
                
                # 회사 이름 추출
                company_name = data.get("Company", "Unknown Company")
                
                # 상위 폴더 이름 추출
                folder_name = os.path.basename(os.path.dirname(file))
                
                # 지원 동기에 해당하는 질문 및 답변 찾기
                qna_list = data.get("QnA", [])
                
                # 폴더별로 ID 초기화 (폴더별로 관리)
                if folder_name not in result_dict:
                    result_dict[folder_name] = {
                        "data": [],
                        "id_counter": 1  # 폴더별 ID 초기화
                    }
                
                # 리스트를 순회하며 각 질문을 확인
                for qna in qna_list:
                    question = qna.get("Question", "").strip()
                    
                    # "지원"이라는 단어가 포함되고, "동기" 또는 "이유"가 포함된 질문을 추출
                    if "지원" in question and ("동기" in question or "이유" in question):
                        answer = qna.get("Answer", "").strip()
                        
                        # 결과에 추가 (ID 포함)
                        folder_data = result_dict[folder_name]
                        folder_data["data"].append({
                            "id": folder_data["id_counter"],
                            "company": company_name,
                            "support_motivation": answer
                        })
                        
                        # ID 증가
                        folder_data["id_counter"] += 1
        
        except json.JSONDecodeError as e:
            print(f"Error reading {file}: {e}")
        except Exception as e:
            print(f"Unexpected error in {file}: {e}")
    
    return result_dict

# 경로 지정 (모든 하위 폴더에서 .json 파일 검색)
file_pattern = 'C:/TailorCV/company_data/**/*.json'

# 함수 실행
extracted_data = extract_support_motivation(file_pattern)

# 추출된 데이터를 폴더별로 파일로 저장
for folder_name, folder_content in extracted_data.items():
    # 각 폴더에 맞는 파일 경로 설정
    output_folder = f'C:/TailorCV/company_data/{folder_name}'
    output_path = f'{output_folder}/extracted_support_motivation.json'
    
    # 폴더가 없는 경우 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 폴더별 파일에 데이터 저장
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(folder_content["data"], outfile, ensure_ascii=False, indent=4)

    print(f"데이터가 '{output_path}' 파일로 저장되었습니다.")
