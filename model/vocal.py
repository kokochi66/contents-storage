from model.data_service import DataService


class Vocal:
    def __init__(self, name_kr, name_origin, debut_date, key):
        self.name_kr = name_kr                              # 가수 이름 한국어
        self.name_origin = name_origin                      # 가수 이름 원어
        self.debut_date = debut_date                        # 가수 데뷔일
        self.key = key

    def save_to_file(self):
        DataService.save_data('vocal_data.json', self.__dict__)
