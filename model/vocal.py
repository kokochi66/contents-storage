from model.data_service import DataService


class Vocal:
    def __init__(self, name_kr, name_origin, birth, person_key_list):
        self.name_kr = name_kr                              # 가수 이름 한국어
        self.name_origin = name_origin                      # 가수 이름 원어
        self.birth = birth                                  # 가수 데뷔일
        self.person_key_list = person_key_list              # 가수에 속한 인물
        self.key = name_origin

    def save_to_file(self):
        DataService.save_data('vocal_data.json', self.__dict__)
