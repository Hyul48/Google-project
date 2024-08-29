import json
import pandas as pd
import glob
import os

# 파일들이 저장된 디렉토리 경로
directory_path = 'C:\TailorCV\Dataset\Thebe_processed'  

# 데이터를 저장할 리스트
combined_data = []

# 디렉토리 내의 모든 파일에 접근
for idx, filename in enumerate(os.listdir(directory_path), start=1):
    if filename.endswith(".json"):
        file_path = os.path.join(directory_path, filename)
        
        # JSON 파일을 읽어서 파싱
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 첫 번째 딕셔너리의 'answer' 추출
            content = data[0]['answer']
            # 새로운 딕셔너리 생성
            combined_data.append({'id': idx, 'content': content})

# 모든 데이터를 하나의 JSON 파일로 저장
output_file = 'combined_output.json'
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(combined_data, outfile, ensure_ascii=False, indent=4)

print(f"모든 데이터를 {output_file}에 저장했습니다.")
