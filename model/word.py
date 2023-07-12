from model.data_service import DataService


class Word:
    file_name = 'word_data.json'

    def __init__(self, key, data_name, data_value):
        self.key = key
        self.data_name = data_name
        self.data_value = data_value

    def save_to_file(self):
        DataService.save_data(Word.file_name, self.__dict__)