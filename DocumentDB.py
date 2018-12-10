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
        self.conn = sqlite3.connect('documents.db', isolation_level=None)
        self.c = self.conn.cursor()
        self.locks = {}
        
        self.c.execute("SELECT id FROM documents")
        for row in self.c.fetchall():
            self.locks[row[0]] = threading.Lock()
    
    def create_tables(self, del_old=True):
        if del_old:
            self.c.execute('DROP TABLE IF EXISTS documents')
            self.c.execute('DROP TABLE IF EXISTS updates')
            self.c.execute('DROP TABLE IF EXISTS members')
        
        # Document class/model definition
        self.c.execute('''CREATE TABLE documents
                        (name TEXT, owner INTEGER, contents TEXT,
                        version INTEGER, privacy TEXT,
                        creation_date REAL,
                        locked INTEGER,
                        id INTEGER PRIMARY KEY AUTOINCREMENT
                        )''')
                        
        self.c.execute('''CREATE TABLE updates
                        (doc_id INTEGER, position INTEGER, length INTEGER, contents TEXT, id INTEGER)''')
                        
        self.c.execute('''CREATE TABLE members
                        (doc_id INTEGER, member INTEGER)''')
        self.conn.commit()
        
    def create_document(self, name, user, contents):
        self.c.execute("SELECT id FROM documents WHERE name=? AND owner=?", (name, user, ))
        if self.c.fetchone()!=None:
            # Document exists already
            return False
        self.c.execute('''INSERT INTO documents (name, contents, version, owner, creation_date, locked, id) VALUES (?, ?, ?, ?, ?, ?, NULL)''',\
            (name, contents, 0, user, time.time(), 1, ))
        
        self.conn.commit()
        self.c.execute("SELECT id FROM documents WHERE name=? AND owner=? AND version=0", (name, user, ))
        self.locks[self.c.fetchone()[0]] = threading.Lock()
        
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
            print("DOC: "+str(row[0])+", Pos: "+str(row[1])+", Length: "+str(row[2])+", Contents: "+row[3]+", ID: "+str(row[4]))
            
        return True
        
    def make_document(self, row):
        doc = DocumentModel()
        doc.docName = row[0]
        doc.owner = row[1]
        doc.contents = row[2]
        doc.versionNumber = row[3]
        doc.privacyLevel = row[4]
        doc.createDate = row[5]
        doc.locked = row[6]
        doc.doc_id = row[7]
        
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
        
    def push_update(self, update_bin):
        update = pickle.loads(update_bin.data)
        # Lock document (in database), not to be confused with the metadata lock
        lck = self.locks[update.doc_id]
        lck.acquire()
        success = True
        try:
            count = self.c.execute("SELECT COUNT(*) FROM updates WHERE doc_id=?", (update.doc_id, )).fetchone()[0]
            self.c.execute('''INSERT INTO updates (doc_id, position, length, contents, id)
                                    VALUES (?, ?, ?, ?, ?)''', (update.doc_id, update.position, update.length,\
                                                                update.contents, count + 1, ))
        finally:
            lck.release()
        
        return success
        
    def add_member(self, doc_id, member):
        self.c.execute("INSERT INTO members (doc_id, member) VALUES (?, ?)", (doc_id, member, ))
        return True
        
    def remove_member(self, doc_id, member):
        self.c.execute("DELETE FROM members WHERE doc_id=? AND member=?", (doc_id, member, ))
        return True
        
    def get_members(self, doc_id):
        self.c.execute("SELECT member FROM members WHERE doc_id=?", (doc_id,))
        res = []
        for row in self.c.fetchall():
            res.append(row[0])
        
        return pickle.dumps(res)
        
    def make_update(self, row):
        return Update(row[0], row[1], row[2], row[3], row[4])
        
    def get_updates(self, last_update):
        self.c.execute("SELECT * FROM updates WHERE id>?", (last_update,))
        updates = []
        
        for row in self.c.fetchall():
            updates.append(self.make_update(row))
            
        return pickle.dumps(updates)
        
        
class DocumentDBClient():
    def get_document(self, name, user, version=0):
        return pickle.loads(get_proxy().get_document(name, user, version).data)
    
    def set_document_lock(self, name, user, version, lock_value):
        return get_proxy().set_lock(name, user, version, lock_value)
    
    def add_member(self, doc_id, member):
        return get_proxy().add_member(doc_id, member)
        
    def remove_member(self, doc_id, member):
        return get_proxy().remove_member(doc_id, member)
        
    def get_members(self, doc_id):
        return pickle.loads(get_proxy().get_members(doc_id).data)
        
    def push_update(self, update):
        return get_proxy().push_update(pickle.dumps(update))
        
    def get_updates(self, last_update):
        return pickle.loads(get_proxy().get_updates(last_update).data)
        
    def create_document(self, name, user, contents):
        return get_proxy().create_document(name, user, contents)
        
        
doc_db = DocumentDBServer()
doc_cli = DocumentDBClient()
        
def main():
    #doc_db.create_tables()
    #doc_cli.create_document("Poopy", 0, "whoopy doop loop")
    #get_proxy().show_all_documents()
    
    print(doc_cli.get_members(1))
    print(doc_cli.add_member(1, 10))
    print(doc_cli.add_member(1, 20))
    print(doc_cli.add_member(1, 40))
    print(doc_cli.remove_member(1, 10))
    print(doc_cli.get_members(1))
    


if __name__ == '__main__':
    main()
