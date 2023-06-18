from model.data_service import DataService


class Word:
    def __init__(self, key, data_name, data_value):
        self.key = key
        self.data_name = data_name
        self.data_value = data_value

    def save_to_file(self):
        DataService.save_data('word_data.json', self.__dict__)