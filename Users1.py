import sqlite3
import math


class Users():
    def __init__(self):
        self.conn = sqlite3.connect('usertest.db')
        self.c = self.conn.cursor()
        self.SearchList = []
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
        self.SearchInterestList = d.execute('SELECT username FROM t WHERE Interest1 LIKE ?' , ('%'+ interest + '%',)).fetchall()
        self.SearchInterestList.extend(d.execute('SELECT username FROM t WHERE Interest2 LIKE ?' , ('%'+ interest + '%',)).fetchall())
        self.SearchInterestList.extend(d.execute('SELECT username FROM t WHERE Interest3 LIKE ?', ('%' + interest + '%',)).fetchall())
        for entry in self.SearchInterestList:
            print(entry)
        return self.SearchInterestList


    def searchUser(self, username):
        user = (username,)
        self.conn.row_factory = lambda cursor, row: row[0]
        d = self.conn.cursor()
        self.SearchList = d.execute('SELECT username FROM t WHERE username = ?', user).fetchall()
        for entry in self.SearchList:
            print(entry)
        return self.SearchList

    def setUser(self):
        user = (self.username,)
        self.c.execute('SELECT password FROM t WHERE username= ? ', user)
        # the SU sets the application type to OU

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