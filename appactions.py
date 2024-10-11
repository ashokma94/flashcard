import sys,os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from appdialogbox import OkDialog, Card
from appdatabase import Database

class AppActions:
    def __init__(self, main_window):
        self.main_window = main_window
        self.database = Database()

        # Create actions for the toolbar
        self.create_subject = QAction(QIcon(self.resource_path("images/subject.png")), "Add Subject", self.main_window)
        self.create_subject.triggered.connect(self.createNewSubject)

        self.create_lesson = QAction(QIcon(self.resource_path("images/lesson.png")), "Add Lesson", self.main_window)
        self.create_lesson.triggered.connect(self.createNewLesson)

        self.create_card = QAction(QIcon(self.resource_path("images/question.png")), "Add Card", self.main_window)
        self.create_card.triggered.connect(self.createNewCard)

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def createNewSubject(self):
        dialog = OkDialog("Add New Subject", "Enter The Subject Name:")
        if dialog.exec() == dialog.DialogCode.Accepted:
            subject_name = dialog.getinput()
            subject_id = self.database.addSubject(subject_name)
            self.main_window.left_panel.populate_tree(subject_id) # Refresh the tree view after adding a subject

    def createNewLesson(self):
        # Get the currently selected item from the tree view
        selected_item = self.main_window.left_panel.currentItem()  # Get the selected item from TreeView

        if selected_item is not None:
            # Check if the selected item is a subject or a lesson
            parent_item = selected_item.parent()  # Get the parent item

            # Show dialog to add a new lesson
            dialog = OkDialog("Add New Lesson", "Enter The Lesson Name:")
            if dialog.exec() == dialog.DialogCode.Accepted:
                lesson_name = dialog.getinput()  # Get the lesson name from the dialog
                
                if parent_item is None:
                    # It's a subject, retrieve the subject ID
                    subject_id = selected_item.data(0, Qt.ItemDataRole.UserRole)  # Retrieve the subject ID
                else:
                    # It's a lesson, retrieve the subject ID from the parent
                    subject_id = parent_item.data(0, Qt.ItemDataRole.UserRole)  # Retrieve the subject ID from the parent
                
                # Add the lesson with the subject ID
                self.database.addLesson(subject_id, lesson_name)
                self.main_window.left_panel.populate_tree(subject_id)  # Refresh the tree view after adding a lesson
        else:
            QMessageBox.warning(self.main_window, "Selection Error", "Please select a subject or lesson to add a lesson.")

    def createNewCard(self):
        # Get the currently selected item from the tree view
        selected_item = self.main_window.left_panel.currentItem()

        # Check if the selected item is not empty and is a lesson
        if selected_item is None or selected_item.parent() is None:
            QMessageBox.warning(self.main_window, "Selection Error", "Please select a lesson to add a card.")
            return  # Exit the method if no item is selected

        # It's a lesson, show the dialog to add a card
        dialog = Card()
        if dialog.exec() == dialog.DialogCode.Accepted:
            card_data = dialog.getinput()
            lesson_id = selected_item.data(0, Qt.ItemDataRole.UserRole)  # Retrieve the lesson ID
            lastinsertid=self.database.addCard(card_data['question'], card_data['answer'], lesson_id)  # Add the card with the lesson ID
            # print(self.main_window.cards)  # Check if this exists before appending
            print(self.main_window.cards.cardList)  # Check the card list before appending
            # Refresh the tree view after adding a card
            # self.main_window.left_panel.populate_tree(selected_item.parent().data(0, Qt.ItemDataRole.UserRole))
            self.main_window.cards.cardList.append(lastinsertid)

    def getCardIdList(self, lessonid):
        # Retrieve the card IDs for the given item ID
        return self.database.getCardIds(lessonid)
    
    def getCard(self, cardid):
        # Retrieve the card IDs for the given item ID
        return self.database.getCard(cardid)