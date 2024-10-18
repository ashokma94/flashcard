from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editable Table Example")
        
        # Create a QWidget for the central area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create the QTableView
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        # Set up the model
        self.model = QStandardItemModel(0, 3)  # 0 rows and 3 columns
        self.model.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])

        # Populate the model with sample data
        for row in range(5):
            items = [QStandardItem(f"Item {row+1}, Col {col+1}") for col in range(3)]
            self.model.appendRow(items)

        self.table_view.setModel(self.model)

        # Enable editing
        self.table_view.setEditTriggers(QTableView.EditTrigger.DoubleClicked)

        # Set layout
        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
