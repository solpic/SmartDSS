'''This is just a test file to test instatiating a DocumentScreen from another file'''

import DocumentFileTest
import Users1
import DocumentModel


class user:
    def __init__(self,name):
        self.name=name

    def getRank(self):
        return self.name
    def getUserName(self):
        return self.name


tmpSList = ["SentanceOne","SentanceTwo","SentanceThree","SentanceFour","SentanceArif"]
guestUser = user("GU")
ordUser = user("OU")
superUser = user("SU")
testDoc = DocumentModel.DocumentModel(guestUser, "MY DOCUMENT NAME","PRIVATE")
testScreen1 = DocumentFileTest.DocumentScreen(guestUser,testDoc)
# testScreen2 = DocumentFileTest.DocumentScreen(ordUser,tmpSList)
# testScreen3 = DocumentFileTest.DocumentScreen(superUser)
