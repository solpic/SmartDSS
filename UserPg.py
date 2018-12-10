from tkinter import*
import Users1

class UserPg():
    def __init__(self, parent, username):
        self.user = username
        self.parent = parent
        self.parent.title("")
        self._geom = '800x800+0+0'
        parent.geometry("{0}x{1}+0+0".format(
            parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.parent.configure(background="white")
        obj1 = Users1.Users()
        self.rank = obj1.getRank(username)
        self.Interest1 = obj1.getInterest1(username)
        self.Interest2 = obj1.getInterest2(username)
        self.Interest3 = obj1.getInterest3(username)
        self.createWidget()

    def createWidget(self):
        frame1 = Frame(self.parent)
        frame1.configure(background = "white")
        frame2 = Frame(frame1)
        frame2.config(width = 100)
        frame2.pack(fill=X, expand=True)
        frame3 = Frame(frame1)
        frame3.pack(fill=X, expand=True)
        frame4 = Frame(frame1)
        frame4.pack(fill=X, expand=True)
        frame5 = Frame(frame4)
        frame5.pack(side = LEFT, fill=X)
        frame6 = Frame(frame4)
        frame6.pack(side = LEFT, fill=X)
        frame7 = Frame(frame4)
        frame7.pack(side = LEFT, fill=X)
        frame8 = Frame(frame4)
        frame8.pack( side = LEFT, fill=X)

        UsernameText = self.user
        ULabel =  Label(frame2,text = UsernameText + " " + self.rank, font=('Ariel', 30), fg= "medium blue",
                        background ="white" ).grid(row=0, column=0, padx =10, pady=20)
        fillLabel = Label(frame2, text="", width =800).grid(row=0,column=1)

        img = self.getImage()
        profile = Label(frame5, image= img)
        profile.image = img
        profile.grid(row=0, column=0, pady=10)

        InterestLabel = Label(frame5, text= "Interests", font=('Ariel', 30), fg="medium blue", background="white").grid(
            row=1, column=0, pady=10)
        Interest1Label = Label(frame5, text= self.Interest1, font=('Ariel', 30), fg="medium blue", background="white")\
            .grid(row=2, column=0)
        Interest2Label = Label(frame5, text= self.Interest2, font=('Ariel', 30), fg="medium blue", background="white")\
            .grid(row=3, column=0)
        Interest3Label = Label(frame5, text= self.Interest3, font=('Ariel', 30), fg="medium blue", background="white").\
            grid(row=4, column=0)

        createdocLabel = Button(frame3,text = "create document",font=('Ariel', 30), fg= "medium blue", background ="white" ).grid(row=0, column=0, padx=10, pady=10)
        doc1Label = Button(frame3, text= "recent doc 1", font=('Ariel', 30), fg="medium blue", background="white", width=15).grid(row=0, column=1, padx=20)
        docLabel2 = Button(frame3, text= "doc 2", font=('Ariel', 30), fg="medium blue", background="white", width =15).grid(row=0, column=2, padx=10)
        docLabel3 = Button(frame3, text= " doc 3", font=('Ariel', 30), fg="medium blue", background="white", width =15).grid(row=0, column=3, padx=10)

        searchmember = Label(frame6,text = "    Search members",font=('Ariel', 30), fg= "medium blue", width=15 ).grid(sticky=E)
        Label(frame6, text="", width=5).grid(row=1, column=0)
        searchmEntry = Entry(frame6, width=50 ).grid(row=1,column=0, sticky=E, padx=10)
        simg = PhotoImage(file="images.gif")
        searchpic = Label(frame6, image= simg)
        searchpic.image = simg
        searchpic.grid(row=1, column=1)
        searchMresult = Listbox(frame6, width=50).grid(row=2,column=0, sticky=E,padx=10)

        searchdoc = Label(frame7, text="Search Documents", font=('Ariel', 28), fg="medium blue", width=15).grid(
            sticky=E)
        searchDEntry = Entry(frame7, width=50).grid(row=1, column=0, sticky=E, padx=10)
        simg = PhotoImage(file="images.gif")
        searchpicD = Label(frame7, image=simg)
        searchpicD.image = simg
        searchpicD.grid(row=1, column=1)
        searchDresult = Listbox(frame7, width=50).grid(row=2, column=0, sticky=E, padx=10)


        compltaboo = Label(frame8,text =  "taboo",font=('Ariel', 30), fg= "medium blue", background ="white" ).grid(row=0, column=0, sticky=E, padx = 50)
        tabooButton = Button(frame8, text= "Process Complaints", font=('Ariel', 24), fg="medium blue", background="white").grid(row=1, column=0, padx=10)


        frame1.pack()

    def getImage(self):
        img = PhotoImage(file="testgirl.gif")
        return img

    def main(self, username):
        root = Toplevel()
        UserPg(root, username)
        root.mainloop()