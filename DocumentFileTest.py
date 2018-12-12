from tkinter import *
import tkinter.simpledialog as tkSimpleDialog 
import TabooWords
import DeltaObjects

'''Document View'''
#TODO: Real User Class Integration
class DocumentScreen:
    def __init__(self,user,document):
        self.lastChange = -1
        self.currentUser = user;
        self.userRank = user.getRank()
        self.currentDoc= document
        # self.docMembers = document.getMembers()
        from DocumentDB import doc_cli
        #self.allUsers = doc_cli.get_all_sys_Users() #TODO: Server Call
        self.allUsers = ["ARI","ME","JAS"]

        self.makeScreen()


    def makeScreen(self):

        DocHeight=1024
        DocWidth = 720
        
        TextPlaceHolder="PLACEHOLDER"

        self.root= Tk()
        #root.title(self.currentDoc.getTitle() +" || "+ self.currentUser.getUserName())
        self.root.title("Document Screen")
        self.root.geometry(str(DocHeight)+"x"+str(DocHeight))
        
        # --Menu Set Up -------------------------------------------------------------------------
        self.mainMenu = Menu(self.root)
        
        # All Following Menus are submenus of the self.mainMenu object
        # Back Menu
        backMenu = Menu(self.mainMenu,tearoff=0)
        backMenu.add_command(label="GO BACK")#command ~~ openHomePg()
        self.mainMenu.add_cascade(label="<--",menu=backMenu)

        # Complain Menu
        complainMenu = Menu(self.mainMenu)
        complainMenu.add_command(label="Submit Document Complaint",command=self.addDocComplaint)
        complainMenu.add_command(label="Submit User Complaint",command=self.addUserComplaint)
        self.mainMenu.add_cascade(label="Complaints",menu=complainMenu)
        # complainMenu.entryconfigure("Submit Document Complaint",state="disabled")

        # Document Options Menu
        optMenu = Menu(self.mainMenu)
        optMenu.add_command(label="View Past Versions")#command = ???? Something to view previous docs
        optMenu.add_command(label="Lock Document",command=self.lockDocument)#command = lockDocument 
        optMenu.add_command(label="Unlock Document",command=self.unlockDocument)#command = unLockDocument
        self.mainMenu.add_cascade(label="Document Options", menu=optMenu)
        
        # Membership Options Menu

        membOptMenu = Menu(self.mainMenu)
        membOptMenu.add_command(label="Update Member(s)")
        #TODO: add members/ remove members
        self.updateMembersMenu = Menu(membOptMenu)
        # self.updateMembersMenu.add_command(label="Add User",command=self.addUser)
        # self.updateMembersMenu.add_command(label="Remove User",command=self.removeUser)
        
        membOptMenu.add_cascade(label="Update Members", menu=self.updateMembersMenu)
        self.allMembersMenu = Menu(membOptMenu)
        #TODO: UNcommetn 2 lower lines
        #for member in self.currentDoc.getMembers():
            #self.allMembersMenu.add_command(label=member.getUserName(),command=self.removeUser(member.getUserName()))
        self.allUserMenu = Menu(self.updateMembersMenu)
        # allMembersMenu.add_command(label="xyz")
        for member in self.currentDoc.getMembers():
            #self.allMembersMenu.add_command(label=member.getUserName())
            self.allMembersMenu.add_command(label=memeber.getUserName(),command=lambda i= user: self.removeUser(i))
        # self.updateMembersMenu.add_cascade(label="Remove User", menu=self.allMembersMenu)
        self.allUserMenu = Menu(self.updateMembersMenu)
        for user in self.allUsers:
            self.allUserMenu.add_command(label=user,command=lambda j = user: self.addUser(j))
        self.updateMembersMenu.add_cascade(label="Remove Member", menu=self.allMembersMenu)
        self.updateMembersMenu.add_cascade(label="All Registered System Users",menu=self.allUserMenu)
        membOptMenu.add_cascade(label="View All Members", menu=self.allMembersMenu)
        self.mainMenu.add_cascade(label="Membership Option",menu=membOptMenu)

        # Taboo Word Menu
        self.tabooMenu = Menu(self.mainMenu)
        self.tabooWords = TabooWords.TabooWord.getAllTaboo() 
        for tWord in self.tabooWords:
            self.tabooMenu.add_command(label=tWord)
        self.tabooMenu.add_separator()
        self.tabooMenu.add_command(label="Add Taboo Word", command=self.addTabooWord)# command ~~ addTabooWord
        self.tabooMenu.add_separator()
        self.tabooMenu.add_command(label="Newly Added Taboos")
        
        self.mainMenu.add_cascade(label="TabooWords", menu=self.tabooMenu)

        # Document Complaints [ Against Document ] Menu
        docComplaintMenu = Menu(self.mainMenu)
        complaints = self.currentDoc.getComplaints()
        for complaint in complaints:
            docComplaintMenu.add_command(label=complaint)
        self.mainMenu.add_cascade(label="View Document Complaints",menu=docComplaintMenu)

        # Submit Menu
        changeMenu = Menu(self.mainMenu)
        changeMenu.add_command(label="Submit Changes",command= self.submitChanges)
        changeMenu.add_command(label="Pull Staged Changes",command = self.pullChanges)
        self.mainMenu.add_cascade(label="PUSH/PULL",menu=changeMenu)


        # --Dynamic Buttons----------------------------------------------------------------------
        # These come from the user who opened this documentvIEW
        # These can also just be extra fields in the menu
        # Acomplished by Disabling buttons based on user Rank
        # TODO: Check if anymore must be added
        if(self.userRank=="SU"):
            print()
        elif(self.userRank=="OU"):
            #Lock Document
            print()
        elif(self.userRank=="GU"):
            optMenu.entryconfigure("Lock Document",state="disabled")
            optMenu.entryconfigure("Unlock Document",state="disabled")
            print()
        else:
            print("ERROR: USER RANK UNDIFINED")

        
        # --Text Fields--------------------------------------------------------------------------

        displayText = self.currentDoc.getWords() 
        # create a Text (widget)
        textFrame = Frame(self.root,width = DocWidth,height=DocHeight)
        textFrame.pack(fill="both",expand=True)
        textFrame.grid_propagate(False)
        textFrame.grid_rowconfigure(0,weight=1)
        textFrame.grid_columnconfigure(0,weight=1)
        self.txt = Text(textFrame, borderwidth=3, relief="sunken",width=200,height=DocHeight)
        self.txt.insert(END,self.currentDoc.words)
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2,)
        scrollb = Scrollbar(textFrame, command=self.txt.yview)
        scrollb.grid(row=0, column=2, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set    
        self.root.config(menu=self.mainMenu)   
        # Get changes from server
        self.pullChanges() 
        self.root.mainloop()
#--- END MAKE SCREEN ------------------------------

    def refreshText(self):
        self.txt.delete(1.0,END)
        self.txt.insert(END,self.currentDoc.words)
    def addUser(self,user):
        print("Add User Function")
        self.currentDoc.memberList.append(user)
    def removeUser(self,uname):
        from DocumentDB import doc_cli

        print("Remove User Function , uname: {}".format(uname))
        x=0
        
        mem = self.currentDoc.getMembers()
        
        for i in range(0,len(mem)):
            if (mem[i].getUserName()==uname):
                x=i
                delmem = mem[i]
                break


        self.allMembersMenu.delete(x)
        self.currentDoc.removeMember(delmem)
    #PostCond: The inputed Word is added to the DB of Taboo Words
    def addTabooWord(self):
        from DocumentDB import doc_cli

        uInput = tkSimpleDialog.askstring("Add Taboo Word","Word?")
        #TabooWords.TabooWord.addTabooWord(uInput)
        if doc_cli.add_taboo_word(uInput):
            self.tabooMenu.add_command(label=uInput)
        #self.tabooMenu.pack()

    #TODO: Changing other GUI elements as well when its locked
    #  - submit button
    #  - adding member button
    def lockDocument(self):
        self.txt.config(state="disabled")
        self.currentDoc.lockDocument()
    def unlockDocument(self):
        self.txt.config(state="normal")
        self.currentDoc.unlockDocument()
    def addDocComplaint(self):
        complaint=tkSimpleDialog.askstring("Enter Complaint against Document","Complaint:")
        self.currentDoc.addComplaint(complaint,self.currentUser)
    def addUserComplaint(self):
        complaint=tkSimpleDialog.askstring("Enter Complain Against User")
        self.currentUser.addComplaint()

    def submitChanges(self):
        from DocumentDB import doc_cli
        old = self.currentDoc.getWords()
        print("OLD: "+old)
        new = self.txt.get("1.0",'end-1c')
        deltas = self.currentDoc.generateDeltas(old,new)
        self.currentDoc.words= new
        for delta in deltas:
            delta.show()
            if(isinstance(delta,DeltaObjects.Delete)):
                doc_cli.push_delete(self.currentDoc.doc_id,delta)
            if(isinstance(delta,DeltaObjects.Insert)):
                doc_cli.push_insert(self.currentDoc.doc_id,delta)
        doc_cli.show_all_updates()
        # deltaListServ = doc_cli.get_updates(self.currentDoc.doc_id,0)
        # print("DeltaList Server")
        # for i in deltaListServ:
            # i.show()
        # print("DeltaList Client")
        # deltaListClient = self.currentDoc.deltaLog
        # for j in deltaListClient:
            # j.show()
        # print("Old {} | New {} |Doc.words {}".format(old,new,self.currentDoc.words))

    def refreshText(self):
        self.txt.delete(1.0, END)
        self.txt.insert(END, self.currentDoc.words)

    def pullChanges(self):
        from DocumentDB import doc_cli
        doc_cli.show_all_updates()
        deltaList= doc_cli.get_updates(self.currentDoc.doc_id,self.lastChange)
        for i in deltaList:
            i.show()
        self.currentDoc.reconstruct(5,deltaList)
        self.refreshText()
        if len(deltaList)>0:
            self.lastChange = deltaList[len(deltaList)-1].u_id
        else:
            self.lastChange = -1

    # TODO: UPDATING SCREEN WITH NEW INFO
    # For Menu we can destroy and re build
