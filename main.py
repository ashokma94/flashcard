import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QStatusBar, QSplitter)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from appactions import AppActions
from appviews import TreeView, FlashCardView
from appchildclass import CardItems

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create Cards and pass the main window
        self.cards=CardItems(self)

        # Create AppActions and pass the main window
        self.actions = AppActions(self)

        self.setWindowTitle("Flash Card")
        self.setWindowIcon(QIcon(self.actions.resource_path("images/flashcard.png")))

        # Menu Bar
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        toolmenu = menubar.addMenu("Tools")

        # Tool Bar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Add the actions to the menubar
        # filemenu.addAction(self.actions.open_action)
        filemenu.addAction(self.actions.create_subject)
        filemenu.addAction(self.actions.create_lesson)
        filemenu.addAction(self.actions.create_card)

        # Add the actions to the toolbar
        toolbar.addAction(self.actions.create_subject)
        toolbar.addAction(self.actions.create_lesson)
        toolbar.addAction(self.actions.create_card)

        # Main Widget with Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.left_panel = TreeView(self)  # Pass MainWindow reference to TreeView
        self.right_panel = FlashCardView(self)  # Create the FlashCardView
        splitter.addWidget(self.left_panel)  # Add the TreeView to the splitter
        splitter.addWidget(self.right_panel)  # Add the FlashCardView to the splitter
        splitter.setSizes([200, 600])  # Adjust sizes as needed

        self.setCentralWidget(splitter)  # Set the splitter as the central widget

        # Status Bar
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        self.statusBar().showMessage("Application Running", 3000)

# Main application execution
app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()
window.showMaximized()
sys.exit(app.exec())