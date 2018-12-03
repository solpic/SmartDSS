from tkinter import *
import inputPopUp

def main():

    DocHeight=1024
    DocWidth = 720
    
    TextPlaceHolder="PLACEHOLDER"

    root= Tk()
    root.title("document.getTitle() || user.getUserName()")
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

    # Taboo Word Menu
    tabooMenu = Menu(mainMenu)
 
    tabooWords = {"Word1", "Word2", "Word3"} # PLACEHOLDER, should be obtained from DB TODO: Server Call
    for tWord in tabooWords:
        tabooMenu.add_command(label=tWord)
    tabooMenu.add_command(label="Add Taboo Word", command=addTabooWord)# command ~~ addTabooWord
    mainMenu.add_cascade(label="TabooWords", menu=tabooMenu)

    # TODO: How to get User Rank and make Dynamic Buttons
    # --Text Fields--------------------------------------------------------------------------
    textArray = [] # Should be an array of TK TEXT WIDGETS

    numberOfSentances = 10 # PLACE HOLDER VALUES TODO : Server Call
    # numberOfSentances = Some Database Pull

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
def addTabooWord():
    inputPopUp.textPopUp("Enter Taboo Word Suggestion Below")


main()