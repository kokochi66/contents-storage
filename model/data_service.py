import os
import json

class DataService:
    @staticmethod
    def save_data(file_name, item):
        # 파일 경로
        file_path = os.path.join('data', file_name)

        data = {}  # data를 먼저 빈 딕셔너리로 초기화

        # 파일이 존재하면 기존 데이터 로드
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                # 파일 내용이 JSON 형식이 아닐 경우 빈 딕셔너리를 사용
                pass

        # 기존에 등록된 아이템이면 업데이트, 아니면 새로 추가
        data[item['key']] = item

        # 변경된 데이터를 다시 파일에 저장
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_data(file_name, key):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # If the key is in the data, return the associated value
        if key in data:
            return data[key]

        # If the key is not found, return an empty dictionary
        return {}

    @staticmethod
    def delete_data(file_name, key):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # If the key is in the data, delete the associated value
        if key in data:
            del data[key]

        # Save the updated data back to the file
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
    @staticmethod
    def get_all_keys(file_name):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return list(data.keys())
    @staticmethod
    def get_all_data(file_name):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data