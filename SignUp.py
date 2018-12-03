from tkinter import*
from tkinter import messagebox
from datetime import date
import Users1
import sqlite3

class SignUp():
    def __init__(self):
        root = self.root = Toplevel()
        root.title('Test')
        self.page = StringVar()

        self.var1 = StringVar()
        self.InList = ["Python","Java", "C++", "JavaScript"]
        self.var2 = StringVar()
        self.InList2 = ["Math", "Science", "Technology", "Engineering"]
        self.var3 = StringVar()
        self.InList3 = ["AI", "Machine Learning", "Programming", "Blockchain", "Gaming",
                        "Web development"]
        self.signupName = StringVar()
        self.signupPass = StringVar()
        self.signupFnam = StringVar()
        self.signupLnam = StringVar()
        self.sts = StringVar()
        self.createWidgets()
        self.showSignup()


    def createWidgets(self):
        Label(self.root, textvariable = self.page, font=("",20)).pack()
        frame1 = Frame(self.root)
        Label(frame1, text="Username").grid(sticky=W)
        Entry(frame1, textvariable=self.signupName).grid(row=0, column=1,padx=10,pady=10)
        Label(frame1, text="Password").grid(sticky=W)
        Entry(frame1, textvariable = self.signupPass, show='*').grid(row=1,column=1)
        Label(frame1, text="First name").grid(sticky=W)
        Entry(frame1, textvariable=self.signupFnam).grid(row=2, column=1, padx=10, pady=10)
        Label(frame1, text="Last name").grid(sticky=W)
        Entry(frame1, textvariable=self.signupLnam).grid(row=3, column=1)
        Label(frame1, text="Technical Interest").grid(sticky=W)
        Label(frame1, text="Technical Interest").grid(sticky=W)
        Label(frame1, text="Technical Interest").grid(sticky=W)
        self.var1.set(self.InList[0])
        it1 = OptionMenu(frame1, self.var1, *self.InList)
        it1.grid(row=4, column=1)
        it1.config(width=14)
        self.var2.set(self.InList2[0])
        it2 = OptionMenu(frame1, self.var2, *self.InList2)
        it2.grid(row=5, column=1)
        it2.config(width=14)
        self.var3.set(self.InList3[0])
        it3 = OptionMenu(frame1, self.var3, *self.InList3)
        it3.grid(row=6, column=1)
        it3.config(width=14)
        Button(frame1, text="Request", command=self.create).grid(pady=10)
        Button(frame1, text="Cancel", command=self.quit).grid(row=7, column=1)

        self.signinFrame= frame1
        Label(self.root,textvariable =self.sts).pack()

    def showSignup(self):
        self.page.set("Sign Up")
        self.signinFrame.pack()

    def create(self):
        username = self.signupName.get()
        password = self.signupPass.get()
        Fname = self.signupFnam.get()
        Lname = self.signupLnam.get()
        Interest1 = self.var1.get()
        Interest2 = self.var2.get()
        Interest3 = self.var3.get()
        joindate = str(date.today())
        Application = 'GU'

        x1 = Users1.Users()
        usern = x1.getUsername(username)
        username1 = (username,)

      #  c.execute('''CREATE TABLE t
      #              (username text NOT NULL PRIMARY KEY, password text, Fname text, Lname text, Interest1 text,
      #   Interest2 text, Interest3 text, joindate date, type text)''')


        if(username == "" ):
            messagebox.showwarning("Warning",
                                   "Application needs all items to be completed to be successfully submitted")

        elif(password ==""):
            messagebox.showwarning("Warning",
                                   "Application needs all items to be completed to be successfully submitted")

        elif(Fname == ""):
            messagebox.showwarning("Warning",
                                   "Application needs all items to be completed to be successfully submitted")

        elif (username1 == usern):
            messagebox.showwarning("Warning",
                                   "Username already taken. Please try another one")
            self.signinFrame.destroy()
        else:
            x1 = Users1.Users()
            userEntry = x1.createUSer(username, password, Fname, Lname, Interest1, Interest2, Interest3, joindate,
                                      Application)
            self.quit()

    def quit(self):
        self.root.destroy()

    def main(self):
        signgui= SignUp()
        signgui.root.mainloop()


