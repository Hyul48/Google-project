"""import os
import shutil
import glob

def move_and_rename_files(src_base_folder, dest_folder):
    # 모든 하위 폴더 내의 json 파일 찾기
    file_pattern = os.path.join(src_base_folder, '**', 'extracted_support_motivation.json')
    files = glob.glob(file_pattern, recursive=True)
    
    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # 각 파일을 순회하며 새로운 폴더로 이동 및 이름 변경
    for file in files:
        # 원래 있던 폴더명 추출 (상위 폴더명)
        folder_name = os.path.basename(os.path.dirname(file))
        
        # 새 파일 이름 설정: 폴더명_extracted_support_motivation.json
        new_file_name = f"{folder_name}_extracted_support_motivation.json"
        
        # 목적지 경로 설정
        dest_path = os.path.join(dest_folder, new_file_name)
        
        # 파일 복사 (이동할 경우 shutil.move 사용 가능)
        shutil.copy(file, dest_path)
        print(f"Moved: {file} -> {dest_path}")

# 원본 폴더 (현재 데이터가 있는 폴더 경로)
src_base_folder = 'C:/TailorCV/company_data'

# 파일을 옮길 목적지 폴더
dest_folder = 'C:/TailorCV/JSON'

# 파일 이동 및 이름 변경 함수 실행
move_and_rename_files(src_base_folder, dest_folder)
"""

import json
import glob
import os

def merge_non_development_files_with_new_ids(src_base_folder, exclude_folder_name, output_file):
    # 모든 하위 폴더 내의 json 파일 찾기
    file_pattern = os.path.join(src_base_folder, '**', 'extracted_support_motivation.json')
    files = glob.glob(file_pattern, recursive=True)
    
    merged_data = []
    new_id_counter = 1  # 새로운 ID를 부여하기 위한 카운터
    
    # 각 파일을 순회하며 데이터 통합 (제외할 폴더는 처리하지 않음)
    for file in files:
        folder_name = os.path.basename(os.path.dirname(file))
        
        if folder_name == exclude_folder_name:
            print(f"Skipping folder: {folder_name}")
            continue
        
        print(f"Processing file: {file}")
        
        # JSON 파일 읽기
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 각 데이터 항목에 새로운 ID 부여
                for entry in data:
                    entry['id'] = new_id_counter  # 기존 id를 무시하고 새 ID 할당
                    new_id_counter += 1
                    merged_data.append(entry)  # 데이터를 통합 리스트에 추가
                
        except json.JSONDecodeError as e:
            print(f"Error reading {file}: {e}")
        except Exception as e:
            print(f"Unexpected error in {file}: {e}")
    
    # 통합된 데이터를 하나의 JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, ensure_ascii=False, indent=4)
    
    print(f"통합된 데이터가 '{output_file}' 파일로 저장되었습니다.")

# 원본 폴더 (현재 데이터가 있는 폴더 경로)
src_base_folder = 'C:/TailorCV/company_data'

# 제외할 폴더명 ('개발 데이터' 제외)
exclude_folder_name = '개발 데이터'

# 통합된 데이터를 저장할 경로
output_file = 'C:/TailorCV/JSON/merged_non_development_with_new_ids.json'

# 함수 실행
merge_non_development_files_with_new_ids(src_base_folder, exclude_folder_name, output_file)
