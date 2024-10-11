import sqlite3

class Database():
    def __init__(self, dbname="db/flashcards.db"):
        self.connection=sqlite3.connect(dbname)
        self.cursor=self.connection.cursor()
        self.createTables()
    
    def createTables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subjects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS units (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, subject_id INTEGER, FOREIGN KEY (subject_id) REFERENCES subjects(id))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, unit_id INTEGER, FOREIGN KEY (unit_id) REFERENCES units(id))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, path TEXT NOT NULL, unit_id INTEGER, FOREIGN KEY (unit_id) REFERENCES units(id))""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, answer TEXT NOT NULL, unit_id INTEGER, FOREIGN KEY (unit_id) REFERENCES units(id))""")
        self.connection.commit()
    
    def addSubject(self, subjectname):
        self.cursor.execute("INSERT INTO subjects (name) VALUES (?)",(subjectname,))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def addUnit(self, subjectid, unitname):
        self.cursor.execute("INSERT INTO units (name, subject_id) VALUES (?,?)", (unitname, subjectid))
        self.connection.commit()

    def addCard(self, question, answer, unitid):
        self.cursor.execute("INSERT INTO cards (question, answer, unit_id) VALUES(?,?,?)", (question, answer, unitid))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def getSubjects(self):
        self.cursor.execute("SELECT * FROM subjects")
        return self.cursor.fetchall()
    
    def getUnits(self, subjectid=False):
        self.cursor.execute("SELECT * FROM units WHERE subject_id = ? ", (subjectid,))
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
            return [x[0] for x in result]      
    
    def editCard(self, question, answer, cardid):
        self.cursor.execute("UPDATE cards SET question=?, answer=? WHERE id=?", (question, answer, cardid))
        self.connection.commit()
    
    def close(self):
        self.connection.close()