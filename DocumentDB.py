import sqlite3
from DocumentModel import DocumentModel
import time

class DocumentDB():
    def __init__(self):
        self.conn = sqlite3.connect('documents.db')
        self.c = self.conn.cursor()
        
    def create_tables(self, del_old=True):
        if del_old:
            self.c.execute('DROP TABLE IF EXISTS documents')
            self.c.execute('DROP TABLE IF EXISTS doc_changes')
        
        # Document class/model definition
        self.c.execute('''CREATE TABLE documents
                        (name TEXT, owner TEXT, contents TEXT,
                        version INTEGER, privacy TEXT,
                        creation_date REAL,
                        locked INTEGER
                        )''')
                        
        self.c.execute('''CREATE TABLE doc_changes
                        (doc_id INTEGER, position INTEGER, is_deletion INTEGER, contents TEXT, id INTEGER)''')
                        
        self.conn.commit()
        
    def create_document(self, name, user, contents):
        self.c.execute('''INSERT INTO documents (name, contents, version, owner, creation_date, locked) VALUES (?, ?, ?, ?, ?, ?)''',\
            (name, contents, 0, user, time.time(), 1, ))
        
        self.conn.commit()
        
    def get_document(self, name, user):
        self.c.execute("SELECT * FROM documents")# WHERE name=? AND owner=?", (name, user, ))
        row = self.c.fetchone()
        if row==None:
            return None
            
        doc = DocumentModel()
        doc.docName = row[0]
        doc.owner = row[1]
        doc.contents = row[2]
        doc.versionNumber = row[3]
        doc.privacyLevel = row[4]
        doc.createDate = row[5]
        doc.locked = row[6]
       
        return doc
        
        
        
docs = DocumentDB()
docs.create_tables()
docs.create_document("Poopy",  "Fred",'''Poopy made poopy pants everyday''')
print(docs.get_document("Poopy", "Fred"))
