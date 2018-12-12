import sqlite3
from RPCClient import get_proxy
import threading
import time
import pickle  # serialization stuff
import DeltaObjects
import math
import TabooWords


# DocumentDBServer runs on the server and handles DB stuff
# DocumentDBClient is called by the client for all getters/setters
# Helper functions to wrap documentdbserver for RPC

# 3 most read or opened
# Get all users

class DocumentDBServer():
    def __init__(self):
        self.conn = sqlite3.connect('database.db', isolation_level=None)
        self.c = self.conn.cursor()
        self.locks = {}

        self.c.execute("SELECT id FROM documents")
        for row in self.c.fetchall():
            self.locks[row[0]] = threading.Lock()
            
    def get_all_users(self):
        self.c.execute("SELECT username FROM users")
        return pickle.dumps(self.c.fetchall())
    
    def createUSer(self, username, password, Fname, Lname, Interest1, Interest2, Interest3, joindate, Application ):
        print("Creating user: "+username)
        self.c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)", (username, password, Fname, Lname, Interest1, Interest2,
                                                               Interest3, joindate, Application))
        self.conn.commit()
        for row in self.c.execute('SELECT * FROM users'):
            print(row)

        return True

    def getUsername(self, username):
        user = (username,)
        self.c.execute('SELECT username FROM users WHERE username= ? ', user)
        usern = self.c.fetchone()
        return usern

    def getPassword(self, username):
        print("Getting password for: " + username)
        user = (username,)
        self.c.execute('SELECT password FROM users WHERE username= ? ', user)
        passw = self.c.fetchone()
        print(passw)
        print(passw[0])
        return passw

    def searchUserInt(self, interest):
        if len(interest) <= 3:
            interest = interest
        else:
            partialWordCount = math.floor(len(interest) / 2)
            partialIntSearch = interest[0:partialWordCount]
            interest = partialIntSearch
        self.conn.row_factory = lambda cursor, row: row[0]
        d = self.conn.cursor()
        self.SearchInterestList = d.execute('SELECT username FROM users WHERE Interest1 LIKE ?',
                                            ('%' + interest + '%',)).fetchall()
        self.SearchInterestList.extend(
            d.execute('SELECT username FROM users WHERE Interest2 LIKE ?', ('%' + interest + '%',)).fetchall())
        self.SearchInterestList.extend(
            d.execute('SELECT username FROM users WHERE Interest3 LIKE ?', ('%' + interest + '%',)).fetchall())
        for entry in self.SearchInterestList:
            print(entry)
        return pickle.dumps(self.SearchInterestList)

    def searchUser(self, username):
        user = (username,)
        self.conn.row_factory = lambda cursor, row: row[0]
        d = self.conn.cursor()
        self.SearchList = d.execute('SELECT username FROM users WHERE username = ?', user).fetchall()
        for entry in self.SearchList:
            print(entry)
        return pickle.dumps(self.SearchList)

    def searchtestUser(self, username):
        user = (username,)
        self.SearchList = self.c.execute('SELECT username, Interest1 FROM users WHERE username = ?', user).fetchall()
        for entry in self.SearchList:
            print(entry)
        return pickle.dumps(self.SearchList)

    def removeUser(self, username):
        user = (username,)
        self.c.execute('DELETE FROM users WHERE username= ? ', user)
        self.conn.commit()
        self.c.execute('SELECT * FROM users WHERE username= ? ', user)
        return True

    def setUser(self):
        user = (username,)
        self.c.execute('UPDATE users SET type = "OU" WHERE username= ? ', user)
        self.conn.commit()
        self.c.execute('SELECT * FROM users WHERE username= ? ', user)
        usern = self.c.fetchone()
        print(usern)
        return True

    # TODO: FIX THIS, currently doesnt work
    def getRank(self, username):
        user = (username,)
        self.c.execute('SELECT type FROM users WHERE username= ? ', user)
        rank = self.c.fetchone()[0]
        print(rank)
        return rank

    #   Pre: Runs on a user instance
    #   Post: returns the rank of the user instance as a string of "OU" "GU" or "SU"

    def getInterest1(self, username):
        user = (username,)
        self.c.execute('SELECT Interest1 FROM users WHERE username= ? ', user)
        Interest1 = self.c.fetchone()[0]
        print(Interest1)
        return Interest1

    def getInterest2(self, username):
        user = (username,)
        self.c.execute('SELECT Interest2 FROM users WHERE username= ? ', user)
        Interest2 = self.c.fetchone()[0]
        print(Interest2)
        return Interest2

    def getInterest3(self, username):
        user = (username,)
        self.c.execute('SELECT Interest3 FROM users WHERE username= ? ', user)
        Interest3 = self.c.fetchone()[0]
        print(Interest3)
        return Interest3

    def getMemberAppl(self):
        type = ("GU",)
        self.membershipList = self.c.execute('SELECT username, FName, LName, Interest1, Interest2, Interest3, type FROM users WHERE type = ?', type).fetchall()
        for entry in self.membershipList:
            print(entry)
        return pickle.dumps(self.membershipList)

    def create_tables(self, del_old=True):
        if del_old:
            self.c.execute('DROP TABLE IF EXISTS documents')
            self.c.execute('DROP TABLE IF EXISTS updates')
            self.c.execute('DROP TABLE IF EXISTS members')
            self.c.execute('DROP TABLE IF EXISTS taboo')
            self.c.execute('DROP TABLE IF EXISTS complaints')
            self.c.execute('DROP TABLE IF EXISTS users')

        # Document class/model definition
        self.c.execute('''CREATE TABLE documents
                        (name TEXT, owner TEXT, contents TEXT,
                        version INTEGER, privacy TEXT,
                        creation_date REAL,
                        locked INTEGER,
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        times_read INTEGER
                        )''')

        self.c.execute('''CREATE TABLE updates
                        (doc_id INTEGER, position INTEGER, length INTEGER, contents TEXT, id INTEGER)''')

        self.c.execute('''CREATE TABLE members
                        (doc_id INTEGER, member TEXT)''')

        self.c.execute('''CREATE TABLE taboo (word TEXT UNIQUE, status INTEGER)''')
        self.c.execute('''CREATE TABLE complaints (user TEXT, complaint TEXT)''')
        self.c.execute('''CREATE TABLE users
                            (username text NOT NULL PRIMARY KEY, password text, Fname text, Lname text, Interest1 text,
                 Interest2 text, Interest3 text, joindate date, type text)''')
        self.conn.commit()
        return True

    def create_document(self, name, user, contents):
        self.c.execute("SELECT id FROM documents WHERE name=? AND owner=?", (name, user,))
        if self.c.fetchone() != None:
            # Document exists already
            return False
        self.c.execute(
            '''INSERT INTO documents (name, contents, version, owner, creation_date, locked, id) VALUES (?, ?, ?, ?, ?, ?, NULL)''', \
            (name, contents, 0, user, time.time(), 1,))

        self.conn.commit()
        self.c.execute("SELECT id FROM documents WHERE name=? AND owner=? AND version=0", (name, user,))
        self.locks[self.c.fetchone()[0]] = threading.Lock()

        return True

    def delete_updates(self, doc_id, first, last):
        self.c.execute("DELETE FROM updates WHERE doc_id=? AND id>=? AND id<=?", (doc_id, first, last,))
        return True

    def show_all_documents(self):
        self.c.execute("SELECT * FROM documents")
        for row in self.c.fetchall():
            doc = self.make_document(row)
            doc.show()
        return True

    def show_all_users(self):
        self.c.execute("SELECT * FROM users")
        for row in self.c.fetchall():
            print("Username: " + row[0] + ", Password: " + row[1])
        return True

    def show_all_updates(self):
        self.c.execute("SELECT * FROM updates")
        for row in self.c.fetchall():
            print("DOC: " + str(row[0]) + ", Pos: " + str(row[1]) + ", Length: " + str(row[2]) + ", Contents: " + row[
                3] + ", ID: " + str(row[4]))

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
        self.c.execute("SELECT * FROM documents WHERE name=? AND owner=? AND version=?", (name, user, version,))
        row = self.c.fetchone()
        if row == None:
            return None

        doc = self.make_document(row)

        return pickle.dumps(doc)

    def set_lock(self, name, user, version, lock_value):
        self.c.execute('''UPDATE documents SET locked=? WHERE name=? AND owner=? AND version=?''',
                       (lock_value, name, user, version,))
        # Check if successful
        self.c.execute("SELECT locked FROM documents WHERE name=? AND owner=? AND version=?", (name, user, version,))
        return self.c.fetchone()[0]

    def push_update(self, doc_id, location, contents, length):
        # Lock document (in database), not to be confused with the metadata lock
        lck = self.locks[doc_id]
        lck.acquire()
        success = True
        try:
            count = self.c.execute("SELECT COUNT(*) FROM updates WHERE doc_id=?", (doc_id,)).fetchone()[0]
            self.c.execute('''INSERT INTO updates (doc_id, position, length, contents, id)
                                    VALUES (?, ?, ?, ?, ?)''', (doc_id, location, length, \
                                                                contents, count + 1,))
        finally:
            lck.release()

        return success

    def add_member(self, doc_id, member):
        self.c.execute("INSERT INTO members (doc_id, member) VALUES (?, ?)", (doc_id, member,))
        return True

    def remove_member(self, doc_id, member):
        self.c.execute("DELETE FROM members WHERE doc_id=? AND member=?", (doc_id, member,))
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

    def delete_complaint(self, complaint):
        self.c.execute("DELETE FROM complaints WHERE complaint=?", (complaint,))
        return True

    def add_complaint(self, user, complaint):
        self.c.execute("INSERT INTO complaints (user, complaint) VALUES (?, ?)", (user, complaint,))
        return True


