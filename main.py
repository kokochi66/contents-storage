from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from window.upload import UploadWindow
from window.add_content import AddContentWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Page")

        layout = QHBoxLayout()

        btn1 = QPushButton("노래 재생")
        self.uploadWindow = UploadWindow()
        btn2 = QPushButton("업로드")
        btn2.clicked.connect(self.uploadWindow.show)
        
        btn3 = QPushButton("월드컵")
        btn4 = QPushButton("랭킹")
        btn5 = QPushButton("검색")

        self.addContentWindow = AddContentWindow()
        btn6 = QPushButton("컨텐츠 추가")
        btn6.clicked.connect(self.addContentWindow.show)

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)
        layout.addWidget(btn5)
        layout.addWidget(btn6)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
