from model.data_service import DataService


class Song:
    file_name = 'song_data.json'
    def __init__(self, title_kr, title_origin, vocal_key, highlight_start, highlight_end, category_name, category_key, release_date, file_path, key):
        self.title_kr = title_kr                            # 노래 한국어 제목 String
        self.title_origin = title_origin                    # 노래 원어 제목 String
        self.vocal_key = vocal_key                          # 노래 가수 key
        self.highlight_start = highlight_start              # 노래 하이라이트 Number           
        self.highlight_end = highlight_end                  # 노래 하이라이트 Number      
        self.category_name = category_name                  # 카테고리 범주 String
        self.category_key = category_key                    # 카테고리 key String
        self.release_date = release_date                    # 음악 발매일 String
        self.file_path = file_path                          # 노래파일 경로
        self.key = key                             # 검색어용 key String

    def save_to_file(self):
        DataService.save_data(Song.file_name, self.__dict__)
