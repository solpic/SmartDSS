import sqlite3

class Users():
    def create_tables(self):
        self.c.execute("DROP TABLE IF EXISTS users")
        self.c.execute('''CREATE TABLE users
                            (username text NOT NULL PRIMARY KEY, password text, Fname text, Lname text, Interest1 text,
                 Interest2 text, Interest3 text, joindate date, type text)''')
                 
    def __init__(self):      
        self.conn = sqlite3.connect('database.db', isolation_level=None)
        self.c = self.conn.cursor()
        
        
        
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
        # search by username
        # search by interests
        self.c.execute('SELECT username FROM users WHERE Interest1= ? OR Interest2= ? OR Interest3= ?', interest)

        return usern

    def searchUsername(self):
        # search by username
        user = (self.username,)
        for entry in self.c.execute('SELECT username FROM users WHERE username= ? ', user):
            print(entry) #push to array

    def setUser(self):
        user = (self.username,)
        self.c.execute('SELECT password FROM users WHERE username= ? ', user)
        # the SU sets the application type to OU

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
        

def main():
    user_db = Users()
    user_db.create_tables()
    
if __name__ == '__main__':
    main()

