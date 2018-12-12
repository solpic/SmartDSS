from tkinter import*
import Users1
from DocumentDB import doc_cli

class MemberApplication():
    def __init__(self):
        root = self.root = Toplevel()
        root.title('Process Applications')
        root.geometry('370x230')
        self.applicationSearch = []
        self.appvar = StringVar(value=self.applicationSearch)
        self.createWidgets()

    def createWidgets(self):
        frame1 = Frame(self.root)
        frame2 = Frame(frame1)
        frame2.grid(row=3,column=0)

      #  Label(frame1, text="Memebership Applications", font=('Ariel', 14), fg="medium blue", width=15).grid(row=0,column=0)
        self.mapplications = Listbox(frame1, listvariable=self.appvar, width=50)
        self.mapplications.grid(row=1, column=0, padx=5, pady=5)
        for entry in self.applicationSearch:
            print("entry", entry)
            self.mapplications.insert(entry)
        Button(frame2, text="View", font=('Ariel', 14), fg="medium blue", command=self.getApplications).grid(row=0, column=0,padx=2, pady=5)
        Button(frame2, text="Accept", font=('Ariel', 14), fg="medium blue", command = self.acceptMember).grid(row=0, column=1, padx=2, pady=5)
        Button(frame2, text="Deny", font=('Ariel', 14), fg="medium blue", command =self.deleteMember).grid(row=0, column=2, padx=2, pady=5)
        Button(frame2, text="Exit", font=('Ariel', 14), fg="medium blue", command = self.quit).grid(row=0, column=3, padx=2,  pady=5)

        frame1.pack()

    def getApplications(self):
        self.applicationSearch = doc_cli.getMemberAppl()
        for entry in self.applicationSearch:
            print("PM entry", entry)
        self.appvar.set(self.applicationSearch)

    def acceptMember(self):
        item = self.mapplications.curselection()
        idx = item[0]
        memberdetail = self.applicationSearch[idx]
        username = memberdetail[0]
        self.doc_cli.setUser(username)
        self.applicationSearch = self.doc_cli.getMemberAppl()
        self.appvar.set(self.applicationSearch)

    def deleteMember(self):
        item = self.mapplications.curselection()
        idx = item[0]
        memberdetail = self.applicationSearch[idx]
        username = memberdetail[0]
        self.doc_cli.removeUser(username)
        self.applicationSearch = self.doc_cli.getMemberAppl()
        self.appvar.set(self.applicationSearch)

    def quit(self):
        self.root.destroy()

    def main(self):
        Applicationgui = MemberApplication()
        Applicationgui.root.mainloop()

