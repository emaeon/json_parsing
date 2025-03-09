import json
import os
import re

# 여러 묶음으로 된 json 하나씩 인식하는 함수
def json_dir_list():
    root_path=r'.\\01-1.정식개방데이터\\Training\\02.라벨링데이터\\TL\\'
    json_files_lst=[]
    for root, dirs, files in os.walk(root_path):
        for file in files:
            # print(file)
            if file.endswith('.json'):
                json_files_lst.append(os.path.join(root, file))
    return json_files_lst

# 필요한 key만 추출해서 저장하는 함수
def main(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        
    preprocessed_data = {
        "Dataset" : json_data['Dataset'],
        "data":[
            {
                "db_id" : entry['db_id'],
                "hardness": entry["hardness"],
                "query": entry["query"],
                "utterance": entry["utterance"]
            }
            for entry in json_data['data']
        ]
    }

    # JSON 데이터 저장
    output_dir = '.\\output\\'
    output_path = os.path.join(output_dir, f"preprocessed_{os.path.basename(json_path)}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(preprocessed_data, file, indent=4, ensure_ascii=False)

    print(f"JSON file saved successfully: {output_path}") 


    
if __name__ =='__main__':    
    json_files_lst = json_dir_list()
    for json_path in json_files_lst:  
        main(json_path)  
    
     
'''
{    
    "hardness": 난이도,
    "db_id": DB의 ID, 
    “scheme”:”스키마” 혹은 스키마의 인덱스 ?
    “question”:”질문”,
    “sql”: “질문에 관한 SQL”,
}
'''

'''
	"data": [

		{
			"db_id": "seouldata_healthcare_455",
			"utterance_id": "Wht_0001",
			"hardness": "medium",
			"utterance_type": "BR04",
			"query": "SELECT UPSO_SITE_TELNO, TRDP_AREA FROM SEOUL_PUBLIC_HYGIENE_BIZ WHERE DCB_YMD LIKE '2010%'",
			"utterance": "2010년에 폐업한 영업장의 면적과 소재지 전화번호를 나타내줘",
			"values": [],
			"cols": [
				{
					"token": "영업장의 면적",
					"start": 11,
					"column_index": 8
				},
				{
					"token": "소재지 전화번호",
					"start": 20,
					"column_index": 9
				}
			]
		},
  
'''