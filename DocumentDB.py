import sqlite3
from RPCClient import get_proxy
import threading
import time
import pickle #serialization stuff
import DeltaObjects
import TabooWords

# DocumentDBServer runs on the server and handles DB stuff
# DocumentDBClient is called by the client for all getters/setters
# Helper functions to wrap documentdbserver for RPC

class DocumentDBServer():
    def __init__(self):
        self.conn = sqlite3.connect('database.db', isolation_level=None)
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
            self.c.execute('DROP TABLE IF EXISTS taboo')
            self.c.execute('DROP TABLE IF EXISTS complaints')
        
        # Document class/model definition
        self.c.execute('''CREATE TABLE documents
                        (name TEXT, owner TEXT, contents TEXT,
                        version INTEGER, privacy TEXT,
                        creation_date REAL,
                        locked INTEGER,
                        id INTEGER PRIMARY KEY AUTOINCREMENT
                        )''')
                        
        self.c.execute('''CREATE TABLE updates
                        (doc_id INTEGER, position INTEGER, length INTEGER, contents TEXT, id INTEGER)''')
                        
        self.c.execute('''CREATE TABLE members
                        (doc_id INTEGER, member TEXT)''')
                        
        self.c.execute('''CREATE TABLE taboo (word TEXT UNIQUE, status INTEGER)''')
        self.c.execute('''CREATE TABLE complaints (user TEXT, complaint TEXT)''')
        self.conn.commit()
        return True
        
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

    def delete_updates(self, doc_id, first, last):
        self.c.execute("DELETE FROM updates WHERE doc_id=? AND id>=? AND id<=?", (doc_id, first, last, ))
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
        from DocumentModel import DocumentModel
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
        
    def push_update(self, doc_id, location, contents, length):
        # Lock document (in database), not to be confused with the metadata lock
        lck = self.locks[doc_id]
        lck.acquire()
        success = True
        try:
            count = self.c.execute("SELECT COUNT(*) FROM updates WHERE doc_id=?", (doc_id, )).fetchone()[0]
            self.c.execute('''INSERT INTO updates (doc_id, position, length, contents, id)
                                    VALUES (?, ?, ?, ?, ?)''', (doc_id, location, length,\
                                                                contents, count + 1, ))
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
        self.c.execute("SELECT member FROM members WHERE doc_id=? ORDER BY id ASC", (doc_id,))
        res = []
        for row in self.c.fetchall():
            res.append(row[0])
        
        return pickle.dumps(res)
        
    def get_all_documents(self):
        self.c.execute("SELECT * FROM documents")
        return pickle.dumps(self.c.fetchall())
        
    def get_updates(self, doc_id, last_update):
        self.c.execute("SELECT * FROM updates WHERE doc_id=? AND id>?", (doc_id, last_update,))
        
        updates = []
        
        for row in self.c.fetchall():
            updates.append(row)
        
        return pickle.dumps(updates)
        
    def add_taboo_word(self, word):
        self.c.execute("INSERT INTO taboo (word, status) VALUES (?, ?)", (word, 0,))
        return True
        
    def get_taboo_words(self):
        self.c.execute("SELECT * FROM taboo")
        return pickle.dumps(self.c.fetchall())
        
    def accept_taboo_word(self, word):
        self.c.execute("UPDATE taboo SET status=1 WHERE word=? AND status=0", (word,))
        return True
        
    def delete_taboo_word(self, word):
        self.c.execute("DELETE FROM taboo WHERE word=?", (word,))
        return True
        
    def get_complaints(self):
        self.c.execute("SELECT * FROM complaints")
        return pickle.dumps(self.c.fetchall())
        
    def delete_complaint(self, user, complaint):
        self.c.execute("DELETE FROM complaints WHERE user=? AND complaint=?", (user, complaint, ))
        return True
        
    def add_complaint(self, user, complaint):
        self.c.execute("INSERT INTO complaints (user, complaint) VALUES (?, ?)", (user, complaint, ))
        return True
        
        
class DocumentDBClient():
    def make_document(self, row):
        from DocumentModel import DocumentModel
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
    def make_update(self, row):
        if row[3]=="":
            # Deletion
            return DeltaObjects.Delete(row[1], row[2], row[4])
        else:
            return DeltaObjects.Insert(row[1], row[3], row[4])
            
    def get_all_documents(self):
        rows = pickle.loads(get_proxy().get_all_documents().data)
        docs = []
        for row in rows:
            docs.append(self.make_document(row))
        return docs
        
    def show_all_updates(self):
        get_proxy().show_all_updates()
        
            
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
        
    def push_insert(self, doc_id, insert):
        return get_proxy().push_update(doc_id, insert.location, insert.string, 0)
        
    def push_delete(self, doc_id, delete):
        return get_proxy().push_update(doc_id, delete.location, "", delete.length)
        
    def get_updates(self, doc_id, last_update):
        updates = pickle.loads(get_proxy().get_updates(doc_id, last_update).data)
        ret = []
        for update in updates:
            ret.append(self.make_update(update))
            
        return ret
        
    def create_document(self, name, user, contents):
        return get_proxy().create_document(name, user, contents)
        
    def add_taboo_word(self, word):
        return get_proxy().add_taboo_word(word)
        
    def get_taboo_words(self):
        words = pickle.loads(get_proxy().get_taboo_words().data)
        
        ret = []
        for w in words:
            ret.append(TabooWords.TabooWord(w[0], w[1]))
            
        return ret
        
    def accept_taboo_word(self, word):
        return get_proxy().accept_taboo_word(word)
        
    def delete_taboo_word(self, word):
        return get_proxy().delete_taboo_word(word)
        
    def get_complaints(self):
        from Complaint import Complaint
        complaints = pickle.loads(get_proxy().get_complaints().data)
        ret = []
        for c in complaints:
            ret.append(Complaint(c[1], c[0]))
        return ret
        
    def delete_complaint(self, user, complaint):
        return get_proxy().delete_complaint(user, complaint)
        
    def add_complaint(self, user, complaint):
        return get_proxy().add_complaint(user, complaint)
        
        
doc_cli = DocumentDBClient()
        
def main():
    #get_proxy().create_tables()
    doc_cli.delete_complaint("Fred", "Water sucks")
    
    complaints = doc_cli.get_complaints()
    for c in complaints:
        c.show()
    

if __name__ == '__main__':
    main()
