from tkinter import*
import time

def main():
    root=Tk()
    root.title("PHASE II DEMO")
    root.geometry("1024x720")
    titleLabel = Label(root, text="AP WORLD HISTORY NOTES",borderwidth=4, relief="groove", bg="lightblue")
    titleLabel.config(font=("Courier", 18))
    titleLabel.place(x=50,y=10)
   # titleLabel.pack()

    backButton = Button(root, text="BACK" , borderwidth=4, relief="groove", fg="red")
    backButton.configure(font=("Courier", 10))
    backButton.place(x=0,y=15)

    complainLabel = Label(root, text="COMPLAIN",borderwidth=4,relief="groove", bg="red")
    complainLabel.configure(font=("Courier",15))
    complainLabel.place(x=375,y=14)
    '''
    tabooLabel = Label(root, text="TABOO WORDS", borderwidth=4,relief="groove")
    tabooLabel.configure(font=("Courier",15))
    tabooLabel.place(x=485,y=14)
    '''

    dropFrame = Frame(root)
    dropFrame.grid(column=0, row=0, sticky=(N,W,E,S))
    dropFrame.columnconfigure(0,weight=1)
    dropFrame.rowconfigure(0, weight =1)
    dropFrame.pack(pady=100,padx=100)
    tkVar = StringVar(root)
    badWords = {"BadWordOne", "BadWordTwo", "BadWordThree"}
    tkVar.set("TABOO WORDS")
    tabooPopUp = OptionMenu(dropFrame,tkVar,*badWords)
    #Label(dropFrame,text="TABOO WORDS").grid(row=1,column=1)
    tabooPopUp.grid(row =2, column = 1)
    dropFrame.place(x=480, y=14)


    addTabooButton = Button(root,text="+", borderwidth=4,relief="groove",width=4, command=suggestTaboo)
    addTabooButton.place(x=610,y=14)

    historyLabel = Label (root, text="DOCUMENT HISTORY",borderwidth = 4, relief = "groove", bg="green")
    historyLabel.config(font=("Courier",14))
    historyLabel.place(x=10,y=50)

    ownerNameLabel = Label(root, text="OWNER NAME", borderwidth = 4,relief="groove")
    # Realistically should be  text=getOwnerDisplayName()
    ownerNameLabel.config(font=("Courier",14))
    ownerNameLabel.place(x=200,y=50)

    # Hold all of the dynamic buttons
    # Planned to be used to sped up instantiation of Dynamic Buttons
    # Since a lot of them have similar properties, and the USER class
    # should know how many buttons there will be
    # For the demo I'll simply populate it
    dynamicButtonArray=[];

    dynamicButtonOne = Button(root,text="Dynamic Button One", borderwidth = 4, relief="groove",fg="tan")
    # text attribute should be obtained from the user
    # something like text=user.getDynamicButtonName(1),where the parameter is the number of the dyanmic button desired

    dynamicButtonOne.config(font=("Courier",14))
    dynamicButtonOne.place(x=325,y=50)
    dynamicButtonArray.append(dynamicButtonOne)
    
    dynamicButtonTwo = Button(root,text="Dynamic Button Two", borderwidth = 4, relief="groove", fg="tan")
    dynamicButtonTwo.config(font=("Courier",14))
    dynamicButtonTwo.place(x=550,y=50)
    dynamicButtonArray.append(dynamicButtonTwo)

    dynamicButtonThree = Button(root,text="Dynamic Button Three", borderwidth = 4, relief="groove", fg="tan")
    dynamicButtonThree.config(font=("Courier",14))
    dynamicButtonThree.place(x=775,y=50)
    dynamicButtonArray.append(dynamicButtonThree)

    documentEntry = Text(root,width=640,height=480)
    documentEntry.place(x=0,y=100)


    root.mainloop()

def suggestTaboo():
    global pop
    pop = Toplevel()
    pop.title("Taboo Word Pop Up")
    
    messageLabel = Label(pop,text="Please Insert Suggested Taboo Word Below")
    messageLabel.pack()

    wordEntry = Entry(pop)
    wordEntry.pack()

    submitButton = Button(pop,text="Submit",borderwidth=4,relief="groove",command=confirmTaboo)
    submitButton.pack()

    #confirmPop.destroy()

def confirmTaboo():
    global pop
    pop.destroy()
    global confirmPop 
    confirmPop = Toplevel()
    confirmPop.title("CONFIRMED")
    
    #msg="Suggestion Recieved, Awaiting Super User Approval"
    messageButton = Button(confirmPop,text="Suggestion Recieved, Awaiting Super User Approval",borderwidth=4,relief="groove")
    messageButton.pack()

    closeWindow = Label(confirmPop,text="Close this Window")
    closeWindow.pack()

main();