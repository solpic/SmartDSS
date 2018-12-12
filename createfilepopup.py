from tkinter import*


class createinput():
    def __init__(self):
        self.root = Toplevel()
        self.documentName = StringVar()
        self.documentPrivacyLevel = StringVar()
        self.privacyLevel = 'public'
        self.privacyLevels = ['public', 'restricted', 'shared', 'private']
        self.createWidgets()

    def createWidgets(self):
        frame1 = Frame(self.root)

        Label(frame1, text="Document Name").grid(sticky=W, pady=2)
        Entry(frame1, textvariable=self.documentName).grid(row=0, column=1)
        Label(frame1, text="PrivacyLevel").grid(sticky=W)


        Button(frame1, text="Create!", command = self.createdoc).grid(row=5, column = 0, pady=2)
        Button(frame1, text="Cancel", command = self.quit).grid(row=5, column=1, pady=2)

        frame1.pack()


    def createdoc(self):
        self.name = self.documentName.get()
        print(self.name)
        print(self.name)
        return self.name

    def quit(self):
        var ="we won"
        self.root.destroy()
        return var


    def main(self):
       creategui = createinput()
       creategui.root.mainloop()