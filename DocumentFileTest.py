from tkinter import *
import tkinter.simpledialog as tkSimpleDialog 
import TabooWords
import DeltaObjects

'''Document View'''
#TODO: Real User Class Integration
class DocumentScreen:
    def __init__(self,user,document):
        self.currentUser = user;
        self.userRank = user.getRank()
        self.currentDoc= document
        # self.docMembers = document.getMembers()
        self.allUsers = ["Arik","Idrisy","Microsoft","IBM"] #TODO: Server Call
        from RPCClient import get_proxy
        get_proxy().delete_updates(1, 0, 100)
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
        allMembersMenu = Menu(membOptMenu)
        # allMembersMenu.add_command(label="xyz")
        for member in self.currentDoc.getMembers():
            allMembersMenu.add_command(label=member.getUserName())
        self.updateMembersMenu.add_cascade(label="Remove User", menu=allMembersMenu)
        allUserMenu = Menu(self.updateMembersMenu)
        for user in self.allUsers:
            allUserMenu.add_command(label=user)
        self.updateMembersMenu.add_cascade(label="All Registered Users",menu=allUserMenu)
        membOptMenu.add_cascade(label="View All Members", menu=allMembersMenu)
        self.mainMenu.add_cascade(label="Membership Option",menu=membOptMenu)

        # Taboo Word Menu
        tabooMenu = Menu(self.mainMenu)
        tabooWords = TabooWords.TabooWords.getAllTaboo() 
        for tWord in tabooWords:
            tabooMenu.add_command(label=tWord)
        tabooMenu.add_separator()
        tabooMenu.add_command(label="Add Taboo Word", command=self.addTabooWord)# command ~~ addTabooWord
        self.mainMenu.add_cascade(label="TabooWords", menu=tabooMenu)

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
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2,)
        scrollb = Scrollbar(textFrame, command=self.txt.yview)
        scrollb.grid(row=0, column=2, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set    
        self.root.config(menu=self.mainMenu)    
        self.root.mainloop()

    def addUser(self):
        print("Add User Function")
        self.updateMembersMenu
    def removeUser(self):
        print("Remove User Function")
    #PostCond: The inputed Word is added to the DB of Taboo Words
    def addTabooWord(self):
        uInput = tkSimpleDialog.askstring("Add Taboo Word","Word?")
        #currentDoc.addTabooWord(uInput)
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
        new = self.txt.get("1.0",'end-1c')
        self.currentDoc.generateDeltas(old,new)
        self.currentDoc.words= new
        for delta in self.currentDoc.deltaLog:
            if(isinstance(delta,DeltaObjects.Delete)):
                doc_cli.push_delete(self.currentDoc.doc_id,delta)
            if(isinstance(delta,DeltaObjects.Insert)):
                doc_cli.push_insert(self.currentDoc.doc_id,delta)
        print("Old {} | New {} |Doc.words {}".format(old,new,self.currentDoc.words))

    def pullChanges(self):
        from DocumentDB import doc_cli
        deltaList= doc_cli.get_updates(self.currentDoc.doc_id,0)
        for i in deltaList:
            i.show()
        self.currentDoc.reconstruct(5,deltaList)

    # TODO: UPDATING SCREEN WITH NEW INFO
    # For Menu we can destroy and re build
