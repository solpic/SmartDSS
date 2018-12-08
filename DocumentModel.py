import datetime

#TODO: Add Server Update code as well

class DocumentModel():

    def __init__(self,user,documentName,privLevel):
        self.owner = user
        self.versionNumber = self.genVersionNumber
        self.docName = documentName
        self.privacyLevel = privLevel
        self.createDate = datetime.datetime.now()
        self.versionDate = self.createDate
        self.words=""
        self.memberList = []
        self.locked = False
        self.deltaLog = []
        self.complaints = []
        
    def lockDocument(self):
        self.locked=True
    def unlockDocument(self):
        self.locked=False

    def addMember(self, member):
        self.memberList.append(member)
    def removeMember(self,member):
        targetUName = member.getUserName()
        for i in range(0,len(self.memberList)):
            if (self.memberList[i].getUserName()==targetUName):
                del member[i]
    
    def addComplaint(self, complaint):
        self.complaints.append(complaint)