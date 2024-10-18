import sqlite3
import os, sys
from bcrypt import hashpw, checkpw, gensalt
from time import perf_counter

class Database():
    def __init__(self, dbname="db/flashcards.db"):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(os.getcwd(), 'db', 'flashcards.db')
        self.connection=sqlite3.connect(db_path)
        self.cursor=self.connection.cursor()
        self.createTables()
    
    def createTables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subjects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, custom_order INTEGER NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS units (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, custom_order INTEGER NOT NULL, subject_id INTEGER, FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, content TEXT, custom_order INTEGER NOT NULL, unit_id INTEGER, FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE CASCADE)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, answer TEXT NOT NULL, unit_id INTEGER, lesson_id INTEGER, FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE CASCADE, FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, path TEXT NOT NULL, unit_id INTEGER, FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE CASCADE)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS progress (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, subject_id INTEGER,
                            unit_id INTEGER, lesson_id INTEGER, card_id INTEGER, progress_percentage INTEGER DEFAULT 0, completion_status TEXT DEFAULT 'not attempted', 
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
                            FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE CASCADE, FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE, FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE)""")
        self.connection.commit()

    def customOrder(self, table_name):
        query=f"SELECT MAX(custom_order) FROM {table_name}"
        self.cursor.execute(query)
        max_order = self.cursor.fetchone()[0]
        new_order = 1 if max_order is None else max_order + 1
        return new_order
    
    def addSubject(self, subjectname):
        custom_order=self.customOrder('subjects')
        self.cursor.execute("INSERT INTO subjects (name, custom_order) VALUES (?, ?)",(subjectname,custom_order))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def addUnit(self, subjectid, unitname):
        custom_order=self.customOrder('units')
        self.cursor.execute("INSERT INTO units (name, subject_id, custom_order) VALUES (?, ?, ?)", (unitname, subjectid, custom_order))
        self.connection.commit()

    def addLesson(self, unitid, lessoname):
        custom_order=self.customOrder('lessons')
        self.cursor.execute("INSERT INTO lessons (name, unit_id, custom_order) VALUES (?, ?, ?)", (lessoname, unitid, custom_order))
        self.connection.commit()

    def addCard(self, question, answer, unitid):
        self.cursor.execute("INSERT INTO cards (question, answer, unit_id) VALUES(?,?,?)", (question, answer, unitid))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def getSubjects(self):
        self.cursor.execute("SELECT * FROM subjects ORDER BY custom_order")
        return self.cursor.fetchall()
    
    def getUnits(self, subjectid=False):
        self.cursor.execute("SELECT * FROM units WHERE subject_id = ? ORDER BY custom_order", (subjectid,))
        return self.cursor.fetchall()
    
    def getLessons(self, unitid=False):
        self.cursor.execute("SELECT * FROM lessons WHERE unit_id = ? ORDER BY custom_order", (unitid,))
        return self.cursor.fetchall()
    
    def getLesson(self, lessonid):
        self.cursor.execute("SELECT content FROM lessons WHERE id = ? ORDER BY custom_order", (lessonid,))
        return self.cursor.fetchall()
    
    def getCard(self, cardid):
        self.cursor.execute("SELECT * FROM cards WHERE id= ?", (cardid,))
        result=self.cursor.fetchall()
        if result:
            return result
            
    def getCardIds(self, unitid):
        self.cursor.execute("SELECT id FROM cards WHERE unit_id = ? ", (unitid,))
        result=self.cursor.fetchall()
        if result:
            return [card[0] for card in result]      
    
    def editCard(self, question, answer, cardid):
        self.cursor.execute("UPDATE cards SET question=?, answer=? WHERE id=?", (question, answer, cardid))
        self.connection.commit()
    
    def editLesson(self, lessonid, content):
        self.cursor.execute("UPDATE lessons SET content=? WHERE id=?", (content, lessonid))
        self.connection.commit()

    def createNewUser(self, name, email, plainpassword):
        verify_email=self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if verify_email is not None:
            return False
        hashpassword=hashpw(plainpassword.encode('utf-8'), gensalt(12))
        self.cursor.execute("INSERT INTO users (name, email, password) VALUES(?, ?, ?)", (name, email, hashpassword))
        self.connection.commit()
        return True

    def userLogin(self, user_login_data):
        email, plainpassword = user_login_data.values()
        verify_password = self.cursor.execute("SELECT password FROM users WHERE email = ?", (email,)).fetchone()        
        if verify_password:
            if checkpw(plainpassword.encode('utf-8'), verify_password[0]):
                return True
        return False

    def close(self):
        self.connection.close()
    
    def delete(self, table_name, id):
        if table_name is None or id is None:
            return False
        query = f"DELETE FROM {table_name} WHERE id=?"
        self.cursor.execute(query, (id, ))
        self.connection.commit()
        return True