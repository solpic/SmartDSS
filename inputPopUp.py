"""
DONT USE, use the following instead
import tkinter.simpledialog as tkSimpleDialog 
 uInput = tkSimpleDialog.askstring("Add Taboo Word","Word?")

"""
from tkinter import *
class textPopUp:
    'For Text Input Pop Ups'

    # Message is the message you want to prompt the user with
    def __init__(self,message):
        self.root = Toplevel()
        self.root.title("Submit Taboo Word")
        self.prompt = Label(self.root,text=message)
        self.prompt.pack()
        self.userInput = Entry(self.root)
        self.userInput.pack()
        self.enterButton = Button(self.root,text="Submit", command=self.inputData)
        self.enterButton.pack()
        self.inputWord = ""
        self.exists = True

    # Should Update DB with user input
    def inputData(self):
        self.inputWord = self.userInput.get()
        print("INPUT CLASS: ",self.inputWord)
        # TODO: add Taboo Word to DB
        # print("inputData Method Body")
        self.exists=False
        self.root.destroy()
    
    def getInputWord(self):
        print("In getInput")
        return self.inputWord
    