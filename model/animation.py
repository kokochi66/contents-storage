from model.data_service import DataService


class Animation:
    file_name = 'animation_data.json'

    def __init__(self, title_kr, title_origin, genre, director, airing_period, production_company, key):
        self.title_kr = title_kr
        self.title_origin = title_origin
        self.genre = genre
        self.director = director
        self.airing_period = airing_period
        self.production_company = production_company
        self.key = key  # key 필드 추가

    def save_to_file(self):
        DataService.save_data(Animation.file_name, self.__dict__)
