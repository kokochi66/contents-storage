from msilib.schema import ComboBox
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QListWidget, QMessageBox, QHBoxLayout, QListWidgetItem, QCompleter, QDateEdit
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from model.song import Song
from model.data_service import DataService
from model.vocal import Vocal
from model.word import Word
from model.enum import Genre

class EditVocalWindow(QMainWindow):
    data_changed = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setWindowTitle("가수 추가 페이지")

        self.layout = QVBoxLayout()

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        # 저장 폼
        self.form = QFormLayout()
        self.data_key = 0
        # 기본값 초기화
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 가수이름 입력폼
        self.name_kr = QLineEdit()
        self.form.addRow("가수 이름 (한글)", self.name_kr)

        self.name_origin = QLineEdit()
        self.form.addRow("가수 이름 (원어)", self.name_origin)

        # 데뷔일 입력폼
        self.debut_date = QDateEdit()
        self.form.addRow("데뷔일", self.debut_date)

        self.layout.addLayout(self.form)

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

        self.airing_word_list = QListWidget()
        self.airing_word_list.setMaximumHeight(50)  # widget의 최대 높이를 설정합니다.
        self.form.addRow("검색어", self.airing_word_list)

        # 저장 및 삭제 버튼 추가
        self.save_btn = QPushButton("저장")
        self.save_btn.clicked.connect(self.save_vocal)
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_vocal)  # delete_animation 메소드를 아래에서 정의
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.form.addRow(self.button_layout)

        # 초기 상태에서는 삭제 버튼을 비활성화합니다.
        self.edit_flag = False

    # 가수 저장
    def save_vocal(self):
        vocal = Vocal(
            name_kr=self.name_kr.text(),
            name_origin=self.name_origin.text(),
            debut_date=self.debut_date.date().toString(Qt.ISODate),
            key=self.data_key
        )
        # 데이터 저장
        vocal.save_to_file()

        # 검색어 키 저장
        current_words = [self.airing_word_list.item(i).text() for i in range(self.airing_word_list.count())]

        # 중복 검색어가 있는지 확인하기 위해서 데이터를 조회
        word_data = DataService.get_all_data(Word.file_name)
        for key, word in word_data.items():
            if str(word['data_value']) == str(vocal.key) and str(word['key']) not in current_words:
                DataService.delete_data(Word.file_name, word['key'])

        # 각 생성한 검색어 저장
        for word in current_words:
            word = Word(
                word,
                Vocal.file_name,
                vocal.key
            )
            word.save_to_file()
            

        # 알림 창 띄우기
        QMessageBox.information(self, "저장 완료", "저장이 완료되었습니다.")
        
        # 창 닫기
        self.data_changed.emit()
        self.close()


    def delete_vocal(self):
        DataService.delete_data(Vocal.file_name, self.data.key)

        # word_data.json에서 해당 검색어 데이터 삭제
        # 데이터 구조가 적절하다면, 단어 데이터를 한번에 가져와서 각각 삭제합니다.
        word_data = DataService.get_all_data(Word.file_name)
        for key, word in word_data.items():
            if word['data_value'] == self.data.key:
                DataService.delete_data(Word.file_name, word['key'])

        # 알림 창 띄우기
        QMessageBox.information(self, "삭제 완료", "삭제가 완료되었습니다.")

        # 데이터 변경 신호를 보내고 창 닫기
        self.data_changed.emit()
        self.close()

    def setData(self, data):
        self.data_key = data['key']
        self.name_kr.setText(data['name_kr'])
        self.name_origin.setText(data['name_origin'])
        year, month, day = map(int, data['debut_date'].split('-'))
        self.debut_date.setDate(QDate(year, month, day))

        # Word 데이터에서 해당 애니메이션에 해당하는 검색어 리스트를 가져와서 airing_word_list에 추가
        word_data = DataService.get_all_data(Word.file_name)
        for key, word in word_data.items():
            if word['data_value'] == data['key']:
                self.airing_word_list.addItem(word['key'])
    
        self.data = data  # 삭제 시 사용하려고 저장해 둡니다.
        self.edit_flag = True

    def add_word(self):
        word = self.word_input.text()

        # 기존에 추가된 항목들과 비교
        for i in range(self.airing_word_list.count()):
            if self.airing_word_list.item(i).text() == word:
                QMessageBox.warning(self, "오류", "이미 추가된 검색어입니다.")
                return

        # JSON 파일에 키가 이미 존재하는지 확인
        if DataService.is_key_exist('word_data.json', word):
            QMessageBox.warning(self, "오류", "이미 존재하는 검색어입니다.")
            return

        self.airing_word_list.addItem(word)

    def delete_word(self):
        for item in self.airing_word_list.selectedItems():
            self.airing_word_list.takeItem(self.airing_word_list.row(item))

    def closeEvent(self, event):
        # 각 입력 필드를 초기화
        self.name_kr.clear()
        self.name_origin.clear()
        self.debut_date.clear()

        # 이벤트를 부모 클래스에게 전달하여 창을 닫음
        super().closeEvent(event)