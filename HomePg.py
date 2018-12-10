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
        frame2.configure(background = "")
        frame2.grid(row=0, column=0, sticky=W)
        frame3 = Frame(frame1)
        frame3.grid(row=1, column=0, sticky=W, padx=120)

        img = PhotoImage(file = "SmartD.gif")
        logo = Label(frame3, image=img)
        logo.image = img
        logo.grid(sticky=W)

        Label(frame2, text="", height =0, width=100).grid(row=0, column=1)
        Label(frame2, text= "SmartDSS", font=('Arial', 48), fg = "medium blue").grid(row=0,column=0)
        Button(frame2, text="Log in", font=('Ariel', 30), fg= "medium blue", borderwidth = 0,  command = self.login, height=1, width=10).grid(row=0, column=2, sticky=E, padx=10)
        Button(frame2, text="Get Started",font=('Arial', 30), fg= "medium blue", borderwidth = 0, command = self.signup, height=1, width=10).grid(row=0, column=3, sticky=E, padx=10)
        frame1.pack()


    def login(self):
        Login2.Login.main(self)

    def signup(self):
        SignUp.SignUp.main(self)


if __name__== "__main__":
    root = Tk()
    HomePg(root)
    root.mainloop()