from tkinter import *
from DocumentDB import doc_cli
import Users1
import DocumentFileTest
from DocumentScreenTester import user
import ProcessMember
import ProcessTabooWord
import ProcessComplaints
#import createfilepopup
import datetime
import DocumentFileTest
from DocumentScreenTester import user

## This UserPage is specific to the user. It holds all the main functions of the system
## From this page the user can create documents, search for documents, open documents
## If the user has a rank of SU they have additional buttons to process member applications, complaints and taboo words
## To see this page the user must be a member with a valid username and password and rank of OU or SU

class UserPg():

    def __init__(self, parent, username):
        self.user = username
        self.parent = parent
        self.frame1 = Frame(self.parent)
        self.parent.title("")
        self._geom = '800x800+0+0'
        parent.geometry("{0}x{1}+0+0".format(
            parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.parent.configure(background="white")

        self.rank = doc_cli.getRank(username)
        self.memberName = StringVar()
        self.memberInt = StringVar()
        self.docName = StringVar()
        self.memberSearch = []
        self.interestsSearch = []
        self.documentSearch = []
        self.activedoc = ""
        self.invar = StringVar(value=self.interestsSearch)
        self.var = StringVar(value=self.memberSearch)
        self.docvar = StringVar(value=self.documentSearch)
        self.Interest1 = doc_cli.getInterest1(username)
        self.Interest2 = doc_cli.getInterest2(username)
        self.Interest3 = doc_cli.getInterest3(username)
        self.recentDoc1tite = "Document 1"
        self.recentDoc1tite = "Document 1"
        self.recentDoc1tite = "Document 1"
        self.userDocs = []
        self.getDocs()
        self.createWidget()

# This function creates all the GUI for the user page and holds calls to the functions
    def createWidget(self):
        self.frame1.configure(background="white")
        frame2 = Frame(self.frame1)
        frame2.config(width=100)
        frame2.pack(fill=X, expand=True)
        frame3 = Frame(self.frame1)
        frame3.pack(fill=X, expand=True)
        frame4 = Frame(self.frame1)
        frame4.pack(fill=X, expand=True)
        frame5 = Frame(frame4)
        frame5.pack(side=LEFT, fill=X)
        frame6 = Frame(frame4)
        frame6.pack(side=LEFT, fill=X)
        frame7 = Frame(frame4)
        frame7.pack(side=LEFT, fill=X)
        frame8 = Frame(frame4)
        frame8.pack(side=LEFT, fill=X)

        UsernameText = self.user
        Label(frame2, text=UsernameText , font=('Ariel', 34), fg="medium blue",
              background="white").grid(row=0, column=0, padx=10, pady=20)

        img = self.getImage()
        profile = Label(frame5, image=img)
        profile.image = img
        profile.grid(row=0, column=0, pady=10)

        Label(frame5, text="Interests", font=('Ariel', 30), fg="medium blue").grid(
            row=1, column=0, pady=10)
        Label(frame5, text=self.Interest1, font=('Ariel', 26), fg="medium blue") \
            .grid(row=2, column=0, padx=20, sticky=W)
        Label(frame5, text=self.Interest2, font=('Ariel', 26), fg="medium blue") \
            .grid(row=3, column=0, padx=20, sticky=W)
        Label(frame5, text=self.Interest3, font=('Ariel', 26), fg="medium blue"). \
            grid(row=4, column=0, padx=20, sticky=W)

        Button(frame3, text="create document", font=('Ariel', 30), fg="medium blue", background="white",
               command=self.createnewdoc).grid(row=0, column=0, padx=10, pady=10)
        if len(self.userDocs)>0:
            Button(frame3, text=self.userDocs[0][0], command = self.openDoc1, font=('Ariel', 30), fg="medium blue", background="white", width=15).grid( row=0, column=1, padx=20)
        if len(self.userDocs)>1:
            Button(frame3, text=self.userDocs[1][0], command = self.openDoc2, font=('Ariel', 30), fg="medium blue", background="white", width=15).grid(row=0,column=2, padx=10)
        if len(self.userDocs)>2:
            Button(frame3, text=self.userDocs[2][0], command= self.openDoc3, font=('Ariel', 30), fg="medium blue", background="white", width=15).grid(row=0, column=3,  padx=10)

        Label(frame6, text="Search Members by Username", font=('Ariel', 16), fg="medium blue", width=24).grid(row=0, column=0)
        Entry(frame6, textvariable=self.memberName, width=50).grid(row=1, column=0, sticky=E, padx=10)

        simg = PhotoImage(file="images.gif")
        searchpic1 = Button(frame6, image=simg, command=self.memSearch)
        searchpic1.image = simg
        searchpic1.grid(row=1, column=1)
        searchResults = Listbox(frame6, listvariable=self.var, width=50).grid(row=2, column=0, sticky=E, padx=10)
        for entry in self.memberSearch:
            searchResults.insert(entry)

        Label(frame6, text="Search Members by Interests", font=('Ariel', 18), fg="medium blue", width=22).grid(row=3,                                                                                                        column=0)
        Entry(frame6, textvariable=self.memberInt, width=50).grid(row=4, column=0, sticky=E, padx=10)
        searchpic2 = Button(frame6, image=simg, command=self.intSearch)
        searchpic2.image = simg
        searchpic2.grid(row=4, column=1)
        searchResultInt = Listbox(frame6, listvariable=self.invar, width=50).grid(row=5, column=0, sticky=E, padx=10)
        for entry in self.interestsSearch:
            searchResultInt.insert(entry)

        Label(frame7, text="Search Documents", font=('Ariel', 26), fg="medium blue", width=15).grid(
            sticky=E)
        Entry(frame7, textvariable=self.docName, width=50).grid(row=1, column=0, sticky=E, padx=10)
        simg = PhotoImage(file="images.gif")
        searchpicD = Button(frame7, image=simg, command=self.docSearch)
        searchpicD.image = simg
        searchpicD.grid(row=1, column=1)
        self.searchResultDocs = Listbox(frame7, listvariable=self.docvar, width=50)
        self.searchResultDocs.grid(row=2, column=0, sticky=E, padx=10)
        for entry in self.documentSearch:
            print("entry", entry)
        Button(frame7, text="Open Document", font=('Ariel', 24), fg="medium blue", width=16, background="white",
               command=self.opendocument).grid(row=3, column=0, pady=5)
        Label(frame7, height=12).grid(row=5, column=0)

        if self.rank == 'SU':
            Button(frame8, text="Process Complaints", font=('Ariel', 24), fg="medium blue", background="white", command = self.processComplaint).grid(
                row=1, column=1, padx=30, pady=40, sticky=E)
            Button(frame8, text="Process Taboo Words", font=('Ariel', 24), fg="medium blue", background="white", command = self.processTaboo).grid(
                row=3, column=1, padx=30, pady=40, sticky=E)
            Button(frame8, text="Process Applications", font=('Ariel', 24), fg="medium blue", background="white",
                   command=self.processApl).grid(row=5, column=1, padx=30, pady=40, sticky=E)
        elif self.rank == 'OU':
            docimg = PhotoImage(file="docSharing.gif")
            OUdocpic = Label(frame8, image=docimg)
            OUdocpic.image = docimg
            OUdocpic.grid(row=1, column=1)

        self.frame1.pack()

    def getImage(self):
        if (self.rank == 'SU' and self.Interest1 == "Python"):
            img = PhotoImage(file="testgirl.gif")
        elif (self.rank == 'OU' and self.Interest1 == "Python"):
            img = PhotoImage(file="testboy.gif")
        elif (self.rank == "SU" ):
            img = PhotoImage(file="SU.gif")
        else:
            img = PhotoImage(file="Fred.gif")
        return img

# This function searches for a Member based on name
    def memSearch(self):
        user = self.memberName.get()
        self.memberSearch = doc_cli.searchUser(user)
        self.var.set(self.memberSearch)

# This function searches for a member based on Interests
    def intSearch(self):
        user = self.memberInt.get()
        self.interestsSearch = doc_cli.searchUserInt(user)
        self.invar.set(self.interestsSearch)

#This function searches for documents based on title
    def docSearch(self):
        docs = doc_cli.get_all_documents()
        searchItem = self.docName.get()

        names = []
        for doc in docs:
            if searchItem in doc.docName:
                entry = (doc.docName, doc.owner, doc.versionNumber)
                names.append(entry)
        self.documentSearch = names
        self.docvar.set(names)

#This function gets the user documents to show his/her 3 most recent
    def getDocs(self):
        docs = doc_cli.get_all_documents()
        names = []
        for doc in docs:
            if self.user in doc.owner:
                entry = (doc.docName, doc.owner, doc.versionNumber, doc.createDate)
                self.userDocs.append(entry)
        #sort this array
        self.userDocs.sort(key=self.sortdate)
        for doc in docs:
            if self.user not in doc.owner:
                entry = (doc.docName, doc.owner, doc.versionNumber, doc.createDate)
                self.userDocs.append(entry)
        for doc in docs:
            entry = (doc.docName, doc.owner, doc.versionNumber, doc.createDate)
            names.append(entry)

    def sortdate(self, val):
        return val[3]

# Function to create a new document
    def createnewdoc(self):
        print("new document")
        from tkinter import simpledialog
        doc_name = simpledialog.askstring("Document Name", "Name of new document?")
        versionNo = 0
        init_contents = ""
        doc_cli.create_document(doc_name, self.user, init_contents)
        doc_cli.get_document(doc_name, self.user, versionNo)
        DocumentFileTest.DocumentScreen(user(user), doc_cli.get_document(doc_name, self.user, versionNo))

#Function to open a document
    def opendocument(self):
        item = self.searchResultDocs.curselection()
        idx = item[0]
        docdetail = self.documentSearch[idx]
        document = docdetail[0]
        usern = docdetail[1]
        versionNo = docdetail[2]
        DocumentFileTest.DocumentScreen(user(usern), doc_cli.get_document(document, usern, versionNo))

    def openDoc1(self):
        documentname = self.userDocs[0][0]
        usern = self.userDocs[0][1]
        versionNo = self.userDocs[0][2]
        DocumentFileTest.DocumentScreen(user(usern), doc_cli.get_document(documentname, self.user, versionNo))

    def openDoc2(self):
        documentname = self.userDocs[1][0]
        usern = self.userDocs[1][1]
        versionNo = self.userDocs[1][2]
        DocumentFileTest.DocumentScreen(user(usern), doc_cli.get_document(documentname, self.user, versionNo))

    def openDoc3(self):
        documentname = self.userDocs[2][0]
        usern = self.userDocs[2][1]
        versionNo = self.userDocs[2][2]
        DocumentFileTest.DocumentScreen(user(usern), doc_cli.get_document(documentname, self.user, versionNo))

# The next 3 functions can only be accessed by a SU
#Function that connects to the ProcessMember class that holds the Process Member GUI and functions
    def processApl(self):
        ProcessMember.MemberApplication.main(self)

 # Function that connects to the ProcessTabooWord class that holds the Process Taboo Words GUI and functions
    def processTaboo(self):
        ProcessTabooWord.ProcessTabooWord.main(self)

   # Function that connects to the ProcessComplaints class that holds the Process Complaints GUI and functions
    def processComplaint(self):
        ProcessComplaints.ProcessComplaints.main(self)

    def main(self, username):
        root = Toplevel()
        UserPg(root, username)
        root.mainloop()
