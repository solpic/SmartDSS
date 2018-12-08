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
        self.createWidget()

    def createWidget(self):
        frame1 = Frame(self.parent)
        frame1.configure(background = "white")
        UsernameText = self.user
        ULabel =  Label(frame1,text = UsernameText,font=('Ariel', 30), fg= "medium blue", background ="white" ).grid(row=0, column=0)

        frame1.pack()


    def main(self, username):
        root = Tk()
        UserPg(root, username)
        root.mainloop()