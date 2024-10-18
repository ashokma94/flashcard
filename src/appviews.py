from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QTextCharFormat,QColor, QFont
import sys, os

class FlashCardView(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1,1,1,1)

        # Question Label and Input
        self.question_label = QLabel("Question:")
        self.question_input = QTextEdit()
        self.question_input.setFixedHeight(100)
        layout.addWidget(self.question_label)
        layout.addWidget(self.question_input)

        # User Answer Label and Input
        self.user_answer_label = QLabel("User Answer:")
        self.user_answer_input = QTextEdit()
        layout.addWidget(self.user_answer_label)
        layout.addWidget(self.user_answer_input)

        # Answer Label and Input
        self.answer_label = QLabel("Actual Answer:")
        self.answer_input = QTextEdit()
        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_input)

        # Button Layout
        buttons_layout = QHBoxLayout()
        self.prev_button = QPushButton("Prev")
        self.show_answer_button = QPushButton("Show Answer")
        self.next_button = QPushButton("Next")

        # Center buttons and set fixed width
        self.prev_button.setFixedWidth(100)
        self.show_answer_button.setFixedWidth(100)
        self.next_button.setFixedWidth(100)

        self.next_button.clicked.connect(self.nextCard)
        self.prev_button.clicked.connect(self.prevCard)
        self.show_answer_button.clicked.connect(self.showAnswer)
        
        buttons_layout.addStretch()  # Add stretch before buttons
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.show_answer_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addStretch()

        # Add buttons layout to the main layout
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def nextCard(self):
        self.card=self.main_window.actions.getCard(self.main_window.cards.next())
        if self.card:
            self.question_input.setPlainText(self.card[0][1])
            self.answer_input.setPlainText("")
    
    def prevCard(self):
        self.card=self.main_window.actions.getCard(self.main_window.cards.prev())
        if self.card:
            self.question_input.setPlainText(self.card[0][1])
            self.answer_input.setPlainText("")
    
    def showCard(self):
        self.card=self.main_window.actions.getCard(self.main_window.cards.current)
        if self.card is None:
            self.main_window.customMessage("Cards not available to display")
            return
        self.question_input.setPlainText(self.card[0][1])

    def showAnswer(self):
        if not hasattr(self, 'card'):
            self.main_window.customMessage("Please select the lesson to view the card")
            return
        if self.card is None:
            self.main_window.customMessage("Cards not available to display")
            return
        self.answer_input.setPlainText(self.card[0][2])
        # self.answer_input.setHtml(self.card[0][2])  
    
    def resetWindow(self):
        self.question_input.setPlainText("")
        self.answer_input.setPlainText("")
        self.main_window.cards.reset()

