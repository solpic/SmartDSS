

class TabooWord:

# status 0 is proposed, 1 is accepted
    allTaboo = []
    def __init__(self,t, status=0):
        self.text = t
        self.status = status
        
    def getTaboo(self):
        return self.text

    @staticmethod
    def addTabooWord(word):
        global allTaboo
        allTaboo.append(word)
        # TODO: Database call to add word
        print("# TODO: Database call to add word")

    @staticmethod
    def getAllTaboo():
        #TODO: Database Call to get all words
        return ["This", "should", "have all the words from the servrer"]
        
    def show(self):
        print("Word: "+self.text+", Status: "+str(self.status))
