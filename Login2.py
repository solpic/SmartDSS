from tkinter import*
import sqlite3

class Login():
    def __init__(self):
        root = self.root = Toplevel()
        root.title('Test')
        self.page = StringVar()
        self.loginName = StringVar()
        self.loginPass = StringVar()
        self.sts = StringVar()
        self.createWidgets()
        self.showLogin()

    def createWidgets(self):
        Label(self.root, textvariable = self.page, font=("",20)).pack()
        frame1 = Frame(self.root)
        Label(frame1,text = "Username").grid(sticky=W)
        Entry(frame1, textvariable = self.loginName).grid(row=0,column=1)
        Label(frame1, text="Password").grid(sticky=W)
        Entry(frame1, textvariable=self.loginPass, show='*').grid(row=1,column=1)
        Button(frame1, text="Log in", command=self.login).grid(row=3, pady=10)
        Button(frame1, text="Cancel", command=self.quit).grid( row=3 ,column=1)
        frame3 = Frame(self.root)
        Label(frame3, text="Logged In", font=("", 50)).pack(padx=10, pady=10)
        frame1.pack(padx = 10, pady=10)
        self.logedFrame = frame3
        self.loginFrame = frame1
        Label(self.root,textvariable =self.sts).pack()


    def login(self):
        username = self.loginName.get()
        password = self.loginPass.get()

        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        print(username)
        print(password)
        user = (username,)
        passw = (password,)
        c.execute('SELECT password FROM t WHERE username= ? ', user)
        u = c.fetchone()

        if(u == NONE):
             print("Error no username")
        if(u == passw):
             self.showLoged()
        else:
             self.sts.set("Wrong Name and Password")

    def showLoged(self):
        self.loginFrame.pack_forget()
        self.logedFrame.pack()

    def showLogin(self):
        self.page.set("Log In")
        self.loginFrame.pack()

    def quit(self):
        self.root.destroy()

#if __name__=="__main__":
    def main(self):
        loggui = Login()
        loggui.root.mainloop()
