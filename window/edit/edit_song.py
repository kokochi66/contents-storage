import os
import shutil
from msilib.schema import ComboBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from model.animation import Animation
from model.song import Song
from model.service.data_service import DataService
from model.vocal import Vocal
from model.word import Word
from model.enum import Genre
from datetime import datetime

from property import Property

class EditSongWindow(QMainWindow):

    data_changed = pyqtSignal()
    CATEGORY_NAMES = ['None', 'Animation']

    def __init__(self):
        super().__init__()

        self.setWindowTitle("노래 추가 페이지")

        self.layout = QVBoxLayout()

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.data_key = 0
        self.setCentralWidget(self.container)

        # 노래 저장을 위한 song 저장 폼
        self.form = QFormLayout()

        # 레이아웃이 없으면 기본 값을 0으로 설정
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Set up animation form
        self.title_kr_input = QLineEdit()
        self.form.addRow("노래 제목 (한글)", self.title_kr_input)

        self.title_origin_input = QLineEdit()
        self.form.addRow("노래 제목 (원어)", self.title_origin_input)

        # 가수 입력용 검색창
        self.search_vocal_layout = QHBoxLayout()  # 검색창에 대한 레이아웃 생성

        self.search_vocal_input = QLineEdit()
        self.search_vocal_input.setPlaceholderText("Search...")
        self.search_vocal_input.returnPressed.connect(self.add_vocal)  # 엔터키 눌렀을 때 검색 기능 연결

        self.search_button = QPushButton("가수 추가")
        self.search_button.clicked.connect(self.add_vocal)  # 검색 버튼 클릭시 검색 기능 연결

        self.data_changed.connect(self.update_completer)

        self.search_vocal_layout.addWidget(self.search_vocal_input)  # 검색창 레이아웃에 추가
        self.search_vocal_layout.addWidget(self.search_button)  # 검색창 레이아웃에 추가
        self.form.addRow(self.search_vocal_layout)

        self.delete_vocal_btn = QPushButton('가수 삭제')
        self.delete_vocal_btn.clicked.connect(self.delete_vocal)
        self.vocal_button_layout = QHBoxLayout()
        self.vocal_button_layout.addWidget(self.delete_vocal_btn)
        self.form.addRow(self.vocal_button_layout)

        self.vocal_list = QListWidget()
        self.vocal_list.setMaximumHeight(50)  # widget의 최대 높이를 설정합니다.
        self.form.addRow("가수", self.vocal_list)
        QApplication.instance().applicationStateChanged.connect(self.on_applicationStateChanged)
        # 추가버튼을 누르면 가수가 추가됨 (일단 피쳐링 구분 없음)

        # Highlight start 입력
        self.highlight_start_input = QSpinBox()
        self.highlight_start_input.setRange(0, 10000)  # 범위 설정(0초 ~ 10000초)
        self.form.addRow("하이라이트 시작 (초)", self.highlight_start_input)

        # Highlight end 입력
        self.highlight_end_input = QSpinBox()
        self.highlight_end_input.setRange(0, 10000)  # 범위 설정(0초 ~ 10000초)
        self.form.addRow("하이라이트 끝 (초)", self.highlight_end_input)

        # Category name 입력
        self.category_name_input = QComboBox()
        self.category_name_input.addItems(self.CATEGORY_NAMES)  # 범주 추가
        self.category_name_input.currentTextChanged.connect(self.on_category_changed)
        self.form.addRow("카테고리 범주", self.category_name_input)

        # Category key 입력
        self.cateogry_key_map = {}
        self.search_category_layout = QHBoxLayout()
        self.search_category_input = QLineEdit()
        self.search_category_input.setPlaceholderText("Search...")
        self.search_category_button = QPushButton("카테고리 추가")
        self.search_category_button.clicked.connect(self.add_category)  # 검색 버튼 클릭시 검색 기능 연결

        self.search_category_layout.addWidget(self.search_category_input)
        self.search_category_layout.addWidget(self.search_category_button)
        self.form.addRow(self.search_category_layout)

        self.delete_category_btn = QPushButton('카테고리 삭제')
        self.delete_category_btn.clicked.connect(self.delete_category)
        self.category_button_layout = QHBoxLayout()
        self.category_button_layout.addWidget(self.delete_category_btn)
        self.form.addRow(self.category_button_layout)

        self.category_list = QListWidget()
        self.category_list.setMaximumHeight(50)
        self.form.addRow("카테고리", self.category_list)

        # Release date 입력
        self.release_date_input = QDateEdit()
        self.release_date_input.setCalendarPopup(True)  # 달력 팝업 활성화
        self.form.addRow("음악 발매일", self.release_date_input)

        # File path 입력
        self.file_path_input = QLineEdit()
        self.file_path_button = QPushButton("파일 업로드")
        self.file_path_button.clicked.connect(self.upload_file)  # 파일 업로드 함수 연결

        self.file_path_layout = QHBoxLayout()
        self.file_path_layout.addWidget(self.file_path_input)
        self.file_path_layout.addWidget(self.file_path_button)
        self.form.addRow("노래파일 경로", self.file_path_layout)

        # 검색어 입력 폼
        self.word_input = QLineEdit()
        self.form.addRow("검색어 키", self.word_input)

        self.add_word_btn = QPushButton('검색어 추가')
        self.add_word_btn.clicked.connect(self.add_word)
        self.delete_word_btn = QPushButton('검색어 삭제')
        self.delete_word_btn.clicked.connect(self.delete_word)
        self.word_button_layout = QHBoxLayout()
        self.word_button_layout.addWidget(self.add_word_btn)
        self.word_button_layout.addWidget(self.delete_word_btn)
        self.form.addRow(self.word_button_layout)

        self.word_list = QListWidget()
        self.word_list.setMaximumHeight(50)  # widget의 최대 높이를 설정합니다.
        self.form.addRow("검색어", self.word_list)

    
        # 저장 및 삭제 버튼 추가
        self.save_btn = QPushButton("저장")
        self.save_btn.clicked.connect(self.save_data)
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_data)  # delete_animation 메소드를 아래에서 정의
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.form.addRow(self.button_layout)

        # Add animation form to the layout
        self.layout.addLayout(self.form)

        # 초기 상태에서는 삭제 버튼을 비활성화합니다.
        self.delete_btn.setVisible(False)
        self.edit_flag = False

    def save_data(self):
        title_kr = self.title_kr_input.text()
        title_origin = self.title_origin_input.text()

        # vocal_keys는 이미 이전에 작성하였습니다.
        vocal_keys = [self.vocal_list.item(i).data(Qt.UserRole) for i in range(self.vocal_list.count())]

        highlight_start = self.highlight_start_input.value() # QSpinBox에서 value() 함수를 이용하여 값을 꺼냅니다.
        highlight_end = self.highlight_end_input.value() # QSpinBox에서 value() 함수를 이용하여 값을 꺼냅니다.

        category_name = self.category_name_input.currentText() # QComboBox에서 currentText() 함수를 이용하여 현재 선택된 텍스트를 꺼냅니다.
        category_file_name = DataService.get_file_name(category_name) # 카테고리 이름을 파일 이름으로 변환

        # QListWidget에서 선택된 카테고리의 key 값을 얻습니다.
        category_keys = [self.category_list.item(i).data(Qt.UserRole) for i in range(self.category_list.count())]

        release_date = self.release_date_input.date().toString(Qt.ISODate) # QDateEdit에서 date() 함수를 이용하여 QDate를 가져오고, toString() 함수를 이용하여 문자열로 변환합니다.

        file_path = self.file_path_input.text()
        file_name = os.path.basename(file_path)  # 파일 경로에서 파일 이름만 추출
        if not self.is_valid_file_name(file_name, title_kr):
            file_path = DataService.rename_file(file_path, title_kr)
    
        data_key = self.data_key

        song_data = Song(
            title_kr=title_kr,
            title_origin=title_origin,
            vocal_keys=vocal_keys,
            highlight_start=highlight_start,
            highlight_end=highlight_end,
            category_name=category_file_name,
            category_keys=category_keys,
            release_date=release_date,
            file_path=file_path,
            key=data_key
        )

        # Save the animation data
        song_data.save_to_file()

        # Get the current list of words
        current_words = [self.word_list.item(i).text() for i in range(self.word_list.count())]
        
        word_data = DataService.get_all_data(Word.file_name)
        for key, word in word_data.items():
            if str(word['data_value']) == str(song_data.key) and str(word['key']) not in current_words:
                DataService.delete_data(Word.file_name, word['key'])

        # Save the updated list of words
        for word in current_words:
            word = Word(
                word,
                Song.file_name,
                song_data.key
            )
            word.save_to_file()
            
        # 알림 창 띄우기
        QMessageBox.information(self, "저장 완료", "저장이 완료되었습니다.")
        
        # 창 닫기
        self.data_changed.emit()
        self.close()
        
    def delete_data(self):
        # animation_data.json에서 해당 애니메이션 데이터 삭제
        DataService.delete_data('animation_data.json', self.animation_data['key'])

        # word_data.json에서 해당 검색어 데이터 삭제
        # 데이터 구조가 적절하다면, 단어 데이터를 한번에 가져와서 각각 삭제합니다.
        word_data = DataService.get_all_data('word_data.json')
        for key, word in word_data.items():
            if word['data_value'] == self.animation_data['key']:
                DataService.delete_data('word_data.json', word['key'])

        # 알림 창 띄우기
        QMessageBox.information(self, "삭제 완료", "삭제가 완료되었습니다.")

        # 데이터 변경 신호를 보내고 창 닫기
        self.data_changed.emit()
        self.close()

    def setData(self, song_data):
        # 기본적인 데이터 설정
        self.data_key = song_data['key']
        self.title_kr_input.setText(song_data['title_kr'])
        self.title_origin_input.setText(song_data['title_origin'])
        self.highlight_start_input.setValue(song_data['highlight_start'])
        self.highlight_end_input.setValue(song_data['highlight_end'])
        self.release_date_input.setDate(QDate.fromString(song_data['release_date'], 'yyyy-MM-dd'))
        self.file_path_input.setText(song_data['file_path'])

        # 가수 정보를 설정
        vocal_data = DataService.get_all_data(Vocal.file_name)  # 해당 경로에 vocal 데이터가 저장되어 있다고 가정합니다.
        for key in song_data['vocal_keys']:
            key_str = str(key)  # 키를 문자열로 변환
            if key_str in vocal_data:
                item = QListWidgetItem(vocal_data[key_str]['name_kr'])  # 'name_kr' 사용
                item.setData(Qt.UserRole, key)
                self.vocal_list.addItem(item)

        # 카테고리 설정
        self.category_name_input.setCurrentText(song_data['category_name'])
        if song_data['category_name'] != "None":
            file_name = song_data['category_name']  # category_name 자체가 파일 이름입니다.
            category_data = DataService.get_all_data(file_name)
            for key in song_data['category_keys']:
                if key in category_data:
                    self.category_list.addItem(category_data[key]['name'])  # 가정: category_data에는 'name'이라는 키가 카테고리 이름을 나타냅니다.

        # 검색어 설정
        word_data = DataService.get_all_data('word_data.json')
        for key, word in word_data.items():
            if word['data_value'] == song_data['key']:
                self.word_list.addItem(word['key'])

        # 데이터가 설정된 경우 삭제 버튼을 활성화
        self.delete_btn.setVisible(True)
        self.song_data = song_data  # 삭제 시 사용하려고 저장해 둡니다.
        self.edit_flag = True

        # 검색 데이터를 세팅하는 update_completer 실행
        self.update_completer()

    def add_vocal(self):
        search_keyword = self.search_vocal_input.text()

        # 데이터 로드 코드 추가...
        word_data = DataService.load_data(Word.file_name, search_keyword)
        if not word_data:
            msg = QMessageBox()
            msg.setWindowTitle("검색 결과 없음")
            msg.setText("검색어를 찾을 수 없습니다.")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            return
        vocal_data = DataService.load_data(word_data['data_name'], word_data['data_value'])

        # 기존에 추가된 항목들과 비교
        for i in range(self.vocal_list.count()):
            if self.vocal_list.item(i).data(Qt.UserRole) == vocal_data['key']:
                QMessageBox.warning(self, "오류", "이미 추가된 가수입니다.")
                return

        # 새 아이템 생성 및 사용자 데이터 설정
        item = QListWidgetItem(vocal_data['name_kr'])
        item.setData(Qt.UserRole, vocal_data['key'])

        # 아이템 추가
        self.vocal_list.addItem(item)

    def delete_vocal(self):
        for item in self.vocal_list.selectedItems():
            self.vocal_list.takeItem(self.vocal_list.row(item))

    def update_completer(self):
        word_data = DataService.get_all_data(Word.file_name)

        # 가수 wordKey 리스트
        vocal_keys = []

        # 카테고리별 word Key 리스트 Map (각 카테고리)
        # 현재는 카테고리는 애니메이션에 한정함
        self.category_key_map = {'Animation': [], 'None': []}

        for key, word in word_data.items():
            data_name = str(word['data_name'])
            if data_name != DataService.get_file_name('None'):
                for category_name in self.CATEGORY_NAMES:
                    if category_name != 'None' and data_name == DataService.get_file_name(category_name):
                        self.category_key_map[category_name].append(word['key'])
            elif data_name == DataService.get_file_name('Vocal'):
                vocal_keys.append(word['key'])

        self.vocal_completer = QCompleter(vocal_keys)  # 자동 완성 제안 단어
        self.vocal_completer.setMaxVisibleItems(10)
        self.search_vocal_input.setCompleter(self.vocal_completer)  # 자동 완성 기능을 QLineEdit에 연결

    def on_category_changed(self, category):
        # 선택된 카테고리에 따라 자동 완성 데이터를 설정합니다.
        self.set_autocompletion_data(category)

        # 이미 추가된 데이터를 모두 지웁니다.
        self.category_list.clear()

    def set_autocompletion_data(self, category):
        # 선택된 카테고리에 따라 자동 완성 데이터를 설정합니다.
        if category in self.category_key_map:
            self.category_completer = QCompleter(self.category_key_map[category])
            self.category_completer.setMaxVisibleItems(10)
            self.search_category_input.setCompleter(self.category_completer)
        else:
            # 선택된 카테고리가 category_key_map에 없을 경우, 자동 완성 기능을 비활성화합니다.
            self.search_category_input.setCompleter(None)

    def add_category(self):
        search_keyword = self.search_category_input.text()

        # 데이터 로드 코드 추가...
        word_data = DataService.load_data(Word.file_name, search_keyword)
        if not word_data:
            msg = QMessageBox()
            msg.setWindowTitle("검색 결과 없음")
            msg.setText("검색어를 찾을 수 없습니다.")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            return
        category_data = DataService.load_data(word_data['data_name'], word_data['data_value'])

        # 기존에 추가된 항목들과 비교
        for i in range(self.category_list.count()):
            if self.category_list.item(i).data(Qt.UserRole) == category_data['key']:
                QMessageBox.warning(self, "오류", "이미 추가된 카테고리 입니다.")
                return

        # 새 아이템 생성 및 사용자 데이터 설정
        item = QListWidgetItem(category_data['title_kr'])
        item.setData(Qt.UserRole, category_data['key'])

        # 아이템 추가
        self.category_list.addItem(item)

    def delete_category(self):
        for item in self.category_list.selectedItems():
            self.category_list.takeItem(self.category_list.row(item))

    def add_word(self):
        word = self.word_input.text()

        # 기존에 추가된 항목들과 비교
        for i in range(self.word_list.count()):
            if self.word_list.item(i).text() == word:
                QMessageBox.warning(self, "오류", "이미 추가된 검색어입니다.")
                return

        # JSON 파일에 키가 이미 존재하는지 확인
        if DataService.is_key_exist('word_data.json', word):
            QMessageBox.warning(self, "오류", "이미 존재하는 검색어입니다.")
            return

        self.word_list.addItem(word)


    def delete_word(self):
        for item in self.word_list.selectedItems():
            self.word_list.takeItem(self.word_list.row(item))

    def upload_file(self):
        # 음악 파일 확장자 목록 (이 부분은 필요에 따라 확장할 수 있습니다)
        music_file_extensions = [".mp3", ".wav", ".flac", ".m4a", ".aac"]

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "노래 파일 업로드", "", "Music Files (*.mp3 *.wav *.flac *.m4a *.aac);;All Files (*)", options=options)

        if file_path:
            # 선택된 파일의 확장자를 검사합니다.
            _, extension = os.path.splitext(file_path)
            if extension.lower() not in music_file_extensions:
                print("지원하지 않는 파일 형식입니다.")
                return

            # 현재 시간(밀리초)으로 새 파일 이름을 생성합니다.
            now = datetime.now()
            current_time_millis = int(now.timestamp() * 1000)
            new_file_name = f"{current_time_millis}{extension}"

            # 파일을 새 위치로 이동시킵니다. (새 파일 이름을 사용합니다.)
            # 이 스크립트 파일의 절대 경로를 가져옵니다.

            destination_dir = os.path.join(Property.root, Song.data_path)
            # 디렉토리가 존재하지 않으면 생성합니다.
            os.makedirs(destination_dir, exist_ok=True)
            print("destination_dir = ", destination_dir)

            destination_path = os.path.join(destination_dir, new_file_name)
            print("destination_path = ", destination_path)

            # 이제 파일을 안전하게 이동할 수 있습니다.
            shutil.move(file_path, destination_path)

            # 파일 경로를 텍스트 입력창에 표시합니다.
            self.file_path_input.setText(destination_path)
        else:
            print("파일 업로드가 취소되었습니다.")

    def on_applicationStateChanged(self, state):
        if state == Qt.ApplicationActive:   # 어플리케이션이 활성화되었을 때
            self.update_completer()

    def closeEvent(self, event):
        # 각 입력 필드를 초기화
        self.title_kr_input.clear()
        self.title_origin_input.clear()

        # 이벤트를 부모 클래스에게 전달하여 창을 닫음
        super().closeEvent(event)
    def is_valid_file_name(self, file_name, title_kr):
        # 파일 이름과 확장자 분리
        base_name, ext = os.path.splitext(file_name)

        # 파일 이름이 title_kr로 시작하는지 확인
        if not base_name.startswith(title_kr):
            return False

        # title_kr 다음의 문자열 추출
        remaining_part = base_name[len(title_kr):]

        # remaining_part가 _millis 형태인지 확인
        if not remaining_part.startswith("_") or not remaining_part[1:].isdigit():
            return False

        return True