import sqlite3
import math


class Users():
    def __init__(self):
        self.conn = sqlite3.connect('usertest.db')
        self.c = self.conn.cursor()
        self.searchList = []
        self.membershipList = []
        self.SearchInterestList = []
        #self.c.execute('''CREATE TABLE t
        #                    (username text NOT NULL PRIMARY KEY, password text, Fname text, Lname text, Interest1 text,
        #         Interest2 text, Interest3 text, joindate date, type text)''')


    def createUSer(self, username, password, Fname, Lname, Interest1, Interest2, Interest3, joindate, Application ):
        self.c.execute("INSERT INTO t VALUES (?,?,?,?,?,?,?,?,?)", (username, password, Fname, Lname, Interest1, Interest2,
                                                               Interest3, joindate, Application))
        self.conn.commit()
        for row in self.c.execute('SELECT * FROM t'):
            print(row)

    def getUsername(self, username):
        user = (username,)
        self.c.execute('SELECT username FROM t WHERE username= ? ', user)
        usern = self.c.fetchone()
        return usern

    def getPassword(self, username):
        user = (username,)
        self.c.execute('SELECT password FROM t WHERE username= ? ', user)
        passw = self.c.fetchone()
        return passw

    def searchUserInt(self, interest):
        if len(interest) <=3:
            interest = interest
        else:
            partialWordCount = math.floor(len(interest)/2)
            partialIntSearch = interest[0:partialWordCount]
            interest = partialIntSearch
        self.conn.row_factory = lambda cursor, row: row[0]
        d = self.conn.cursor()
        self.searchInterestList = d.execute('SELECT username FROM t WHERE Interest1 LIKE ?' , ('%'+ interest + '%',)).fetchall()
        self.searchInterestList.extend(d.execute('SELECT username FROM t WHERE Interest2 LIKE ?' , ('%'+ interest + '%',)).fetchall())
        self.searchInterestList.extend(d.execute('SELECT username FROM t WHERE Interest3 LIKE ?', ('%' + interest + '%',)).fetchall())
        for entry in self.searchInterestList:
            print(entry)
        return self.searchInterestList

    def searchUser(self, username):
        user = (username,)
        self.conn.row_factory = lambda cursor, row: row[0]
        d = self.conn.cursor()
        self.searchList = d.execute('SELECT username FROM t WHERE username = ?', user).fetchall()
        for entry in self.searchList:
            print(entry)
        return self.searchList

    def searchtestUser(self, username):
        user = (username,)
        self.searchList = self.c.execute('SELECT username, Interest1 FROM t WHERE username = ?', user).fetchall()
        for entry in self.searchList:
            print(entry)
        return self.searchList


    def setUser(self, username):
        user = (username,)
        self.c.execute('UPDATE t SET type = "OU" WHERE username= ? ', user)
        self.conn.commit()
        self.c.execute('SELECT * FROM t WHERE username= ? ', user)
        usern = self.c.fetchone()
        print(usern)

    def removeUser(self, username):
        user = (username,)
        self.c.execute('DELETE FROM t WHERE username= ? ', user)
        self.conn.commit()
        self.c.execute('SELECT * FROM t WHERE username= ? ', user)


    # TODO: Requested Features from Arik:
    def getRank(self, username):
        user = (username,)
        self.c.execute('SELECT type FROM t WHERE username= ? ', user)
        rank = self.c.fetchone()[0]
        print(rank)
        return rank
    #   Pre: Runs on a user instance
    #   Post: returns the rank of the user instance as a string of "OU" "GU" or "SU"

    def getInterest1(self, username):
        user = (username,)
        self.c.execute('SELECT Interest1 FROM t WHERE username= ? ', user)
        Interest1 = self.c.fetchone()[0]
        print(Interest1)
        return Interest1

    def getInterest2(self, username):
        user = (username,)
        self.c.execute('SELECT Interest2 FROM t WHERE username= ? ', user)
        Interest2 = self.c.fetchone()[0]
        print(Interest2)
        return Interest2

    def getInterest3(self, username):
        user = (username,)
        self.c.execute('SELECT Interest3 FROM t WHERE username= ? ', user)
        Interest3 = self.c.fetchone()[0]
        print(Interest3)
        return Interest3

    def getMemberAppl(self):
        type = ("GU",)
        self.membershipList = self.c.execute('SELECT username, FName, LName, Interest1, Interest2, Interest3, type FROM t WHERE type = ?', type).fetchall()
        for entry in self.membershipList:
            print(entry)
        return self.membershipList