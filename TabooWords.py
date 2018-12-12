

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
        # TODO: DallTaboo isnt an attribute
        print("# TODO: THIS DOESNT WORK")

    @staticmethod
    def getAllTaboo():
        from DocumentDB import doc_cli
        return doc_cli.get_taboo_words()
        
    def show(self):
        print("Word: "+self.text+", Status: "+str(self.status))
