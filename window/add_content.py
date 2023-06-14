from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from window.upload import UploadWindow
from window.animation.add_animation import AddAnimationWindow

import sys

class AddContentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Content Page")

        layout = QHBoxLayout()

        self.add_animation_window = AddAnimationWindow()
        btn1 = QPushButton("애니메이션 추가")
        btn1.clicked.connect(self.add_animation_window.show)

        btn2 = QPushButton("노래 추가")
        btn2.clicked.connect(self.add_song)

        btn3 = QPushButton("미연시 추가")
        btn3.clicked.connect(self.add_musical)

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def add_animation(self):
        # TODO: Implement the functionality to add animation content
        pass

    def add_song(self):
        # TODO: Implement the functionality to add song content
        pass

    def add_musical(self):
        # TODO: Implement the functionality to add musical content
        pass