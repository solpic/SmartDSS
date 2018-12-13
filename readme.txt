Rought Break Down of Each File

----- Complaint.py----
Class for the Complaints in the system

----- DeltaObjects.py ----
File containing the Insert and Delete classes, sequences of these two classes are how we track changes between documents

------DocumentDB ----

# DocumentDBServer runs on the server and handles DB stuff
# DocumentDBClient is called by the client for all getters/setters
# Helper functions to wrap documentdbserver for RPC

----- DocumentFileTest.pu ----
GUI for the Document Editor

----- DocumentModel.py ---
All of the data for a document. Stores its meta data and attributes which are obtained from the server

---- HomePg.py -----
*ENTERY POINT FOR THE SYSTEM*
GUI for starting up the System, depends based on rank

----- ProcessMember.py ------
GUI for processing a memmber,

---- ProcessTabooWords.py ---
GUI For the SU to process suggested words

-----Login2.py----
GUI for Login, also does some verification on user name

---- RPC CLIENT ----
Runs on the client machine to connect to the server

----- RPC SERVER ----
Runs on the AWS server

----SignUp.py---
Prompts user to input sign in info and sends it to the DB

---TabooWords.py--
Contains the class for how we store  TabooWords throughout the system as well as staticmethods for system wide changes

----UserPg.py---
GUI for userpage, allowing the user to do searches and open documents

----creatFilePopUp.py---
Dialog for making a new doc

---inputPopUp.py----
NOT USED IN FINAL PRODUCT

