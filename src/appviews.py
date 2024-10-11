from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt

class FlashCardView(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)

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
        self.setMaximumWidth(200)
        self.prevSelectedUnitId=None
        # Populate the tree with initial data
        self.populate_tree()

        # Connect the itemClicked signal to a slot
        self.itemClicked.connect(self.on_item_selected)

    def populate_tree(self, current_subject_id=None):
        self.clear()  # Clear the existing items

        subjects = self.main_window.actions.database.getSubjects()  # Fetch subjects from the database
        for subject_id, subject_name in subjects:
            subject_item = QTreeWidgetItem(self, [subject_name])
            subject_item.setData(0, Qt.ItemDataRole.UserRole, subject_id)  # Store subject ID in the item

            # Expand only the current subject if it's provided
            if current_subject_id is not None and subject_id == current_subject_id:
                subject_item.setExpanded(True)  # Expand the current subject

            units = self.main_window.actions.database.getUnits(subject_id)  # Fetch lessons for the subject
            for unit_id, unit_name, subject_id in units:
                unit_item = QTreeWidgetItem(subject_item, [unit_name])
                unit_item.setData(0, Qt.ItemDataRole.UserRole, unit_id)  # Store lesson ID in the item

    def on_item_selected(self, item, column):
        # This method is called whenever an item is clicked
        if item is None or item.parent() is None:
            return
        # You can get the item data here
        item_id = item.data(0, Qt.ItemDataRole.UserRole)  # Get the ID associated with the item
        item_text = item.text(0)  # Get the text of the clicked item

        if item_id==self.prevSelectedUnitId:
            return

        # print(f"Selected item: {item_text}, ID: {item_id}")
        self.main_window.right_panel.resetWindow()
        card_id_list = self.main_window.actions.getCardIdList(item_id)
        self.main_window.cards.cardList= card_id_list if card_id_list is not None else []
        self.main_window.right_panel.showCard()
        self.prevSelectedUnitId=item_id