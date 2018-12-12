import sqlite3
import math
import pickle

class Users():
    def __init__(self, conn, c):
        self.conn = conn
        self.c = c
        self.SearchList = []
        self.SearchInterestList = []


    def createUSer(self, username, password, Fname, Lname, Interest1, Interest2, Interest3, joindate, Application ):
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
        user = (username,)
        self.c.execute('SELECT password FROM users WHERE username= ? ', user)
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
        self.SearchInterestList = d.execute('SELECT username FROM users WHERE Interest1 LIKE ?' , ('%'+ interest + '%',)).fetchall()
        self.SearchInterestList.extend(d.execute('SELECT username FROM users WHERE Interest2 LIKE ?' , ('%'+ interest + '%',)).fetchall())
        self.SearchInterestList.extend(d.execute('SELECT username FROM users WHERE Interest3 LIKE ?', ('%' + interest + '%',)).fetchall())
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


    def setUser(self):
        user = (self.username,)
        self.c.execute('SELECT password FROM users WHERE username= ? ', user)
        # the SU sets the application type to OU
        return None

    # TODO: Requested Features from Arik:
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
        self.membershipList = self.c.execute('SELECT username, FName, LName, Interest1, Interest2, Interest3, type FROM t WHERE type = ?', type).fetchall()
        for entry in self.membershipList:
            print(entry)
        return self.membershipList
