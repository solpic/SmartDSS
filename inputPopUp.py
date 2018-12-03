"""
DESCRIPTION:
    A class to be used when a pop us needed requesting user input in the form of a string

EXAMPLES:
    Taboo Word Suggestion: We prompt the user, and the user inputs a string

"""
from tkinter import *
class textPopUp:
    'For Text Input Pop Ups'

    # Message is the message you want to prompt the user with
    def __init__(self,message):
        root = Toplevel()
        root.title="test"
        self.prompt = Label(root,text=message)
        self.prompt.pack()
        self.userInput = Entry(root)
        self.userInput.pack()
        self.enterButton = Button(root,text="Submit", command=self.inputData)
        self.enterButton.pack()

    # Should Update DB with user input
    def inputData(self):
        tabooWord = self.userInput.get()
        # TODO Server Call
    