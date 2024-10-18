import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QStatusBar, QSplitter, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from appactions import AppActions
from appviews import TreeView, FlashCardView, LessonView
from appchildclass import CardItems
from appdialogbox import Login, Register
from buildgraph import BuildGraph
from random import choice

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create AppActions and pass the main window
        self.actions = AppActions(self)
        self.setWindowTitle("NoteBook")
        self.setWindowIcon(QIcon(self.actions.resource_path("images/searching.png")))

        # Create a QLabel for the background
        background=['3d-cartoon-back-school.jpg', 'cartoon-student-math-class.jpg', 'close-up-cartoon-character-boy-reading.jpg']
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap('images/background/' + choice(background)))
        self.background_label.setScaledContents(True)  # Enable scaling
        self.background_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # Allow interaction with underlying widgets
        
        # Set the background QLabel to fill the entire window
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Ensure the QLabel is on the bottom layer
        self.background_label.lower()

        # Create a layout to center the login widget
        self.login_widget = Login()
        self.login_layout = QVBoxLayout()
        self.login_layout.addWidget(self.login_widget, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the login widget

        # Create a central widget and set its layout
        central_widget = QWidget()
        central_widget.setLayout(self.login_layout)
        self.login_widget.close_app_signal.connect(QApplication.quit)
        self.login_widget.login_request.connect(self.login_user)
        self.login_widget.regiser_request.connect(self.register_user)
        self.setCentralWidget(central_widget)
        # self.show_progress()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Resize the background label to match the main window
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def show_progress(self):
        # Create a new layout for the progress page
        self.progress_layout = QVBoxLayout()

        # Create the graph widget
        self.progress_widget = QWidget()  # Central widget
        graph_widget = BuildGraph()  # Graph plotting widget

        # Add the graph to the layout
        self.progress_layout.addWidget(graph_widget)

        # Create a button and add it to the layout
        btn = QPushButton("Go Back")
        self.progress_layout.addWidget(btn)
        
        # Set the layout to the central widget
        self.progress_widget.setLayout(self.progress_layout)
        self.setCentralWidget(self.progress_widget)

        # Connect the button click to the show_main_content method
        btn.clicked.connect(self.show_main_content)

    def register_user(self):
        dialog = Register()
        while True:
            if dialog.exec() == dialog.DialogCode.Accepted:
                name, username, password = dialog.getInput()
                # Check if the username already exists before proceeding
                status=self.actions.database.createNewUser(name, username, password)
                if not status:
                    QMessageBox.information(self, "Registration Error", "Username already exists")
                else:
                    QMessageBox.information(self, "Registration Successful", "User has been registered successfully!")
                    break
            else:
                break
    
    def login_user(self):
        input_data = self.login_widget.get_username_password()
        status = self.actions.database.userLogin(input_data)
        if status:
            self.show_main_content()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password. Please try again.")

    def show_main_content(self):
        self.background_label.hide()
        # Menu Bar
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        toolmenu = menubar.addMenu("Tools")

        # Tool Bar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Status Bar
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # Create Cards and pass the main window
        self.cards=CardItems(self)

        # Add the actions to the menubar
        # filemenu.addAction(self.actions.open_action)
        filemenu.addAction(self.actions.create_subject)
        filemenu.addAction(self.actions.create_unit)
        filemenu.addAction(self.actions.create_lesson)
        filemenu.addAction(self.actions.create_card)

        # Add the actions to the toolbar
        toolbar.addAction(self.actions.create_subject)
        toolbar.addAction(self.actions.create_unit)
        toolbar.addAction(self.actions.create_lesson)
        toolbar.addAction(self.actions.create_card)
        toolbar.addAction(self.actions.delete)
        toolbar.addAction(self.actions.move_up)
        toolbar.addAction(self.actions.move_down)

        # Main Widget with Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        file_layout = QVBoxLayout()
        file_widget = QWidget()

        # File View
        self.tree_view = TreeView(self)  # Pass MainWindow reference to TreeView
        self.flashcard_view = FlashCardView(self)  # Create the FlashCardView
        self.lesson_view = LessonView(self) # Create the LessonView

        # Stack The Widgets
        self.file_stacked_widget = QStackedWidget() # Create StackedWidget to switch between windows
        self.file_stacked_widget.addWidget(self.lesson_view) # add lesson_view to stacked widget
        self.file_stacked_widget.addWidget(self.flashcard_view) # add flashcard_view to stacked widget

        splitter.addWidget(self.tree_view)  # Add the TreeView to the splitter
        splitter.addWidget(self.file_stacked_widget)  # Add the FlashCardView to the splitter

        # Set the splitter as the layout of the file_view
        file_layout.addWidget(splitter)
        file_layout.setContentsMargins(1,1,1,1)
        file_widget.setLayout(file_layout)

        self.customMessage("Application Running")

        self.login_widget.hide()  # Hide the login widget
        # self.progress_widget.hide()
        self.setCentralWidget(file_widget)  # Set the main content as the central widget
        self.show()

    def customMessage(self, message, timeout=3000):
        self.statusBar().showMessage(message, timeout)

# Main application execution
if __name__=="__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    # window.show()
    window.showMaximized()
    sys.exit(app.exec())