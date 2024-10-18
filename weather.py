import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtCore import Qt


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 300)  # Set fixed size for the login dialog

        layout = QVBoxLayout(self)

        # Create username and password fields
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Add fields to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Create button layout
        button_layout = QVBoxLayout()
        self.login_button = QPushButton("Login")
        self.close_button = QPushButton("Close")

        self.login_button.clicked.connect(self.accept)
        self.close_button.clicked.connect(self.reject)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

        layout.addStretch()  # Add stretch to push buttons down


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        # self.setGeometry(100, 100, 400, 400)  # Main window size

        # Create a central widget for the main window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create layout for the central widget
        self.layout = QVBoxLayout(self.central_widget)

        # Center the Login dialog
        self.login_widget = Login()
        self.layout.addStretch()  # Stretch before the login widget
        self.layout.addWidget(self.login_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch()  # Stretch after the login widget

        # Connect the login button to handle login logic
        self.login_widget.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.login_widget.username_input.text().strip()
        password = self.login_widget.password_input.text().strip()

        if username and password:  # Simple validation
            print("Login Success. Implementation pending.")
            self.login_widget.accept()  # Close dialog on successful login
        else:
            QMessageBox.warning(self, "Login Error", "Username and password required.")


# Main application execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())