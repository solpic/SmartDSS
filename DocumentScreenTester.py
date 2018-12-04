'''This is just a test file to test instatiating a DocumentScreen from another file'''

import DocumentFileTest
import Users1



class user:
    def __init__(self,name):
        self.name=name

    def getRank(self):
        return self.name
    def getUserName(self):
        return self.name
class Document:
    def __init__(self,name,sList):
        self.name=name
        self.sentances = sList 

    def getNumberOfSentances(self):
        return len(self.sentances)

    def getMembers(self):
        return [guestUser,ordUser,superUser]

tmpSList = ["SentanceOne","SentanceTwo","SentanceThree","SentanceFour","SentanceArif"]
guestUser = user("GU")
ordUser = user("OU")
superUser = user("SU")
testDoc = Document("Captains Log", tmpSList)
testScreen1 = DocumentFileTest.DocumentScreen(guestUser,testDoc)
# testScreen2 = DocumentFileTest.DocumentScreen(ordUser,tmpSList)
# testScreen3 = DocumentFileTest.DocumentScreen(superUser)
