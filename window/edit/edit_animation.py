from msilib.schema import ComboBox
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from model.animation import Animation
from model.service.data_service import DataService
from model.word import Word
from model.enum import Genre

class EditAnimationWindow(QMainWindow):
    data_changed = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setWindowTitle("애니메이션 추가 페이지")

        self.layout = QVBoxLayout()

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        # Initialize animation form
        self.form = QFormLayout()

                # Clear the existing layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Set up animation form
        self.title_kr_input = QLineEdit()
        
        self.data_key = 0
        
        self.form.addRow("애니메이션 제목 (한글)", self.title_kr_input)

        self.title_origin_input = QLineEdit()
        self.form.addRow("애니메이션 제목 (원어)", self.title_origin_input)

        self.genre_input = QComboBox()
        self.genre_input.addItems([g.value for g in Genre])  # Genre Enum에 있는 모든 장르를 추가
        self.form.addRow("장르선택", self.genre_input)

        self.add_genre_btn = QPushButton('장르추가')
        self.add_genre_btn.clicked.connect(self.add_genre)
        self.delete_genre_btn = QPushButton('장르삭제')
        self.delete_genre_btn.clicked.connect(self.delete_genre)
        self.genre_button_layout = QHBoxLayout()
        self.genre_button_layout.addWidget(self.add_genre_btn)
        self.genre_button_layout.addWidget(self.delete_genre_btn)
        self.form.addRow(self.genre_button_layout)

        self.airing_genre_list = QListWidget()
        self.airing_genre_list.setMaximumHeight(50)  # widget의 최대 높이를 설정합니다.
        self.form.addRow("장르", self.airing_genre_list)

        self.year_input = QComboBox()
        self.year_input.addItems([str(year) for year in range(2000, 2024)])  # 2000년부터 2023년까지 추가   
        self.form.addRow("년도", self.year_input)

        self.quarter_input = QComboBox()
        self.quarter_input.addItems(["WINTER", "SPRING", "SUMMER", "FALL"])
        self.form.addRow("분기", self.quarter_input)

        self.add_period_btn = QPushButton('기간추가')
        self.add_period_btn.clicked.connect(self.add_period)
        self.delete_period_btn = QPushButton('기간삭제')
        self.delete_period_btn.clicked.connect(self.delete_period)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_period_btn)
        self.button_layout.addWidget(self.delete_period_btn)
        self.form.addRow(self.button_layout)

        self.airing_period_list = QListWidget()
        self.airing_period_list.setMaximumHeight(50)  # widget의 최대 높이를 설정합니다.
        self.form.addRow("방영기간", self.airing_period_list)

        self.director_input = QLineEdit()
        self.form.addRow("감독", self.director_input)
               
        self.production_company_input = QLineEdit()
        self.form.addRow("제작사", self.production_company_input)

        
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
        self.save_btn.clicked.connect(self.save_animation)
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_animation)  # delete_animation 메소드를 아래에서 정의
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.form.addRow(self.button_layout)

        # Add animation form to the layout
        self.layout.addLayout(self.form)

        # 초기 상태에서는 삭제 버튼을 비활성화합니다.
        self.delete_btn.setVisible(False)
        self.edit_flag = False


    def save_animation(self):
        title_kr = self.title_kr_input.text()
        title_origin = self.title_origin_input.text()
        genre = [self.airing_genre_list.item(i).text() for i in range(self.airing_genre_list.count())]
        director = self.director_input.text()

        if DataService.is_key_exist('animation_data.json', title_origin) and not self.edit_flag:
            QMessageBox.warning(self, "오류", "이미 존재하는 타이틀 입니다.")
            return


        # 방영기간은 모든 항목을 리스트로 저장합니다.
        airing_period = [self.airing_period_list.item(i).text() for i in range(self.airing_period_list.count())]
        production_company = self.production_company_input.text()
        data_key = self.data_key

        animation = Animation(
            title_kr=title_kr,
            title_origin=title_origin,
            genre=genre,
            director=director,
            airing_period=airing_period,
            production_company=production_company,
            key=data_key
        )

        # Save the animation data
        animation.save_to_file()

        # Get the current list of words
        current_words = [self.airing_word_list.item(i).text() for i in range(self.airing_word_list.count())]

        # Load the existing words related to this animation
        existing_words = DataService.get_all_data('word_data.json')
        
        word_data = DataService.get_all_data('word_data.json')
        for key, word in word_data.items():
            if str(word['data_value']) == str(animation.key) and str(word['key']) not in current_words:
                DataService.delete_data('word_data.json', word['key'])

        # Save the updated list of words
        for word in current_words:
            word = Word(
                word,
                "animation_data.json",
                animation.key
            )
            word.save_to_file()
            

        # 알림 창 띄우기
        QMessageBox.information(self, "저장 완료", "저장이 완료되었습니다.")
        
        # 창 닫기
        self.data_changed.emit()
        self.close()

    def setData(self, animation_data):
        self.data_key = animation_data['key']
        self.title_kr_input.setText(animation_data['title_kr'])
        self.title_kr_input.setEnabled(False)
        self.title_origin_input.setText(animation_data['title_origin'])
        self.title_origin_input.setEnabled(False)
        self.director_input.setText(animation_data['director'])
        self.production_company_input.setText(animation_data['production_company'])

        # 장르와 방영기간, 검색어는 리스트 형태로 저장되어 있으므로, 각각의 요소를 리스트 위젯에 추가해주는 작업이 필요합니다.
        for genre in animation_data['genre']:
            self.airing_genre_list.addItem(genre)
        
        for period in animation_data['airing_period']:
            self.airing_period_list.addItem(period)

        # Word 데이터에서 해당 애니메이션에 해당하는 검색어 리스트를 가져와서 airing_word_list에 추가
        word_data = DataService.get_all_data('word_data.json')
        for key, word in word_data.items():
            if word['data_value'] == animation_data['key']:
                self.airing_word_list.addItem(word['key'])

        # 데이터가 설정된 경우에만 삭제 버튼을 활성화합니다.
        self.delete_btn.setVisible(True)
        
        self.animation_data = animation_data  # 삭제 시 사용하려고 저장해 둡니다.
        self.edit_flag = True

    def add_period(self):
        year = self.year_input.currentText()
        quarter = self.quarter_input.currentText()
        period = f"{year}-{quarter}"

        # 기존에 추가된 항목들과 비교
        for i in range(self.airing_period_list.count()):
            if self.airing_period_list.item(i).text() == period:
                QMessageBox.warning(self, "오류", "이미 추가된 분기입니다.")
                return
        self.airing_period_list.addItem(period)


    def delete_period(self):
        for item in self.airing_period_list.selectedItems():
            self.airing_period_list.takeItem(self.airing_period_list.row(item))

    def add_genre(self):
        genre = self.genre_input.currentText()

        # 기존에 추가된 항목들과 비교
        for i in range(self.airing_genre_list.count()):
            if self.airing_genre_list.item(i).data(Qt.UserRole) == genre:
                QMessageBox.warning(self, "오류", "이미 추가된 장르입니다.")
                return

        self.airing_genre_list.addItem(genre)

    def delete_genre(self):
        for item in self.airing_genre_list.selectedItems():
            self.airing_genre_list.takeItem(self.airing_genre_list.row(item))

    def closeEvent(self, event):
        # 각 입력 필드를 초기화
        self.title_kr_input.clear()
        self.title_origin_input.clear()
        self.director_input.clear()
        self.production_company_input.clear()

        # 장르와 방영기간 리스트를 초기화
        self.airing_genre_list.clear()
        self.airing_period_list.clear()

        self.airing_word_list.clear()

        # 이벤트를 부모 클래스에게 전달하여 창을 닫음
        super().closeEvent(event)

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

    def delete_animation(self):
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