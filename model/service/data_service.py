import os
import json
import time

class DataService:
    @staticmethod
    def load_data(file_name, key):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get(str(key), {})

    @staticmethod
    def save_data(file_name, item):
        file_path = os.path.join('data', file_name)
        data = {}

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

        if item['key'] is None or item['key'] == 0:
            key = DataService.load_data('key_data.json', file_name)
            key = int(key) + 1 if key else 1
            item['key'] = str(key)

            key_file_path = os.path.join('data', 'key_data.json')
            key_data = DataService.get_all_data('key_data.json')
            key_data[file_name] = str(key)

            with open(key_file_path, 'w', encoding='utf-8') as file:
                json.dump(key_data, file, ensure_ascii=False, indent=4)

        data[str(item['key'])] = item

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def delete_data(file_name, key):
        file_path = os.path.join('data', file_name)
        data = DataService.get_all_data(file_name)

        if str(key) in data:
            del data[str(key)]

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_all_keys(file_name):
        data = DataService.get_all_data(file_name)
        return list(data.keys())

    @staticmethod
    def get_all_data(file_name):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def is_key_exist(file_name, key):
        data = DataService.get_all_data(file_name)
        return str(key) in data

    @staticmethod
    def rename_file(file_path, file_title):
        file_dir, file_name = os.path.split(file_path)
        file_base, file_ext = os.path.splitext(file_name)
        timestamp = int(time.time() * 1000)
        new_name = f"{file_title}_{timestamp}{file_ext}"
        new_path = os.path.join(file_dir, new_name)
        os.rename(file_path, new_path)
        return new_path

    @staticmethod
    def get_file_name(class_name):
        return "None" if class_name == "None" else class_name.lower() + '_data.json'