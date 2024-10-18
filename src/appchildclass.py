# from PyQt6.QtGui import QStandardItem

# class SubjectItem(QStandardItem):
#     def __init__(self, id, name):
#         super().__init__(name)
#         self.subject_id = id  # Store the subject ID

#     def get_id(self):
#         return self.subject_id

# class LessonItem(QStandardItem):
#     def __init__(self, id, name):
#         super().__init__(name)
#         self.lesson_id = id  # Store the lesson ID

#     def get_id(self):
#         return self.lesson_id

class CardItems:
    def __init__(self, main_window):
        self.cardList=[]
        self.main_window=main_window
        self.current_index = 0  # Start at the first card
        # print("Card List", self.cardList)
    
    @property
    def current(self):
        """Return the current card."""
        # print("Current Index", self.current_index)
        if not self.cardList:
            return None  # No cards available
        return self.cardList[self.current_index]

    def prev(self):
        """Move to the previous card if available."""
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.main_window.customMessage("No more cards to show")
        return self.current  # Return the card at the new index

    def next(self):
        """Move to the next card if available."""
        if self.current_index < len(self.cardList) - 1:
            self.current_index += 1
        else:
            self.main_window.customMessage("No more cards to show")
        return self.current  # Return the card at the new index
    
    def reset(self):
        self.main_window.cards.cardList=[]
        self.current_index = 0