from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from window.upload import UploadWindow
from window.edit.edit_animation import EditAnimationWindow
from window.edit.edit_song import EditSongWindow
from window.edit.edit_vocal import EditVocalWindow

import sys

class AddContentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Content Page")

        layout = QHBoxLayout()

        self.add_animation_window = EditAnimationWindow()
        animation_btn = QPushButton("애니메이션 추가")
        animation_btn.clicked.connect(self.add_animation_window.show)
        layout.addWidget(animation_btn)

        self.add_song_window = EditSongWindow()
        song_btn = QPushButton("노래 추가")
        song_btn.clicked.connect(self.add_song_window.show)
        layout.addWidget(song_btn)

        eroge_btn = QPushButton("미연시 추가")
        eroge_btn.clicked.connect(self.add_musical)
        layout.addWidget(eroge_btn)

        self.add_vcoal_window = EditVocalWindow()
        vocal_btn = QPushButton("가수 추가")
        vocal_btn.clicked.connect(self.add_vcoal_window.show)
        layout.addWidget(vocal_btn)

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