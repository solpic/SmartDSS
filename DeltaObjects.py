''' Houses INSERT and DELETE classes'''

class Insert():

    def __init__(self,loc,s):
        self.location = loc
        self.string = s
        
    def show(self):
        print("Insert: "+self.string+", at "+str(self.location))


class Delete():

    def __init__(self,loc,l):
        self.location = loc
        self.length = l
        
    def show(self):
        print("Delete: "+str(self.length)+", at "+str(self.location))
