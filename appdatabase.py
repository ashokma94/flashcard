import sqlite3

class Database():
    def __init__(self, dbname="flashcards.db"):
        self.connection=sqlite3.connect(dbname)
        self.cursor=self.connection.cursor()
        self.createTables()
    
    def createTables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subjects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lesson (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, subject_id INTEGER, FOREIGN KEY (subject_id) REFERENCES subjects(id))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, answer TEXT NOT NULL, lesson_id INTEGER, FOREIGN KEY (lesson_id) REFERENCES lessons(id))""")
        self.connection.commit()
    
    def addSubject(self, subjectname):
        self.cursor.execute("INSERT INTO subjects (name) VALUES (?)",(subjectname,))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def addLesson(self, subjectid, lessonname):
        self.cursor.execute("INSERT INTO lesson (name, subject_id) VALUES (?,?)", (lessonname, subjectid))
        self.connection.commit()

    def addCard(self, question, answer, lessonid):
        self.cursor.execute("INSERT INTO cards (question, answer, lesson_id) VALUES(?,?,?)", (question, answer, lessonid))
        self.connection.commit()
        # print(self.cursor.lastrowid)
        return self.cursor.lastrowid
    
    def getSubjects(self):
        self.cursor.execute("SELECT * FROM subjects")
        return self.cursor.fetchall()
    
    def getLessons(self, subjectid=False):
        self.cursor.execute("SELECT * FROM lesson WHERE subject_id = ? ", (subjectid,))
        # self.cursor.execute("SELECT * FROM lesson")
        return self.cursor.fetchall()
    
    def getCard(self, cardid):
        self.cursor.execute("SELECT * FROM cards WHERE id= ?", (cardid,))
        result=self.cursor.fetchall()
        if result:
            return result
            
    def getCardIds(self, lessonid):
        self.cursor.execute("SELECT id FROM cards WHERE lesson_id = ? ", (lessonid,))
        result=self.cursor.fetchall()
        if result:
            return [x[0] for x in result]      
    
    def editCard(self, question, answer, lessonid, cardid):
        self.cursor.execute("UPDATE cards SET question=?, answer=?, lesson_id=? WHERE id=?", (question, answer, lessonid, cardid))
        self.connection.commit()
    
    def close(self):
        self.connection.close()