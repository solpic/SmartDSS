import datetime

#TODO: Add Server Update code as well

class DocumentModel():
        
    def __init__(self,user=None,documentName=None,privLevel=None):
        self.owner = user
        self.versionNumber = self.genVersionNumber
        self.docName = documentName
        self.privacyLevel = privLevel
        self.createDate = datetime.datetime.now()
        self.versionDate = self.createDate
        self.words=""
        self.memberList = [] #LIST OF ALL MEMBERS RELATED TO DOCUMENT
        self.locked = False
        self.deltaLog = []
        self.complaints = []
        
    # TODO: How does this work?/ What does it do?
    def genVersionNumber(self):
        return 5
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

    def getMembers(self):
        return self.memberList
    def getAllMembers(self):
        #TODO:
        return # a list of all registered members in DB, should be a Server Querey
    def getWords(self):
        return self.words
    # TODO: Update Local Changes with DB Tables

    def getComplaints(self):
        return self.complaints
    def synchronize(self):
        print()
