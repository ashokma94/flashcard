from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt

class OkDialog(QDialog):
    def __init__(self, title, label):
        super().__init__()
        self.setWindowTitle(title)

        # Set up the layout for the dialog
        layout = QVBoxLayout()

        # Add a label and input field for the subject
        self.subjectlabel = QLabel(label)
        self.subjectinput = QLineEdit()
        layout.addWidget(self.subjectlabel)
        layout.addWidget(self.subjectinput)

        # Add an OK button
        self.okbutton = QPushButton("OK")
        self.okbutton.clicked.connect(self.accept)  # Accept the dialog when OK is clicked
        layout.addWidget(self.okbutton)

        self.setLayout(layout)

    def getinput(self):
        return self.subjectinput.text()

class Card(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Card")
        self.resize(700, 500)  # Set a fixed size for the dialog

        # Set up the layout for the dialog
        layout = QVBoxLayout()

        # Set better monospace font for the inputs (e.g., Consolas, Monaco, or DejaVu Sans Mono)
        monospace_font = QFont("Consolas", 10)  # Consolas is a clean monospace font, adjust size as needed

        # Question input (Front) with QTextEdit for multiline
        self.question_label = QLabel("Question:")
        self.question_input = QTextEdit()
        self.question_input.setFixedHeight(100)
        self.question_input.setPlaceholderText("Enter the question")
        # self.question_input.setToolTip("This is the question or the front side of the flashcard.")
        self.question_input.setFont(monospace_font)  # Set the better-looking monospace font
        layout.addWidget(self.question_label)
        layout.addWidget(self.question_input)

        # Answer input (Back) with QTextEdit for multiline
        self.answer_label = QLabel("Answer:")
        self.answer_input = QTextEdit()
        self.answer_input.setPlaceholderText("Enter the answer")
        # self.answer_input.setToolTip("This is the answer or the back side of the flashcard.")
        self.answer_input.setFont(monospace_font)  # Set the better-looking monospace font
        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_input)

        # Button layout (OK and Cancel) placed next to each other
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # OK button with fixed size
        self.ok_button = QPushButton("Save")
        self.ok_button.setFixedSize(80, 30)  # Set the button size to prevent enlargement
        self.ok_button.clicked.connect(self.on_ok_clicked)
        button_layout.addWidget(self.ok_button)

        # Cancel button with fixed size
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(80, 30)  # Set the button size to prevent enlargement
        self.cancel_button.clicked.connect(self.reject)  # Close the dialog without accepting
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()

        # Add button layout to the main layout
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_ok_clicked(self):
        # Validate input fields before accepting
        if not self.question_input.toPlainText().strip() or not self.answer_input.toPlainText().strip():
            # Show an error message if either field is empty
            QMessageBox.warning(self, "Input Error", "Both 'Front' and 'Back' fields are required!")
        else:
            self.accept()  # Close the dialog and return success

    def getinput(self):
        # Return the question and answer as a dictionary
        return {
            "question": self.question_input.toPlainText().strip(),
            "answer": self.answer_input.toPlainText().strip()
        }

class Login(QDialog):
    close_app_signal = pyqtSignal()
    login_request = pyqtSignal()
    regiser_request = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("color: white")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("color: white")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.login_button = QPushButton("Login")
        self.login_button.setFixedSize(80, 30)
        self.login_button.clicked.connect(self.validation)
        self.close_button = QPushButton("Exit")
        self.close_button.setFixedSize(80, 30)
        self.close_button.clicked.connect(self.close_app)
        self.register_button = QPushButton("Register")
        self.register_button.setFixedSize(80, 30)
        self.register_button.clicked.connect(self.user_register)
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.login_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()
        self.setLayout(layout)
    
    def validation(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if username and password:
            self.login_request.emit()
        else:
            QMessageBox.warning(self, "Input Error", "Username and password required")
    
    def user_register(self):
        self.regiser_request.emit()
        
    def close_app(self):
        self.close_app_signal.emit()

    def get_username_password(self):
        return {"username" : self.username_input.text().strip(), 
                "password" : self.password_input.text().strip()
                }

class Register(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 220)
        self.setWindowTitle("Register")
        layout = QVBoxLayout()
        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(80, 30)
        self.submit_button.clicked.connect(self.validation)
        self.close_button = QPushButton("Close")
        self.close_button.setFixedSize(80, 30)
        self.close_button.clicked.connect(self.reject)
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()
        self.setLayout(layout)
    
    def validation(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if name and username and password:
            self.accept()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill all the fields")
    
    def getInput(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        return name, username, password