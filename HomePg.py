from tkinter import*
# PIL import ImageTk, Image
import Login2
import SignUp
import sqlite3

class HomePg():
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Home")
        self._geom = '800x800+0+0'
        parent.geometry("{0}x{1}+0+0".format(
            parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.createWidget()

    def createWidget(self):
        frame1 = Frame(self.parent)
        frame2 = LabelFrame(frame1)
        frame2.grid(row=0, column=0, sticky=W)
        frame3 = Frame(frame1)
        frame3.grid(row=1, column=0, sticky=W)

        img = PhotoImage(file = "SmartD.gif")
        l = Label(frame3, image=img)
        l.image = img
        l.grid(sticky=W)

        Label(frame2, text="", height =0, width=100).grid(row=0, column=1)
        Label(frame2, text= "SmartDSS", font=('Comic Sans MS', 48), fg = "dodgerblue").grid(row=0,column=0)
        Button(frame2, text="Log in", font=('Comic Sans MS', 25), command = self.login, height=1, width=10).grid(row=0, column=2, sticky=E, padx=10)
        Button(frame2, text="Get Started",font=('Comic Sans MS', 25), command = self.signup, height=1, width=10).grid(row=0, column=3, sticky=E, padx=10)

        frame1.pack()


    def login(self):
        Login2.Login.main(self)

    def signup(self):
        SignUp.SignUp.main(self)


if __name__== "__main__":
    root = Tk()
    HomePg(root)
    root.mainloop()