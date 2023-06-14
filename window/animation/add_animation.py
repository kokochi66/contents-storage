from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFormLayout, QLineEdit
from model.animation import Animation

class AddAnimationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Content Page")

        self.layout = QVBoxLayout()

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        # Initialize animation form
        self.animation_form = QFormLayout()

                # Clear the existing layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Set up animation form
        self.title_kr_input = QLineEdit()
        self.title_origin_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.director_input = QLineEdit()
        self.airing_period_input = QLineEdit()
        self.production_company_input = QLineEdit()

        self.animation_form.addRow("애니메이션 제목 (한글)", self.title_kr_input)
        self.animation_form.addRow("애니메이션 제목 (원어)", self.title_origin_input)
        self.animation_form.addRow("장르", self.genre_input)
        self.animation_form.addRow("감독", self.director_input)
        self.animation_form.addRow("방영기간", self.airing_period_input)
        self.animation_form.addRow("제작사", self.production_company_input)

        save_btn = QPushButton("저장")
        save_btn.clicked.connect(self.save_animation)
        self.animation_form.addRow(save_btn)

        # Add animation form to the layout
        self.layout.addLayout(self.animation_form)


    def save_animation(self):
        title_kr = self.title_kr_input.text()
        title_origin = self.title_origin_input.text()
        genre = self.genre_input.text()
        director = self.director_input.text()
        airing_period = self.airing_period_input.text()
        production_company = self.production_company_input.text()

        animation = Animation(
            title_kr=title_kr,
            title_origin=title_origin,
            genre=genre,
            director=director,
            airing_period=airing_period,
            production_company=production_company
        )

        # Save the animation data
        animation.save_to_database()
        animation.save_to_file()