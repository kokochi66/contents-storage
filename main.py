from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
from model.animation import Animation
from model.service.data_service import DataService
from model.song import Song
from model.vocal import Vocal
from window.upload import UploadWindow
from window.add_content import AddContentWindow
from window.edit.edit_animation import EditAnimationWindow
from window.edit.edit_song import EditSongWindow
from window.edit.edit_vocal import EditVocalWindow
import sys
import os

class MainWindow(QMainWindow):
    data_changed = pyqtSignal()
    root = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Page")

        main_layout = QVBoxLayout()  # 메인 레이아웃을 QVBoxLayout로 변경


        # 검색창
        search_layout = QHBoxLayout()  # 검색창에 대한 레이아웃 생성

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.returnPressed.connect(self.search)  # 엔터키 눌렀을 때 검색 기능 연결

        self.search_button = QPushButton("검색")
        self.search_button.clicked.connect(self.search)  # 검색 버튼 클릭시 검색 기능 연결

        self.update_completer()
        self.data_changed.connect(self.update_completer)

        search_layout.addWidget(self.search_input)  # 검색창 레이아웃에 추가
        search_layout.addWidget(self.search_button)  # 검색창 레이아웃에 추가

        

        self.addContentWindow = AddContentWindow()
        btn6 = QPushButton("추가")
        btn6.clicked.connect(self.addContentWindow.show)

        button_layout = QHBoxLayout()  # 버튼에 대한 레이아웃 생성
        button_layout.addWidget(btn6)  # 버튼 레이아웃에 추가

        main_layout.addLayout(search_layout)  # 메인 레이아웃에 검색창 레이아웃 추가
        main_layout.addLayout(button_layout)  # 메인 레이아웃에 버튼 레이아웃 추가

        container = QWidget()
        container.setLayout(main_layout)  # 메인 레이아웃 설정

        self.setCentralWidget(container)

        QApplication.instance().applicationStateChanged.connect(self.on_applicationStateChanged)

    def search(self):
        search_keyword = self.search_input.text()

        # 데이터 로드 코드 추가...
        word_data = DataService.load_data('word_data.json', search_keyword)
        if not word_data:
            msg = QMessageBox()
            msg.setWindowTitle("검색 결과 없음")
            msg.setText("검색어를 찾을 수 없습니다.")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            return
        
        data = DataService.load_data(word_data['data_name'], word_data['data_value'])
        self.open_window(data, word_data['data_name'])

    def update_completer(self):
        word_keys = DataService.get_all_keys('word_data.json')
        self.completer = QCompleter(word_keys)  # 자동 완성 제안 단어
        self.completer.setMaxVisibleItems(10)
        self.search_input.setCompleter(self.completer)  # 자동 완성 기능을 QLineEdit에 연결

    def on_applicationStateChanged(self, state):
        if state == Qt.ApplicationActive:   # 어플리케이션이 활성화되었을 때
            self.update_completer()

    def open_window(self, data, data_name):
        if data_name == Animation.file_name:
            self.editWindow = EditAnimationWindow()
            self.editWindow.setData(data)
            self.editWindow.show()
        elif data_name == Song.file_name:
            self.editWindow = EditSongWindow()
            self.editWindow.setData(data)
            self.editWindow.show()
        elif data_name == Vocal.file_name:
            self.editWindow = EditVocalWindow()
            self.editWindow.setData(data)
            self.editWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
