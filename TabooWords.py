

class TabooWords:

    allTaboo = []
    def __init__(self,t):
        self.text = t
        
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