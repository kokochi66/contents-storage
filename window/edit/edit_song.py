from msilib.schema import ComboBox
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QApplication, QListWidget, QMessageBox, QHBoxLayout, QListWidgetItem, QCompleter
from PyQt5.QtCore import Qt, pyqtSignal
from model.animation import Animation
from model.song import Song
from model.data_service import DataService
from model.vocal import Vocal
from model.word import Word
from model.enum import Genre

class EditSongWindow(QMainWindow):
    data_changed = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setWindowTitle("노래 추가 페이지")

        self.layout = QVBoxLayout()

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        # 노래 저장을 위한 song 저장 폼
        self.song_form = QFormLayout()

        # 레이아웃이 없으면 기본 값을 0으로 설정
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Set up animation form
        self.title_kr_input = QLineEdit()
        self.song_form.addRow("노래 제목 (한글)", self.title_kr_input)

        self.title_origin_input = QLineEdit()
        self.song_form.addRow("노래 제목 (원어)", self.title_origin_input)

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
        self.song_form.addRow(self.search_vocal_layout)

        self.delete_vocal_btn = QPushButton('가수 삭제')
        self.delete_vocal_btn.clicked.connect(self.delete_vocal)
        self.vocal_button_layout = QHBoxLayout()
        self.vocal_button_layout.addWidget(self.delete_vocal_btn)
        self.song_form.addRow(self.vocal_button_layout)

        self.vocal_list = QListWidget()
        self.vocal_list.setMaximumHeight(50)  # widget의 최대 높이를 설정합니다.
        self.song_form.addRow("가수", self.vocal_list)

        QApplication.instance().applicationStateChanged.connect(self.on_applicationStateChanged)

        # 추가버튼을 누르면 가수가 추가됨 (일단 피쳐링 구분 없음)

        # 하이라이트 시간(s) : 초 기준으로 몇초~ 몇초까지
        # 하이라이트 종료시간(e) : 0 <= s < e (노래 종료시간보다 큰지는 체크하지 않음 => 따로 가져와서 로직관리를 하기 번거로움)

        # 카테고리 범주는 select로 선택
        # 카테고리 key는 검색하여 추가

        # 발매일 (날짜 형식으로 입력 => 달력 입력 폼 가져오기)

        # 파일 업로드 (지정한 파일을 file 폴더로 가져옴) => 업로드한 파일 경로를 가져와서 저장

        # 저장 및 삭제 버튼 추가
        # self.save_btn = QPushButton("저장")
        # self.save_btn.clicked.connect(self.save_animation)
        # self.delete_btn = QPushButton("삭제")
        # self.delete_btn.clicked.connect(self.delete_animation)  # delete_animation 메소드를 아래에서 정의
        # self.button_layout = QHBoxLayout()
        # self.button_layout.addWidget(self.save_btn)
        # self.button_layout.addWidget(self.delete_btn)
        # self.song_form.addRow(self.button_layout)

        # Add animation form to the layout
        self.layout.addLayout(self.song_form)

        # 초기 상태에서는 삭제 버튼을 비활성화합니다.
        # self.delete_btn.setVisible(False)
        self.edit_flag = False

    def setData(self, song_data):
        self.title_kr_input.setText(song_data['title_kr'])
        self.title_origin_input.setText(song_data['title_origin'])
        # self.director_input.setText(animation_data['director'])
        # self.production_company_input.setText(animation_data['production_company'])

        # # 장르와 방영기간, 검색어는 리스트 형태로 저장되어 있으므로, 각각의 요소를 리스트 위젯에 추가해주는 작업이 필요합니다.
        # for genre in animation_data['genre']:
        #     self.airing_genre_list.addItem(genre)
        
        # for period in animation_data['airing_period']:
        #     self.airing_period_list.addItem(period)

        # # Word 데이터에서 해당 애니메이션에 해당하는 검색어 리스트를 가져와서 airing_word_list에 추가
        # word_data = DataService.get_all_data('word_data.json')
        # for key, word in word_data.items():
        #     if word['data_value'] == animation_data['title_origin']:
        #         self.airing_word_list.addItem(word['key'])

        # # 데이터가 설정된 경우에만 삭제 버튼을 활성화합니다.
        # self.delete_btn.setVisible(True)

        # self.animation_data = animation_data  # 삭제 시 사용하려고 저장해 둡니다.
        self.edit_flag = True

        # 검색 데이터를 세팅하는 update_completer 실행
        self.update_completer()

    # def add_period(self):
    #     year = self.year_input.currentText()
    #     quarter = self.quarter_input.currentText()
    #     period = f"{year}-{quarter}"

    #     # 기존에 추가된 항목들과 비교
    #     for i in range(self.airing_period_list.count()):
    #         if self.airing_period_list.item(i).text() == period:
    #             QMessageBox.warning(self, "오류", "이미 추가된 분기입니다.")
    #             return
    #     self.airing_period_list.addItem(period)


    # def delete_period(self):
    #     for item in self.airing_period_list.selectedItems():
    #         self.airing_period_list.takeItem(self.airing_period_list.row(item))

    # def add_word(self):
    #     word = self.word_input.text()

    #     # 기존에 추가된 항목들과 비교
    #     for i in range(self.airing_word_list.count()):
    #         if self.airing_word_list.item(i).text() == word:
    #             QMessageBox.warning(self, "오류", "이미 추가된 검색어입니다.")
    #             return

    #     # JSON 파일에 키가 이미 존재하는지 확인
    #     if DataService.is_key_exist('word_data.json', word):
    #         QMessageBox.warning(self, "오류", "이미 존재하는 검색어입니다.")
    #         return

    #     self.airing_word_list.addItem(word)


    # def delete_word(self):
    #     for item in self.airing_word_list.selectedItems():
    #         self.airing_word_list.takeItem(self.airing_word_list.row(item))

    # def delete_animation(self):
    #     # animation_data.json에서 해당 애니메이션 데이터 삭제
    #     DataService.delete_data('animation_data.json', self.animation_data['title_origin'])

    #     # word_data.json에서 해당 검색어 데이터 삭제
    #     # 데이터 구조가 적절하다면, 단어 데이터를 한번에 가져와서 각각 삭제합니다.
    #     word_data = DataService.get_all_data('word_data.json')
    #     for key, word in word_data.items():
    #         if word['data_value'] == self.animation_data['title_origin']:
    #             DataService.delete_data('word_data.json', word['key'])

    #     # 알림 창 띄우기
    #     QMessageBox.information(self, "삭제 완료", "삭제가 완료되었습니다.")

    #     # 데이터 변경 신호를 보내고 창 닫기
    #     self.data_changed.emit()
    #     self.close()

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
                QMessageBox.warning(self, "오류", "이미 추가된 장르입니다.")
                return

        self.vocal_list.addItem(vocal_data['key'])

    def delete_vocal(self):
        for item in self.vocal_list.selectedItems():
            self.vocal_list.takeItem(self.vocal_list.row(item))

    def update_completer(self):
        print('update_completer')
        word_data = DataService.get_all_data(Word.file_name)

        # 가수 wordKey 리스트
        vocal_keys = []

        # 카테고리별 word Key 리스트 Map (각 카테고리)
        # 현재는 카테고리는 애니메이션에 한정함
        category_key_map = {'animation': [],}

        for key, word in word_data.items():
            print('word = ', word)
            if str(word['data_name']) == str(Animation.file_name):
                category_key_map['animation'].append(word['key'])
            elif str(word['data_name']) == str(Vocal.file_name):
                vocal_keys.append(word['key'])

        self.vocal_completer = QCompleter(vocal_keys)  # 자동 완성 제안 단어
        self.vocal_completer.setMaxVisibleItems(10)
        self.search_vocal_input.setCompleter(self.vocal_completer)  # 자동 완성 기능을 QLineEdit에 연결

        # self.category_completer = QCompleter(vocal_keys)  # 자동 완성 제안 단어
        # self.category_completer.setMaxVisibleItems(10)
        # self.search_category_input.setCompleter(self.category_completer['animation'])  # 자동 완성 기능을 QLineEdit에 연결

    def on_applicationStateChanged(self, state):
        if state == Qt.ApplicationActive:   # 어플리케이션이 활성화되었을 때
            self.update_completer()

    def closeEvent(self, event):
        # 각 입력 필드를 초기화
        self.title_kr_input.clear()
        self.title_origin_input.clear()

        # 이벤트를 부모 클래스에게 전달하여 창을 닫음
        super().closeEvent(event)