import json
import os
import re
import time
from tqdm import tqdm

def extract_ddl(sql_content):
    ddl_pattern = r"(CREATE|ALTER|DROP|TRUNCATE|RENAME|COMMENT ON).*?;"
    full_ddl_statements = []
    for match in re.finditer(ddl_pattern, sql_content, re.IGNORECASE | re.DOTALL): 
        #re.DOTALL? .이 줄바꿈 문자를 포함하도록 한다고 함
        #re.IGNORECASE 대소문자구분없음
        full_ddl_statements.append(match.group().strip()) 
        # match.group()은 전체 일치한 문자열을 반환하고, strip()은 앞뒤의 공백을 제거
    return full_ddl_statements

def json_sql_parsing(json_path, sql_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file) #json 가져오기
    except Exception as e :
        print(f"Error loading Json:{e}")
        return False
            
    for query in tqdm(json_data['data']): #json 데이터 내 data value 접근
        db_id = query['db_id'] #data value 내 db_id value 접근
        # SQL 파일 경로 찾기
        sql_file_path = None
        for root, dirs, files in os.walk(sql_path): #sql 데이터가 있는 상위 폴더 루트에서 최하위 까지 탐색
            for file in files: #파일명 모두 출력
                if file == f"{db_id}.sql":  #만약 파일명중 db_id로 명명된 sql 파일이 있다면?              
                    sql_file_path = os.path.join(root, file) #해당 루트의 파일 읽기
                    break #반복 멈추기
            if sql_file_path: #만약 none에서 파일명이 저장되었다면?
                break #반복 멈추기
            
        if sql_file_path: #파일명이 저장되었다면
            # SQL 파일에서 DDL 명령어 추출
            try:
                with open(sql_file_path, 'r', encoding='utf-8') as sql_file: #sql 파일 가져오기
                    sql_content = sql_file.read() #컨텐츠 읽기
                    ddl_statements = extract_ddl(sql_content)  # extract_ddl 함수로 DDL 추출
                    # print('ddl :' , ddl_statements)
                    # JSON 데이터 수정 및 저장
                    query['sql_ddl'] = ddl_statements  # 예: JSON 데이터에 DDL 명령어 추가
            except Exception as e :
                print(f'Error processing SQL file:{e}')
                
    try:
        # JSON 데이터 저장
        output_path = f".\\output\\{json_path}"
        output_dir = os.path.dirname(output_path)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4) 
            print(f"JSON file saved successfully: {output_path}")
    except Exception as e :
        print(f"Error saving Json : {e}")
        return False
    return True

if __name__ == '__main__':
    json_file_path = ".\\01-1.정식개방데이터\\Training\\02.라벨링데이터\\TL\\1. 서울_열린데이터\\01. 보건\\TEXT_NL2SQL_label_seouldata_healthcare.json"
    sql_file_root_path = ".\\01-1.정식개방데이터\\Training\\01.원천데이터\\TS\\1. 서울_열린데이터\\01. 보건\\"    
    start_time = time.time()
    json_sql_parsing(json_file_path, sql_file_root_path)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")