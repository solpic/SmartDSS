from tkinter import *
import inputPopUp
# TODO: Document Class
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

        root= Tk()
        root.title(self.currentDoc.getTitle() +" || "+ self.currentUser.getUserName())
        root.geometry(str(DocHeight)+"x"+str(DocHeight))
        
        # --Menu Set Up -------------------------------------------------------------------------
        mainMenu = Menu(root)
        
        # All Following Menus are submenus of the mainMenu object
        # Back Menu
        backMenu = Menu(mainMenu,tearoff=0)
        backMenu.add_command(label="GO BACK")#command ~~ openHomePg()
        mainMenu.add_cascade(label="<--",menu=backMenu)

        # Complain Menu
        complainMenu = Menu(mainMenu)
        complainMenu.add_command(label="Submit Document Complaint")
        complainMenu.add_command(label="Submit User Complaint")
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
        membOptMenu.add_command(label="Update Member(s)")#TODO: Add command=inputpopup
        allMembersMenu = Menu(membOptMenu)
        # allMembersMenu.add_command(label="xyz")
        for member in self.currentDoc.getMembers():
            allMembersMenu.add_command(label=member.getUserName())
            # TODO: TEST with Document Object

        membOptMenu.add_cascade(label="View All Members", menu=allMembersMenu)
        mainMenu.add_cascade(label="Membership Option",menu=membOptMenu)
        # Taboo Word Menu
        tabooMenu = Menu(mainMenu)
    
        tabooWords = {"Word1", "Word2", "Word3"} # PLACEHOLDER, should be obtained from DB TODO: Server Call
        for tWord in tabooWords:
            tabooMenu.add_command(label=tWord)
        tabooMenu.add_command(label="Add Taboo Word", command=self.addTabooWord)# command ~~ addTabooWord
        mainMenu.add_cascade(label="TabooWords", menu=tabooMenu)

        # TODO: How to get User Rank and make Dynamic Buttons
        # These come from the user who opened this document
        # These can also just be extra fields in the menu
        # --Dynamic Buttons----------------------------------------------------------------------
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
        textArray = [] # Should be an array of TK ENTRY WIDGETS

        numberOfSentances = 10 # PLACE HOLDER VALUES TODO: Populate from Document Object

        TextHeight=40
        yOffSet=0
        for i in range(0, numberOfSentances):
            textArray.append(Entry(root,width=DocWidth))
            textArray[i].place(x=0,y=yOffSet+20*i)
            # textArray[i].config(state="disabled")
            textArray[i].insert(END,TextPlaceHolder)
            # the argument of this should be populated best on the line number, and the data should
            # come from the Db
            
        root.config(menu=mainMenu)    
        root.mainloop()

    #PostCond: The inputed Word is added to the DB of Taboo Words
    def addTabooWord(self):
        inputPopUp.textPopUp("Enter Taboo Word Suggestion Below")
