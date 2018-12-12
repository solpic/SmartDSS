<<<<<<< HEAD
from tkinter import*
from DocumentDB import doc_cli

class ProcessComplaints():
    def __init__(self):
        root = self.root = Toplevel()
        root.title('Process Complaints')
        root.geometry('450x330')
        self.complaintsSearch = []
        self.compvar = StringVar(value=self.complaintsSearch)
        self.userName = StringVar()
        self.doc_id = IntVar()
        self.createWidgets()

    def createWidgets(self):
        frame1 = Frame(self.root)
        frame2 = Frame(frame1)
        frame2.grid(row=3,column=0)
        frame3 = Frame(frame1)
        frame3.grid(row=4, column=0)

        self.complaintlist = Listbox(frame1, listvariable=self.compvar, width=70)
        self.complaintlist.grid(row=1, column=0, padx=5, pady=5)
        for entry in self.complaintsSearch:
            print("entry", entry)
            self.complaintlist.insert(entry)
        Button(frame2, text="View", font=('Ariel', 14), fg="medium blue", command=self.getComplaints).grid(row=0, column=0,padx=5, pady=5)
        Button(frame2, text="Delete", font=('Ariel', 14), fg="medium blue", command =self.deleteComplaint).grid(row=0, column=2, padx=5, pady=5)
        Button(frame2, text="Exit", font=('Ariel', 14), fg="medium blue", command = self.quit).grid(row=0, column=3, padx=5,  pady=5)

        Label(frame3, text = "Username",font=('Ariel', 12), fg="medium blue" ).grid(row=0,column=0)
        Entry(frame3, textvariable=self.userName).grid(row=0, column=1)
        Label(frame3, text="Document ID", font=('Ariel', 12), fg="medium blue").grid(row=1, column=0)
        Entry(frame3, textvariable=self.doc_id).grid(row=1, column=1)
        Button(frame3, text="Remove Member", font=('Ariel', 14), fg="medium blue", command=self.removeMember).grid(row=0, column=2,
                                                                                                       padx=2, pady=5)
        frame1.pack()

    def getComplaints(self):
        self.complaintsSearch = doc_cli.get_complaints()
        for entry in self.complaintsSearch:
            print("PM entry", entry)
        self.compvar.set(self.complaintsSearchSearch)

    def deleteComplaint(self):
        item = self.curselection()
        idx = item[0]
        complaint = self.complaintsSearch[idx]
        DeleteComplaint = complaint[0]
        doc_cli.delete_complaint(DeleteComplaint)
        self.complaintsSearch = doc_cli.get_complaints()
        self.compvar.set(self.complaintsSearch)

    def removeMember(self):
        username = self.userName.get()
        doc_id = self.doc_id.get()
        doc_cli.remove_member(doc_id, username)

    def quit(self):
        self.root.destroy()

    def main(self):
        Complaintsgui = ProcessComplaints()
        Complaintsgui.root.mainloop()
=======
from tkinter import*
from DocumentDB import doc_cli

class ProcessComplaints():
    def __init__(self):
        root = self.root = Toplevel()
        root.title('Process Complaints')
        root.geometry('450x330')
        self.complaintsSearch = []
        self.compvar = StringVar(value=self.complaintsSearch)
        self.userName = StringVar()
        self.doc_id = IntVar()
        self.createWidgets()

    def createWidgets(self):
        frame1 = Frame(self.root)
        frame2 = Frame(frame1)
        frame2.grid(row=3,column=0)
        frame3 = Frame(frame1)
        frame3.grid(row=4, column=0)

        self.complaintlist = Listbox(frame1, listvariable=self.compvar, width=70)
        self.complaintlist.grid(row=1, column=0, padx=5, pady=5)
        for entry in self.complaintsSearch:
            print("entry", entry)
            self.complaintlist.insert(entry)
        Button(frame2, text="View", font=('Ariel', 14), fg="medium blue", command=self.getComplaints).grid(row=0, column=0,padx=5, pady=5)
        Button(frame2, text="Delete", font=('Ariel', 14), fg="medium blue", command =self.deleteComplaint).grid(row=0, column=2, padx=5, pady=5)
        Button(frame2, text="Exit", font=('Ariel', 14), fg="medium blue", command = self.quit).grid(row=0, column=3, padx=5,  pady=5)

        Label(frame3, text = "Username",font=('Ariel', 12), fg="medium blue" ).grid(row=0,column=0)
        Entry(frame3, textvariable=self.userName).grid(row=0, column=1)
        Label(frame3, text="Document ID", font=('Ariel', 12), fg="medium blue").grid(row=1, column=0)
        Entry(frame3, textvariable=self.doc_id).grid(row=1, column=1)
        Button(frame3, text="Remove Member", font=('Ariel', 14), fg="medium blue", command=self.removeMember).grid(row=0, column=2,
                                                                                                       padx=2, pady=5)
        frame1.pack()

    def getComplaints(self):
        self.complaintsSearch = doc_cli.get_complaints()
        for entry in self.complaintsSearch:
            print("PM entry", entry)
        self.compvar.set(self.complaintsSearchSearch)

    def deleteComplaint(self):
        item = self.curselection()
        idx = item[0]
        complaint = self.complaintsSearch[idx]
        DeleteComplaint = complaint[0]
        doc_cli.delete_complaint(DeleteComplaint)
        self.complaintsSearch = doc_cli.get_complaints()
        self.compvar.set(self.complaintsSearch)

    def removeMember(self):
        username = self.userName.get()
        doc_id = self.doc_id.get()
        doc_cli.remove_member(doc_id, username)

    def quit(self):
        self.root.destroy()

    def main(self):
        Complaintsgui = ProcessComplaints()
        Complaintsgui.root.mainloop()
>>>>>>> 77381e00f198bda64e30e5f3e5e6474ef54e3b41
