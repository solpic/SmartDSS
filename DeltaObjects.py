''' Houses INSERT and DELETE classes'''

class Insert():

    def __init__(self,loc,s, u_id=-1):
        self.location = loc
        self.string = s
        self.u_id = u_id
        
    def show(self):
        print("ID: "+str(self.u_id)+"Insert: "+self.string+", at "+str(self.location))


class Delete():

    def __init__(self,loc,l, u_id=-1):
        self.location = loc
        self.length = l
        self.u_id = u_id
        
    def show(self):
        print("ID: "+str(self.u_id)+"Delete: "+str(self.length)+", at "+str(self.location))
