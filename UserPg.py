from tkinter import*
from DocumentDB import doc_cli
import Users1
import DocumentFileTest
from DocumentScreenTester import user

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
        self.UserDetailService = Users1.Users()
        self.rank = self.UserDetailService.getRank(username)
        self.memberName = StringVar()
        self.memberInt = StringVar()
        self.docName = StringVar()
        self.memberSearch = []
        self.interestsSearch = []
        self.documentSearch = []
        self.activedoc = ""
        self.invar = StringVar(value=self.interestsSearch)
        self.var = StringVar(value=self.memberSearch)
        self.docvar = StringVar(value= self.documentSearch)
        self.Interest1 = self.UserDetailService.getInterest1(username)
        self.Interest2 = self.UserDetailService.getInterest2(username)
        self.Interest3 = self.UserDetailService.getInterest3(username)
        self.createWidget()

    def createWidget(self):
        self.frame1.configure(background = "white")
        frame2 = Frame(self.frame1)
        frame2.config(width = 100)
        frame2.pack(fill=X, expand=True)
        frame3 = Frame(self.frame1)
        frame3.pack(fill=X, expand=True)
        frame4 = Frame(self.frame1)
        frame4.pack(fill=X, expand=True)
        frame5 = Frame(frame4)
        frame5.pack(side = LEFT, fill=X)
        frame6 = Frame(frame4)
        frame6.pack(side = LEFT, fill=X)
        frame7 = Frame(frame4)
        frame7.pack(side = LEFT, fill=X)
        frame8 = Frame(frame4)
        frame8.pack( side = LEFT, fill=X)

        UsernameText = self.user
        Label(frame2,text = UsernameText + " " + self.rank, font=('Ariel', 30), fg= "medium blue",
                        background ="white" ).grid(row=0, column=0, padx =10, pady=20)
      #  Label(frame2, text="", width =800).grid(row=0,column=1)

        img = self.getImage()
        profile = Label(frame5, image= img)
        profile.image = img
        profile.grid(row=0, column=0, pady=10)

        Label(frame5, text= "Interests", font=('Ariel', 30), fg="medium blue").grid(
            row=1, column=0, pady=10)
        Label(frame5, text= self.Interest1, font=('Ariel', 26), fg="medium blue")\
            .grid(row=2, column=0, padx=20, sticky=W)
        Label(frame5, text= self.Interest2, font=('Ariel', 26), fg="medium blue")\
            .grid(row=3, column=0, padx=20, sticky=W)
        Label(frame5, text= self.Interest3, font=('Ariel', 26), fg="medium blue").\
            grid(row=4, column=0, padx=20, sticky=W)

        Button(frame3,text = "create document",font=('Ariel', 30), fg= "medium blue", background ="white", command = self.createnewdoc ).grid(row=0, column=0, padx=10, pady=10)
        Button(frame3, text= "recent doc 1", font=('Ariel', 30), fg="medium blue", background="white", width=15).grid(row=0, column=1, padx=20)
        Button(frame3, text= "doc 2", font=('Ariel', 30), fg="medium blue", background="white", width =15).grid(row=0, column=2, padx=10)
        Button(frame3, text= " doc 3", font=('Ariel', 30), fg="medium blue", background="white", width =15).grid(row=0, column=3, padx=10)

        Label(frame6,text = "Search Members by Username",font=('Ariel', 16), fg= "medium blue", width=24 ).grid(row = 0, column=0)
        Entry(frame6, textvariable = self.memberName, width=50).grid(row=1,column=0, sticky=E, padx=10)
        simg = PhotoImage(file="images.gif")
        searchpic1 = Button(frame6, image= simg, command = self.memSearch)
        searchpic1.image = simg
        searchpic1.grid(row=1, column=1)
        searchResults = Listbox(frame6, listvariable=self.var, width=50).grid(row=2, column=0, sticky=E, padx=10)
        for entry in self.memberSearch:
            print("entry", entry)
            searchResults.insert(entry)

        Label(frame6, text="Search Members by Interests", font=('Ariel', 18), fg="medium blue", width=22).grid(row=3, column=0)
        Entry(frame6, textvariable=self.memberInt, width=50).grid(row=4, column=0, sticky=E, padx=10)
        searchpic2 = Button(frame6, image=simg, command=self.intSearch)
        searchpic2.image = simg
        searchpic2.grid(row=4, column=1)
        searchResultInt = Listbox(frame6, listvariable= self.invar, width=50).grid(row=5, column=0, sticky=E, padx=10)
        for entry in self.interestsSearch:
            print("entry", entry)
            searchResultInt.insert(entry)

        Label(frame7, text="Search Documents", font=('Ariel', 26), fg="medium blue", width=15).grid(
            sticky=E)
        Entry(frame7, textvariable = self.docName, width=50).grid(row=1, column=0, sticky=E, padx=10)
        simg = PhotoImage(file="images.gif")
        searchpicD = Button(frame7, image=simg, command = self.docSearch)
        searchpicD.image = simg
        searchpicD.grid(row=1, column=1)
        self.searchResultDocs = Listbox(frame7, listvariable = self.docvar, width=50)
        self.searchResultDocs.grid(row=2, column=0, sticky=E, padx=10)
        for entry in self.documentSearch:
            print("entry", entry)

        Button(frame7,text="Open Document", font=('Ariel', 24), fg="medium blue", width=16, background= "white", command = self.opendoc).grid(row=3, column=0, pady=5)

        Button(frame8, text= "Process Complaints", font=('Ariel', 24), fg="medium blue", background="white"
                            ).grid(row=1, column=1, padx=30, pady=40, sticky=E)
        Button(frame8, text="Process Taboo Words", font=('Ariel', 24), fg="medium blue",
                             background="white").grid(row=3, column=1,padx=30, pady=40, sticky = E)
        Button(frame8, text="Process Applications", font=('Ariel', 24), fg="medium blue",
                             background="white").grid(row=5, column=1, padx=30, pady =40, sticky=E)
        self.frame1.pack()

    def getImage(self):
        img = PhotoImage(file="testgirl.gif")
        return img

    def memSearch(self):
        user = self.memberName.get()
        self.memberSearch = self.UserDetailService.searchUser(user)
        for entry in self.memberSearch:
            print("bottom entry", entry)
        self.var.set(self.memberSearch)

    def intSearch(self):
        user = self.memberInt.get()
        self.interestsSearch = self.UserDetailService.searchUserInt(user)
        for entry in self.interestsSearch:
            print("bottom entry", entry)
        self.invar.set(self.interestsSearch)

    def docSearch(self):
        docs = doc_cli.get_all_documents()
        searchItem = self.docName.get()

        names = []
        for doc in docs:
            if searchItem in doc.docName:
                entry = (doc.docName, doc.owner, doc.versionNumber)
                names.append(entry)
        self.documentSearch = names
        for entry in self.documentSearch:
            print("search", entry)
        self.docvar.set(names)

    def createnewdoc(self):
        print("new document")
        doc_name = "New Document Test"
        versionNo = 0
        init_contents =""
        doc_cli.create_document( doc_name, self.user, init_contents)
        doc_cli.get_document(doc_name, self.user, versionNo)
        DocumentFileTest.DocumentScreen(user(user), doc_cli.get_document(doc_name, self.user, versionNo))

    def opendoc(self):
        item = self.searchResultDocs.curselection()
        idx = item[0]
        docdetail = self.documentSearch[idx]
        document = docdetail[0]
        usern = docdetail[1]
        versionNo = docdetail[2]
        DocumentFileTest.DocumentScreen(user(usern), doc_cli.get_document(document, usern, versionNo))


    def main(self, username):
        root = Toplevel()
        UserPg(root, username)
        root.mainloop()