# 자소서 데이터 마스킹 및 처리 스크립트

이 리포지토리는 특정 디렉토리 내 텍스트 파일에서 회사 이름을 마스킹하고, 질문과 답변 형식으로 변환한 후 JSON 파일로 저장하는 Python 스크립트를 포함하고 있습니다.

## 주요 기능

- **회사 이름 마스킹**: 파일 내 지정된 회사 이름을 마스킹합니다.
- **질문과 답변 분리**: 텍스트를 질문과 답변 형식으로 분리합니다.
- **JSON 저장**: 처리된 데이터를 JSON 형식으로 저장합니다.
- **중복 파일 제거**: 중복된 파일을 자동으로 삭제합니다.
- **빈 파일 삭제**: 내용이 없는 빈 파일을 삭제합니다.
- **파일명 일괄 수정**: 처리된 파일을 순서에 따라 파일명을 수정합니다.

## 요구사항

- Python 3.x
- 필요한 패키지: `re`, `os`, `sys`, `json`

## 설치 및 사용법

1. 리포지토리를 클론합니다.
   ```bash
      git clone https://github.com/yourusername/your-repo.git
      cd your-repo```

2. Dataset 폴더 내부에 pre_processing.py

3. 스크립트의 company_names 리스트에 마스킹하려는 회사 이름을 추가합니다.

   ```python
   company_names = ['삼성 SDS', '삼성']```
   확인은 안해봤지만 세부 사항에서 포괄적인 범주로 넘어가야 할 것 같습니다. ex) ['LG화학', 'LG전자', 'LG']

4. 스크립트의 input_dir와 output_dir 경로를 설정합니다.

   ```python
     input_dir = r'C:\\TailorCV\\Dataset\\삼성
     output_dir = r'C:\\TailorCV\\Dataset\\Thebe_processed
   ```
## 추가 ##
자소서 json파일에서 지원동기만 불러올 수 있게끔 설정 (단, 지원동기가 가장 위에 있어야 함 지원 동기가 첫번째가 아닐 경우 combine_json.py에서 index 수정 필요)
```python
   content = data[0]['answer']
``` 
combine_json.py 실행방법
```python
   directory_path = 'C:\TailorCV\Dataset\Thebe_processed'
```
pre_processing.py 로 생성된 데이터 폴더를 입력 경로로 지정해주기만 하면 combine_json파일 생성됨
