import os
import json

class DataService:
    @staticmethod
    def load_data(file_name, key):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # If the key is in the data, return the associated value
        if str(key) in data:
            return data[str(key)]

        # If the key is not found, return an empty dictionary
        return {}

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

        if item['key'] is None or item['key'] == 0:
            # 키 데이터가 없으면, 새로운 키를 가져옴 (key_data에서 로드)
            # 로드하는 데이터가 비어있다면, 1로 초기화
            key = DataService.load_data('key_data.json', file_name)

            # key_data에 해당 key값이 없었으면 {} 를 가져옴. 즉 {}이면 key_data에 file_name 키값으로 1로 초기화하도록 해야함 "file_name": 1 이 형태로
            if not key:
                key = 1
            else:
                # 아이템의 key가 없다면 key_data에서 다음 key를 가져와서 사용
                item['key'] = key
                key = key + 1

            # 해당 초기화한 데이터가 실제 key_data.json 에 반영되어야 함. 이 저장은 save_data 메소드를 따르지 않고 현재 위치에서 직접 저장함
            key_file_path = os.path.join('data', 'key_data.json')
            key_data = {}
            if os.path.exists(key_file_path):
                try:
                    with open(key_file_path, 'r', encoding='utf-8') as file:
                        key_data = json.load(file)
                except json.JSONDecodeError:
                    # 파일 내용이 JSON 형식이 아닐 경우 빈 딕셔너리를 사용
                    pass
            key_data[file_name] = key
            with open(key_file_path, 'w', encoding='utf-8') as file:
                json.dump(key_data, file, ensure_ascii=False, indent=4)

            # 최종적으로 생성하거나, 가져온 key를 현재 파일의 key로 넣어줌
            item['key'] = key_data[file_name]

        # 기존에 등록된 아이템이면 업데이트, 아니면 새로 추가
        data[item['key']] = item

        # 변경된 데이터를 다시 파일에 저장
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def delete_data(file_name, key):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # If the key is in the data, delete the associated value
        if key in data:
            del data[key]

        # Save the updated data back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
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
    @staticmethod
    def is_key_exist(file_name, key):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return key in data