

class Complaint():
    def __init__(self,t,u):
        self.user=u
        self.text = t
    
    def getComplaint(self):
        return self.text
    
    def getComplaintCreator(self):
        return self.user
        
    def show(self):
        print("COMPLAINT: "+self.text+", From: "+self.user)