class DocumentDBClient():
    def show_all_users(self):
        get_proxy().show_all_users()

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
        if row[3] == "":
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

    def searchUserInt(self, interest):
        return pickle.loads(get_proxy().searchUserInt(interest).data)

    def searchUser(self, username):
        return pickle.loads(get_proxy().searchUser(username).data)

    def searchtestUser(self, username):
        return pickle.loads(get_proxy().searchtestUser(username).data)

    def createUSer(self, username, password, Fname, Lname, Interest1, Interest2, Interest3, joindate, Application):
        return get_proxy().createUSer(username, password, Fname, Lname, Interest1, Interest2, Interest3, joindate,
                                      Application)

    def getUsername(self, username):
        return get_proxy().getUsername(username)

    def getPassword(self, username):
        return get_proxy().getPassword(username)

    def setUser(self, username):
        return get_proxy().setUser(username)
        
    def removeUser(self, username):
        return get_proxy().removeUser(username)

    def removeUser(self, username):
        return get_proxy().removeUser(username)

    def getRank(self, username):
        return get_proxy().getRank(username)

    def getInterest1(self, username):
        return get_proxy().getInterest1(username)

    def getInterest2(self, username):
        return get_proxy().getInterest2(username)

    def getInterest3(self, username):
        return get_proxy().getInterest3(username)

    def getMemberAppl(self):
        return pickle.loads(get_proxy().getMemberAppl().data)


doc_cli = DocumentDBClient()


def main():
    get_proxy().create_tables()
    doc_cli.createUSer("me", "me", "me", "me", "python", "audio", "math", 1, "SU")

if __name__ == '__main__':
    main()
