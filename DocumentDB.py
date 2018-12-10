import sqlite3
from DocumentModel import DocumentModel
from RPCClient import get_proxy
from Update import Update
import threading
import time
import pickle #serialization stuff

# DocumentDBServer runs on the server and handles DB stuff
# DocumentDBClient is called by the client for all getters/setters
# Helper functions to wrap documentdbserver for RPC

class DocumentDBServer():
    def __init__(self):
        self.conn = sqlite3.connect('documents.db')
        self.c = self.conn.cursor()
        self.locks = {}
        
        self.c.execute("SELECT name, owner, version FROM documents")
        for row in self.c.fetchall():
            self.locks[row[0]+row[1]+str(row[2])] = threading.Lock()
        
    def create_tables(self, del_old=True):
        if del_old:
            self.c.execute('DROP TABLE IF EXISTS documents')
            self.c.execute('DROP TABLE IF EXISTS updates')
        
        # Document class/model definition
        self.c.execute('''CREATE TABLE documents
                        (name TEXT, owner TEXT, contents TEXT,
                        version INTEGER, privacy TEXT,
                        creation_date REAL,
                        locked INTEGER
                        )''')
                        
        self.c.execute('''CREATE TABLE updates
                        (doc_id INTEGER, position INTEGER, length INTEGER, contents TEXT, id INTEGER)''')
                        
        self.conn.commit()
        
    def create_document(self, name, user, contents):
        self.c.execute('''INSERT INTO documents (name, contents, version, owner, creation_date, locked) VALUES (?, ?, ?, ?, ?, ?)''',\
            (name, contents, 0, user, time.time(), 1, ))
        
        self.conn.commit()
        self.locks[name+user+'0'] = threading.Lock()
        
        return True
        
    def show_all_documents(self):
        self.c.execute("SELECT * FROM documents")
        for row in self.c.fetchall():
            doc = self.make_document(row)
            doc.show()
        return True
        
    def show_all_updates(self):
        self.c.execute("SELECT * FROM updates")
        for row in self.c.fetchall():
            print("DOC: "+row[0]+", Pos: "+row[1]+", Length: "+row[2]+", Contents: "+row[3]+", ID: "+row[4])
        
    def make_document(self, row):
        doc = DocumentModel()
        doc.docName = row[0]
        doc.owner = row[1]
        doc.contents = row[2]
        doc.versionNumber = row[3]
        doc.privacyLevel = row[4]
        doc.createDate = row[5]
        doc.locked = row[6]
        
        return doc
        
    def get_document(self, name, user, version):
        self.c.execute("SELECT * FROM documents WHERE name=? AND owner=? AND version=?", (name, user, version, ))
        row = self.c.fetchone()
        if row==None:
            return None
            
        doc = self.make_document(row)
       
        return pickle.dumps(doc)
    
    def set_lock(self, name, user, version, lock_value):
        self.c.execute('''UPDATE documents SET locked=? WHERE name=? AND owner=? AND version=?''', (lock_value, name, user, version, ))
        # Check if successful
        self.c.execute("SELECT locked FROM documents WHERE name=? AND owner=? AND version=?", (name, user, version, ))
        return self.c.fetchone()[0]
        
    def push_update(self, name, user, version, update_bin):
        update = pickle.loads(update_bin.data)
        # Lock document (in database), not to be confused with the metadata lock
        lck = self.locks[name+user+str(version)]
        lck.acquire()
        try:
            count = self.c.execute("SELECT COUNT(*) FROM updates").fetchone()[0]
            doc_id = self.c.execute("SELECT
        finally:
            lck.release()
        
        return True
        
class DocumentDBClient():
    def get_document(self, name, user, version=0):
        return pickle.loads(get_proxy().get_document(name, user, version).data)
    
    def set_document_lock(self, name, user, version, lock_value):
        return get_proxy().set_lock(name, user, version, lock_value)
        
    def push_update(self, name, user, version, update):
        return get_proxy().push_update(name, user, version, pickle.dumps(update))
        
    def create_document(self, name, user, contents):
        return get_proxy().create_document(name, user, contents)
        
        
doc_db = DocumentDBServer()
doc_client = DocumentDBClient()
        
def main():
    #doc_db.create_tables()
    #doc_client.create_document("Poopy", "Fred", "whoopy doop loop")
   # print(get_proxy().return_square(10))
    #d = doc_client.get_document("Poopy", "Fred", 0)
    #print(doc_client.set_document_lock("Poopy", "Fred", 0, 0))
    u = Update(5, 0, "Hello")
    doc_client.push_update("Poopy", "Fred", 0, u)
    get_proxy().show_all_documents()
    get_proxy().show_all_updates()
   #print(get_proxy().foofy(10))


if __name__ == '__main__':
    main()
