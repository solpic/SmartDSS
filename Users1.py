import sqlite3


class Users():
    def __init__(self):
        self.conn = sqlite3.connect('usertest.db')
        self.c = self.conn.cursor()

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
        # search by username
        # search by interests
        self.c.execute('SELECT username FROM t WHERE Interest1= ? OR Interest2= ? OR Interest3= ?', interest)

        return usern

    def searchUsername(self):
        # search by username
        user = (self.username,)
        for entry in self.c.execute('SELECT username FROM t WHERE username= ? ', user):
            print(entry) #push to array

    def setUser(self):
        user = (self.username,)
        self.c.execute('SELECT password FROM t WHERE username= ? ', user)
        # the SU sets the application type to OU