class TreeView(QTreeWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setHeaderLabels(["Subjects"])  # Set the header of the tree
        self.setMaximumWidth(250)  # Adjust as necessary
        # self.setIndentation(10)
        # self.setDragEnabled(True)          # Allow dragging
        # self.setAcceptDrops(True)          # Accept drops
        # self.setDropIndicatorShown(True)   # Show drop indicator
        # self.setDefaultDropAction(Qt.DropAction.MoveAction)  # Set default drop action as Move
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        css_path = os.path.join(base_path, 'static', 'treeview.css')
        right_arrow = self.main_window.actions.resource_path("images/icons/arrow_right.png")
        down_arrow = self.main_window.actions.resource_path("images/icons/arrow_down.png")
        with open('static/treeview.css', "r") as f:
            stylesheet = f.read()
        # stylesheet = stylesheet.replace('right_arrow', right_arrow).replace('down_arrow', down_arrow)
        # Apply the stylesheet
        self.setStyleSheet(stylesheet)
        self.prevSelectedUnitName = None

        # Populate the tree with initial data
        self.populate_tree()

        # Connect the itemClicked signal to a slot
        self.itemClicked.connect(self.on_item_selected)

    def populate_tree(self, current_subject_id=None, current_unit_id=None):
        self.clear()  # Clear the existing items

        subjects = self.main_window.actions.database.getSubjects()  # Fetch subjects from the database
        for subject_id, subject_name, *_ in subjects:
            subject_item = QTreeWidgetItem(self, [subject_name])
            subject_item.setData(0, Qt.ItemDataRole.UserRole, subject_id)  # Store subject ID in the item

            # Expand only the current subject if it's provided
            if current_subject_id is not None and subject_id == current_subject_id:
                subject_item.setExpanded(True)  # Expand the current subject

            # Fetch units for the subject
            units = self.main_window.actions.database.getUnits(subject_id)
            for unit_id, unit_name, subject_id, *_ in units:
                unit_item = QTreeWidgetItem(subject_item, [unit_name])
                unit_item.setData(0, Qt.ItemDataRole.UserRole, unit_id)  # Store unit ID in the item
                if current_unit_id is not None and unit_id==current_unit_id:
                    unit_item.setExpanded(True)

                # Fetch lessons for the unit
                lessons = self.main_window.actions.database.getLessons(unit_id)
                for lesson_id, lesson_name, lesson_content, unit_id, *_ in lessons:
                    lesson_item = QTreeWidgetItem(unit_item, [lesson_name])
                    lesson_item.setData(0, Qt.ItemDataRole.UserRole, lesson_id)  # Store lesson ID in the item

                # After lessons, add a Q&A section for the unit
                qa_item = QTreeWidgetItem(unit_item, ["Cards"])  # cards item
                qa_item.setData(0, Qt.ItemDataRole.UserRole, unit_id)  # Store unit ID or relevant ID

    def on_item_selected(self, item, column):
        # This method is called whenever an item is clicked
        if item is None or item.parent() is None:
            return
        
        # Get the ID associated with the clicked item
        item_id = item.data(0, Qt.ItemDataRole.UserRole)  
        item_text = item.text(0)  # Get the text of the clicked item

        if item.parent().parent() is None:
            return
        
        if item_text == self.prevSelectedUnitName:
            return

        # Check if the selected item is the Q&A item
        if item_text == "Cards":
            # Handle displaying the Q&A cards
            self.main_window.flashcard_view.resetWindow()
            card_id_list = self.main_window.actions.getCardIdList(item_id)  # Get the cards for this unit
            self.main_window.cards.cardList = card_id_list if card_id_list is not None else []
            self.main_window.flashcard_view.showCard()
            self.main_window.file_stacked_widget.setCurrentWidget(self.main_window.flashcard_view)
        else:
            # Handle other selections (e.g., lessons)
            # Logic to handle selection of lessons can be added here if needed
            lession_id=self.getLessonId()
            self.main_window.lesson_view.showData(lession_id)
            self.main_window.file_stacked_widget.setCurrentWidget(self.main_window.lesson_view)
            
        self.prevSelectedUnitName = item_text
    
    def getSubjectAndUnitId(self):
        selected_item = self.currentItem()
        if selected_item is None or selected_item.parent() is None:
            return
        if selected_item.parent().parent() is None:
            unit_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
            subject_id = selected_item.parent().data(0, Qt.ItemDataRole.UserRole)
        else:
            unit_id = selected_item.parent().data(0, Qt.ItemDataRole.UserRole)
            subject_id = selected_item.parent().parent().data(0, Qt.ItemDataRole.UserRole)
        
        return (subject_id, unit_id)
    
    def getLessonId(self):
        selected_item = self.currentItem()
        if selected_item is None or selected_item.parent() is None:
            return
        if selected_item.parent().parent() is not None and selected_item.text(0) != "Cards":
            lesson_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
            return lesson_id
        
    def getItemTypeAndId(self):
        selected_item = self.currentItem()
        if selected_item is None:
            return None, None  # No item is selected

        # Check if it's a Subject (root level item, no parent)
        if selected_item.parent() is None:
            item_type = "subjects"
            subject_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
            return item_type, subject_id

        # Check if it's a Unit (child of a Subject, has a parent but no grandparent)
        if selected_item.parent().parent() is None:
            item_type = "units"
            unit_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
            return item_type, unit_id

        # Check if it's a Lesson (child of a Unit, has both a parent and grandparent)
        if selected_item.parent().parent() is not None and selected_item.text(0) != "Cards":
            item_type = "lessons"
            lesson_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
            return item_type, lesson_id

        return None, None  # If it doesn't match any known type


class LessonView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window=main_window
        layout = QVBoxLayout(self)

        self.editor=QTextEdit()

        # Header/Editor Tool Layout
        editor_tool_layout = QHBoxLayout()
        editor_tool_layout.setContentsMargins(1,1,1,1)
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["8","9","10","11","12","14","16","18","20","22","24"])
        self.font_size_combo.setCurrentText("12")
        self.bold_button = QPushButton(QIcon(self.main_window.actions.resource_path("images/editor/bold.png")),"")
        self.italic_button = QPushButton(QIcon(self.main_window.actions.resource_path("images/editor/italic.png")), "")
        self.underline_button = QPushButton(QIcon(self.main_window.actions.resource_path("images/editor/underline.png")), "")
        self.highlight_button = QPushButton(QIcon(self.main_window.actions.resource_path("images/editor/highlight.png")), "")
        editor_tool_layout.addWidget(self.bold_button)
        editor_tool_layout.addWidget(self.italic_button)
        editor_tool_layout.addWidget(self.underline_button)
        editor_tool_layout.addWidget(self.highlight_button)
        editor_tool_layout.addWidget(self.font_size_combo)
        editor_tool_layout.addStretch()

        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        # Construct the path to the CSS file
        css_path = os.path.join(base_path, 'static', 'buttons.css')
        css_path='static/buttons.css'

        with open(css_path,'r') as f:
            buttonstyle=f.read()

        # Footer Button Layout
        buttons_layout=QHBoxLayout()
        buttons_layout.setContentsMargins(1,1,1,1)
        self.edit_button=QPushButton("Edit")
        self.save_button=QPushButton("Save")
        self.prev_button=QPushButton("Prev")
        self.next_button=QPushButton("Next")
        self.edit_button.setStyleSheet(buttonstyle)
        self.save_button.setStyleSheet(buttonstyle)
        self.prev_button.setStyleSheet(buttonstyle)
        self.next_button.setStyleSheet(buttonstyle)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addStretch()

        # ToolTip
        self.font_size_combo.setToolTip("Font Size")
        self.bold_button.setToolTip("Bold (Ctrl+B)")
        self.italic_button.setToolTip("Italic (Ctrl+I)")
        self.underline_button.setToolTip("Underline (Ctrl+U)")
        self.highlight_button.setToolTip("Text Highlight (Ctrl+H)")
        self.edit_button.setToolTip("Edit (Ctrl+E)")
        self.save_button.setToolTip("Save (Ctrl+S)")

        # Connect buttons to their functionalities
        self.bold_button.clicked.connect(self.toggle_bold)
        self.italic_button.clicked.connect(self.toggle_italic)
        self.underline_button.clicked.connect(self.toggle_underline)
        self.font_size_combo.currentTextChanged.connect(self.change_font_size)
        self.highlight_button.clicked.connect(self.highlight_text)
        self.edit_button.clicked.connect(self.toggle_edit)
        self.save_button.clicked.connect(self.save_lesson)

        # Add Shortcut
        self.bold_button.setShortcut("Ctrl+B")
        self.italic_button.setShortcut("Ctrl+I")
        self.underline_button.setShortcut("Ctrl+U")
        self.highlight_button.setShortcut("Ctrl+H")
        self.edit_button.setShortcut("Ctrl+E")
        self.save_button.setShortcut("Ctrl+S")

        layout.addLayout(editor_tool_layout)
        layout.addWidget(self.editor)
        layout.addLayout(buttons_layout)
        layout.setSpacing(5)

        self.setLayout(layout)
        self.setReadOnly()

    def toggle_edit(self):
        if self.editor.isReadOnly():
            self.editor.setReadOnly(False)
            self.edit_button.setVisible(False)
            self.save_button.setVisible(True)

    def setReadOnly(self):
        self.editor.setReadOnly(True)
        self.edit_button.setVisible(True)
        self.save_button.setVisible(False)

    def save_lesson(self):
        selected_lession_id = self.main_window.tree_view.getLessonId()
        if selected_lession_id is None:
            return
        data=self.editor.toHtml().strip()
        self.main_window.actions.database.editLesson(selected_lession_id, data)
        self.setReadOnly()

    def showData(self, lession_id):
        self.setReadOnly()
        data=self.main_window.actions.database.getLesson(lession_id)
        if data:
            self.editor.setHtml(data[0][0])

    def toggle_bold(self):
        # Toggle bold formatting for the selected text
        cursor = self.editor.textCursor()
        fmt = cursor.charFormat()
        new_weight = QFont.Weight.Bold if fmt.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal
        fmt.setFontWeight(new_weight)
        cursor.setCharFormat(fmt)

    def toggle_italic(self):
        # Toggle italic formatting for the selected text
        cursor = self.editor.textCursor()
        fmt = cursor.charFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        cursor.setCharFormat(fmt)

    def toggle_underline(self):
        # Toggle italic formatting for the selected text
        cursor = self.editor.textCursor()
        fmt = cursor.charFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        cursor.setCharFormat(fmt)

    def increase_font_size(self):
        current_size = self.editor.font().pointSize()
        print(current_size)
        new_size = current_size + 1
        print(new_size)
        self.editor.setFontPointSize(new_size)

    def decrease_font_size(self):
        current_size = self.editor.font().pointSize()
        new_size = current_size - 1
        self.editor.setFontPointSize(int(new_size))

    def change_font_size(self, size):
        self.editor.setFontPointSize(int(size))

    def highlight_text(self):
        cursor = self.editor.textCursor()
        
        if cursor.hasSelection():
            # Get the current format of the selected text
            current_format = cursor.charFormat()
            
            # Create a new format, but start with the current format
            new_format = QTextCharFormat(current_format)  # Copy the current format
            
            # Toggle highlight color while preserving other properties like font size
            current_background = current_format.background().color()
            if current_background == QColor(255, 255, 0):  # Yellow
                # If currently highlighted, remove highlight
                new_format.setBackground(QColor(255, 255, 255))  # No highlight (white background)
            else:
                # If not highlighted, apply highlight
                new_format.setBackground(QColor(255, 255, 0))  # Highlight with yellow

            # Apply the new format while keeping the other properties (like font size) intact
            cursor.mergeCharFormat(new_format)
        else:
            print("No text selected to highlight.")

class EditView:
    def __init__(self):
        pass