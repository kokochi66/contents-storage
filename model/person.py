from model.data_service import DataService


class Person:
    def __init__(self, name_kr, name_origin, birth, nation):
        self.name_kr = name_kr                              # 인물 이름 한국어
        self.name_origin = name_origin                      # 인물 이름 원어
        self.birth = birth                                  # 인물 생년월일
        self.nation = nation                                # 인물 국적
        self.key = name_origin

    def save_to_file(self):
        DataService.save_data('person_data.json', self.__dict__)
