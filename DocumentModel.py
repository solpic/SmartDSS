import datetime
import Complaint
import DeltaObjects
from DocumentDB import doc_cli

#TODO: Add Server Update code as well
# Getters are Client Side
# Setters are Both CLient and Server (Only do Client if Server passed)
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
        self.doc_id=1
        
    def show(self):
        print("Name:"+self.docName)
        print("Locked: "+str(self.locked))
        print("Contents: "+self.contents)
        print("ID: "+str(self.doc_id))
        
    def genVersionNumber(self):
    # TODO: How does this work?/ What does it do?
        return 5
    def lockDocument(self):
        from DocumentDB import doc_cli
        if doc_cli.set_document_lock(self.docName,self.owner,self.versionNumber,self.locked):
            self.locked=1
        
    def unlockDocument(self):
        from DocumentDB import doc_cli
        if doc_cli.set_document_lock(self.docName,self.owner,self.versionNumber,self.locked):
            self.locked=0

    def addMember(self, member):
        from DocumentDB import doc_cli
        if doc_cli.add_member(self.doc_id,member):
            self.memberList.append(member)

    def removeMember(self,member):
        from DocumentDB import doc_cli
        targetUName = member
        if doc_cli.remove_member(self.doc_id,member):
            for i in range(0,len(self.memberList)):
                if (self.memberList[i].getUserName()==targetUName):
                    del member[i]
    
    def addComplaint(self, complaint,currUser):
        complaintObj = Complaint.Complaint(complaint,currUser)
        self.complaints.append(complaintObj)
        # TODO: Server Call to also add complaint to Document Table.

    def getMembers(self):
        return self.memberList
    def getAllMembers(self):
        return self.memberList 
    def getWords(self):
        return self.words
    
    def getComplaints(self):
        return self.complaints

    def generateDeltas(self,old,new):
        print("Old: "+old)
        #old is the old document words
        #new is the current docment words
        tmpDeltaLog = []
        oldLength = len(old)
        newLength = len(new)
        terminate = 0
        if(oldLength<newLength):
            terminate = oldLength
        else:
            terminate = newLength
            #Also takes care of if oldLength == newLength
        
        diffString="" #Difference in string so far
        diffTable=[""] # Table of Diff Strings 
        dTableIndex = 0 
        stillChanging = True
        travelLength = 0
        for i in range(0,terminate):
            #print(diffTable[dTableIndex])
            if(old[i]!=new[i]): # Constructs diffString
                diffTable[dTableIndex] = diffTable[dTableIndex] + new[i]
                travelLength = travelLength+ 1
                stillChanging = True
            else:
                stillChanging = False
            
            if(i==terminate-1):#At the end you want to grab all changes
                stillChanging = False

            if stillChanging == False:
                #location = (i-len(diffTable[dTableIndex]))
                location = (i-travelLength +1)#i is indicies so its offset from length
                tmpDeltaLog.append(DeltaObjects.Delete(location,len(diffTable[dTableIndex])))
                tmpDeltaLog.append(DeltaObjects.Insert(location,diffTable[dTableIndex]))
                dTableIndex = dTableIndex+1
                diffTable.append("")
                travelLength=0

        # i>term behavior
        if(oldLength!=newLength):
            if(newLength>oldLength):
                tmpDeltaLog.append(DeltaObjects.Insert(terminate,new[terminate:]))
            if(newLength<oldLength):
                tmpDeltaLog.append(DeltaObjects.Delete(terminate,oldLength-terminate))
        cleanDeltaLog = [] # Should contain only the meaningful Delta Functions
        # clean out initial false deltas
        # insert's string is "" or delete's length is 0
        for delta in tmpDeltaLog:
            if(isinstance(delta,DeltaObjects.Delete)):
                if(delta.length!=0):
                    cleanDeltaLog.append(delta)
            if(isinstance(delta,DeltaObjects.Insert)):
                if(delta.string!=""):
                    cleanDeltaLog.append(delta)


        #deltaLog = cleanDeltaLog
        self.deltaLog.extend(cleanDeltaLog)
        
        return cleanDeltaLog
    
    def reconstruct(self,num,deltaLog):
        #print("Begin reconstruct")
        tmp = 0
        tmpStringOld = self.words
        self.words="" #NOTE:This reset might be causing issues. It basically makes reconstruct from null
        for delta in deltaLog:
            tmpString = self.words
            # Insert
            #print("Applying delta: ")
            #delta.show()
            #print("Initial: ")
            #print(self.words)
            if (isinstance(delta,DeltaObjects.Insert)):
                # string from 0 position + Insert Contents + rest of string
                backHalf = tmpString[0:delta.location]
                frontHalf = tmpString[delta.location:]
                self.words = backHalf + delta.string + frontHalf
            if(isinstance(delta,DeltaObjects.Delete)):
                backHalf = tmpString[0:delta.location]
                frontHalf = tmpString[(delta.location+delta.length):]
                self.words = backHalf+frontHalf
            tmp= tmp+1
            #print("Final: ")
            #print(self.words)
            #delta.show()
        #print("OLD: {} NEW: {}".format(tmpStringOld,self.words))
        #print("\n\n")

                


