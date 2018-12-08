from tkinter import *
import tkinter.simpledialog as tkSimpleDialog 
import inputPopUp
'''Document View'''
class DocumentScreen:
    def __init__(self,user,document):
        self.currentUser = user;
        self.userRank = user.getRank()
        self.currentDoc= document
        # self.docMembers = document.getMembers()
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
        mainMenu = Menu(self.root)
        
        # All Following Menus are submenus of the mainMenu object
        # Back Menu
        backMenu = Menu(mainMenu,tearoff=0)
        backMenu.add_command(label="GO BACK")#command ~~ openHomePg()
        mainMenu.add_cascade(label="<--",menu=backMenu)

        # Complain Menu
        complainMenu = Menu(mainMenu)
        complainMenu.add_command(label="Submit Document Complaint",command=self.addDocComplaint)
        complainMenu.add_command(label="Submit User Complaint",command=self.addUserComplaint)
        mainMenu.add_cascade(label="Complaints",menu=complainMenu)
        # complainMenu.entryconfigure("Submit Document Complaint",state="disabled")

        # Document Options Menu
        optMenu = Menu(mainMenu)
        optMenu.add_command(label="View Past Versions")#command = ???? Something to view previous docs
        optMenu.add_command(label="Lock Document")#command = lockDocument 
        optMenu.add_command(label="Unlock Document")#command = unLockDocument
        mainMenu.add_cascade(label="Document Options", menu=optMenu)
        
        # Membership Options Menu

        membOptMenu = Menu(mainMenu)
        membOptMenu.add_command(label="Update Member(s)")
        #TODO: View all Members [system.getAllMembers] or direct Server call?
        allMembersMenu = Menu(membOptMenu)
        # allMembersMenu.add_command(label="xyz")
        for member in self.currentDoc.getMembers():
            allMembersMenu.add_command(label=member.getUserName())

        membOptMenu.add_cascade(label="View All Members", menu=allMembersMenu)
        mainMenu.add_cascade(label="Membership Option",menu=membOptMenu)
        # Taboo Word Menu
        tabooMenu = Menu(mainMenu)
        tabooWords = {"Word1", "Word2", "Word3"} # PLACEHOLDER, should be obtained from DB TODO: Server Call
        for tWord in tabooWords:
            tabooMenu.add_command(label=tWord)
        tabooMenu.add_command(label="Add Taboo Word", command=self.addTabooWord)# command ~~ addTabooWord
        mainMenu.add_cascade(label="TabooWords", menu=tabooMenu)

        # Document Complaints [ Against Document ] Menu
        # TODO: Concert this to deal with Complaints from Document Object
        docComplaintMenu = Menu(mainMenu)
        complaints = ["0000","0001","0002","0004","0005"]
        for complaint in complaints:
            docComplaintMenu.add_command(label=complaint)
        mainMenu.add_cascade(label="Document Complaints",menu=docComplaintMenu)


        # These come from the user who opened this documentvIEW
        # These can also just be extra fields in the menu
        # --Dynamic Buttons----------------------------------------------------------------------
        # Acomplished by Disabling buttons based on user Rank
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
        # TODO: Change to text

        displayText = self.currentDoc.getWords() # PLACE HOLDER VALUES 
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
        self.root.config(menu=mainMenu)    
        self.root.mainloop()

    #PostCond: The inputed Word is added to the DB of Taboo Words
    def addTabooWord(self):
        uInput = tkSimpleDialog.askstring("Add Taboo Word","Word?")
        #currentDoc.addTabooWord(uInput)
    
    def addDocComplaint(self):
        complaint=tkSimpleDialog.askstring("Enter Complaint against Document")
        self.currentDoc.addComplaint(complaint)
    def addUserComplaint(self):
        complaint=tkSimpleDialog.askstring("Enter Complain Against User")
        self.currentUser.addComplaint()
