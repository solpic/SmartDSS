from tkinter import*
from tkinter import messagebox

import Users1
import UserPg

class createfileinput():
    def __init__(self):
        root = self.root = Toplevel()
        self.documentName = StringVar()
        self.documentPrivacyLevel = StringVar()
        self.sts = StringVar()
        self.privacyLevel = 'public'
        self.privacyLevels = ['public', 'restricted', 'shared', 'private']
        self.createWidgets()

    def createWidgets(self):
        frame1 = Frame(self.root)

        Label(frame1, text="Document Name").grid(sticky=W, pady=2)
        Entry(frame1, textvariable=self.documentName).grid(row=0, column=1)
        Label(frame1, text="PrivacyLevel").grid(sticky=W)
        count=1
        self.documentPrivacyLevel.set("public")
        for level in self.privacyLevels:
            self.b = Radiobutton(frame1, text= level,variable= self.documentPrivacyLevel, value= level)
            self.b.grid(row=count, column=1, sticky=W)
            count = count +1

        Button(frame1, text="Create!", command = self.createdoc).grid(row=5, column = 0, pady=2)
        Button(frame1, text="Cancel", command = self.quit).grid(row=5, column=1, pady=2)

        frame1.pack()
        Label(self.root, textvariable=self.sts).pack()

    def createdoc(self):
        name = self.documentName.get()
        if name == "":
            self.sts.set("Please enter a title")
        else:
            privacyLevel = self.documentPrivacyLevel.get()
            self.root.destroy()
            return name, privacyLevel

    def quit(self):
        self.root.destroy()


    def main(self):
       creategui = createfileinput()
       creategui.root.mainloop()