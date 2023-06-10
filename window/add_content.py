from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QRadioButton, QFormLayout, QLineEdit, QVBoxLayout,
    QWidget, QTextEdit, QFileDialog, QDateEdit, QMessageBox
)
import shutil
import json

from model.content import Content


class AddContentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Content Page")

        self.layout = QVBoxLayout()

        self.radio1 = QRadioButton("애니메이션")
        self.radio1.toggled.connect(self.load_form)

        self.radio2 = QRadioButton("노래")
        self.radio2.toggled.connect(self.load_form)

        self.radio3 = QRadioButton("미연시")
        self.radio3.toggled.connect(self.load_form)

        self.layout.addWidget(self.radio1)
        self.layout.addWidget(self.radio2)
        self.layout.addWidget(self.radio3)

        self.form = QFormLayout()

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

        self.save_button = QPushButton("컨텐츠 추가")
        self.save_button.clicked.connect(self.save_content)
        self.layout.addWidget(self.save_button)

    def load_form(self):
        if self.sender().isChecked():
            content_type = self.sender().text()

            # Clear the existing form layout.
            while self.form.count():
                child = self.form.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Add content-specific fields to the form layout.
            if content_type == "애니메이션":
                self.form.addRow("제목 (한글)", QLineEdit())
                self.form.addRow("제목 (원어)", QLineEdit())
                self.form.addRow("장르", QLineEdit())
                self.form.addRow("원작", QLineEdit())
                self.form.addRow("감독", QLineEdit())
                self.form.addRow("제작사", QLineEdit())
                self.form.addRow("방영기간", QLineEdit())
                self.form.addRow("화수", QLineEdit())
            elif content_type == "노래":
                self.form.addRow("노래 제목 (한글)", QLineEdit())
                self.form.addRow("노래 제목 (원어)", QLineEdit())
                self.form.addRow("가수", QLineEdit())
                self.form.addRow("작곡가", QLineEdit())
                self.form.addRow("노래 종류", QLineEdit())
                self.form.addRow("노래 파일", QPushButton("Upload", clicked=self.upload_file))
                self.form.addRow("하이라이트", QTextEdit())
            elif content_type == "미연시":
                self.form.addRow("미연시 제목 (한글)", QLineEdit())
                self.form.addRow("미연시 제목 (원어)", QLineEdit())
                self.form.addRow("시나리오 라이터", QLineEdit())
                self.form.addRow("일러스트 레이터", QLineEdit())
                self.form.addRow("제작사", QLineEdit())
                self.form.addRow("발매일", QDateEdit())

            self.layout.addLayout(self.form)

    def save_content(self):
        try:
            # 파일을 읽는다.
            with open('data/content_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 파일이 없거나 빈 파일인 경우
            data = {
                "contents": []
            }

        # Add content-specific fields to the form layout.
        content_type = self.get_selected_content_type()
        content = None

        if content_type == "애니메이션":
            content = Content(
                type=content_type,
                title_kr=self.get_form_value("제목 (한글)"),
                title_origin=self.get_form_value("제목 (원어)"),
                attribute1=self.get_form_value("장르"),
                attribute2=self.get_form_value("원작"),
                attribute3=self.get_form_value("감독"),
            )
        elif content_type == "노래":
            content = Content(
                type=content_type,
                title_kr=self.get_form_value("노래 제목 (한글)"),
                title_origin=self.get_form_value("노래 제목 (원어)"),
                attribute1=self.get_form_value("가수"),
                attribute2=self.get_form_value("작곡가"),
                attribute3=self.get_form_value("노래 종류"),
                file=self.file.text(),
                highlights=self.highlights.text(),
            )
        elif content_type == "미연시":
            content = Content(
                type=content_type,
                title_kr=self.get_form_value("미연시 제목 (한글)"),
                title_origin=self.get_form_value("미연시 제목 (원어)"),
                attribute1=self.get_form_value("시나리오 라이터"),
                attribute2=self.get_form_value("일러스트 레이터"),
                attribute3=self.get_form_value("제작사"),
            )

        if content:
            data["contents"].append(content.to_dict())

            with open('data/content_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)

            # Show success message
            QMessageBox.information(self, "추가 완료", "추가가 완료되었습니다.")

            # Close the AddContentWindow
            self.close()


    def get_selected_content_type(self):
        if self.radio1.isChecked():
            return "애니메이션"
        elif self.radio2.isChecked():
            return "노래"
        elif self.radio3.isChecked():
            return "미연시"

        return ""

    def get_form_value(self, field_label):
        for i in range(self.form.rowCount()):
            label_item = self.form.itemAt(i, QFormLayout.LabelRole)
            if label_item and label_item.widget().text() == field_label:
                field_item = self.form.itemAt(i, QFormLayout.FieldRole)
                if field_item and field_item.widget():
                    widget = field_item.widget()
                    if isinstance(widget, QLineEdit):
                        return widget.text()
                    elif isinstance(widget, QTextEdit):
                        return widget.toPlainText()

        return ""

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*)", options=options
        )
        if file_name:
            shutil.copy(file_name, './content')  # assuming './content' directory is where you want to copy the files
    
    def closeEvent(self, event):
        print('closeEvent')
        # Clear the input fields when the window is closed
        self.clear_input_fields()

        # Call the parent class's closeEvent to ensure proper closing behavior
        super().closeEvent(event)

    def clear_input_fields(self):
        # Clear the input fields in the form
        for i in range(self.form.rowCount()):
            field_item = self.form.itemAt(i, QFormLayout.FieldRole)
            if field_item and field_item.widget():
                widget = field_item.widget()
                if isinstance(widget, QLineEdit):
                    widget.clear()
                elif isinstance(widget, QTextEdit):
                    widget.clear()

