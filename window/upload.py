from PyQt5.QtWidgets import QMainWindow, QPushButton, QCheckBox, QTextEdit, QVBoxLayout, QWidget, QFileDialog
import shutil

class UploadWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Upload Page")

        layout = QVBoxLayout()

        self.file_button = QPushButton("파일 업로드")
        self.file_button.clicked.connect(self.upload_file)

        self.copy_check = QCheckBox("복사하기")

        self.info_edit = QTextEdit()

        layout.addWidget(self.file_button)
        layout.addWidget(self.copy_check)
        layout.addWidget(self.info_edit)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)", options=options)

        if file_name:
            if self.copy_check.isChecked():
                shutil.copy(file_name, './')  # copy the file to the current directory
            else:
                shutil.move(file_name, './')  # move the file to the current directory
            self.info_edit.setText(file_name + " has been uploaded.")
