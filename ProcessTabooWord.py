from tkinter import*


class MemberApplication():
    def __init__(self):
        root = self.root = Toplevel()
        root.title('Process Taboo Words')
        root.geometry('370x230')
        self.taboowordSearch = []
        self.taboovar = StringVar(value=self.taboowordSearch)
        self.createWidgets()

    def createWidgets(self):
        frame1 = Frame(self.root)
        frame2 = Frame(frame1)
        frame2.grid(row=3,column=0)

        self.taboowordslist = Listbox(frame1, listvariable=self.taboovar, width=50)
        self.taboowordslist.grid(row=1, column=0, padx=5, pady=5)
        for entry in self.taboowordsSearch:
            print("entry", entry)
            self.taboowordslist.insert(entry)
        Button(frame2, text="View", font=('Ariel', 14), fg="medium blue", command=self.getTaboowords).grid(row=0, column=0,padx=2, pady=5)
        Button(frame2, text="Accept", font=('Ariel', 14), fg="medium blue", command = self.acceptTabooword).grid(row=0, column=1, padx=2, pady=5)
        Button(frame2, text="Deny", font=('Ariel', 14), fg="medium blue", command =self.deleteTabooword).grid(row=0, column=2, padx=2, pady=5)
        Button(frame2, text="Exit", font=('Ariel', 14), fg="medium blue", command = self.quit).grid(row=0, column=3, padx=2,  pady=5)

        frame1.pack()

    def getTaboowords(self):

        ## Need function to get an array of proposed Taboo Words
        for entry in self.applicationSearch:
            print("PM entry", entry)
        self.appvar.set(self.applicationSearch)

    def acceptTabooword(self):
        item = self.taboowordslist.curselection()
        idx = item[0]
        Tabooword = self.applicationSearch[idx]
        NewTabooword = Tabooword[0]

        ##Need function to update Taboo word from proposed to actual
        ## The run the getTabooWords function to put in a revised list

        self.taboovar.set(self.taboowordSearch)

    def deleteTabooword(self):
        item = self.taboowordslist.curselection()
        idx = item[0]
        Tabooword = self.applicationSearch[idx]
        DeletedTabooWord = Tabooword[0]
        ## Need function to delete the taboo word from the db
        ## Need to rerun getTabooWords function to put in a revised list

        self.taboovar.set(self.taboowordSearch)

    def quit(self):
        self.root.destroy()

    def main(self):
        Applicationgui = MemberApplication()
        Applicationgui.root.mainloop()

=======
from tkinter import*


class MemberApplication():
    def __init__(self):
        root = self.root = Toplevel()
        root.title('Process Taboo Words')
        root.geometry('370x230')
        self.taboowordSearch = []
        self.taboovar = StringVar(value=self.taboowordSearch)
        self.createWidgets()

    def createWidgets(self):
        frame1 = Frame(self.root)
        frame2 = Frame(frame1)
        frame2.grid(row=3,column=0)

        self.taboowordslist = Listbox(frame1, listvariable=self.taboovar, width=50)
        self.taboowordslist.grid(row=1, column=0, padx=5, pady=5)
        for entry in self.taboowordsSearch:
            print("entry", entry)
            self.taboowordslist.insert(entry)
        Button(frame2, text="View", font=('Ariel', 14), fg="medium blue", command=self.getTaboowords).grid(row=0, column=0,padx=2, pady=5)
        Button(frame2, text="Accept", font=('Ariel', 14), fg="medium blue", command = self.acceptTabooword).grid(row=0, column=1, padx=2, pady=5)
        Button(frame2, text="Deny", font=('Ariel', 14), fg="medium blue", command =self.deleteTabooword).grid(row=0, column=2, padx=2, pady=5)
        Button(frame2, text="Exit", font=('Ariel', 14), fg="medium blue", command = self.quit).grid(row=0, column=3, padx=2,  pady=5)

        frame1.pack()

    def getTaboowords(self):

        ## Need function to get an array of proposed Taboo Words
        for entry in self.applicationSearch:
            print("PM entry", entry)
        self.appvar.set(self.applicationSearch)

    def acceptTabooword(self):
        item = self.taboowordslist.curselection()
        idx = item[0]
        Tabooword = self.applicationSearch[idx]
        NewTabooword = Tabooword[0]

        ##Need function to update Taboo word from proposed to actual
        ## The run the getTabooWords function to put in a revised list

        self.taboovar.set(self.taboowordSearch)

    def deleteTabooword(self):
        item = self.taboowordslist.curselection()
        idx = item[0]
        Tabooword = self.applicationSearch[idx]
        DeletedTabooWord = Tabooword[0]
        ## Need function to delete the taboo word from the db
        ## Need to rerun getTabooWords function to put in a revised list

        self.taboovar.set(self.taboowordSearch)

    def quit(self):
        self.root.destroy()

    def main(self):
        Applicationgui = MemberApplication()
        Applicationgui.root.mainloop()


