from model.service.data_service import DataService

class Vocal:
    file_name = 'vocal_data.json'

    def __init__(self, name_kr, name_origin, debut_date, key):
        self.name_kr = name_kr                              # 가수 이름 한국어
        self.name_origin = name_origin                      # 가수 이름 원어
        self.debut_date = debut_date                        # 가수 데뷔일
        self.key = key

    def save_to_file(self):
        DataService.save_data(Vocal.file_name, self.__dict__)
