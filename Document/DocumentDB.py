import sqlite3

class DocumentDB():
	def __init__(self):
		self.conn = sqlite3.connect('../documents.db')
		self.c = self.conn.cursor()
		
	def create_tables(self, del_old=True):
		if del_old:
			self.c.execute('DROP TABLE IF EXISTS documents')
			self.c.execute('DROP TABLE IF EXISTS doc_changes')
		
		self.c.execute('''CREATE TABLE documents
						(name TEXT, contents TEXT)''')
						
		self.c.execute('''CREATE TABLE doc_changes
						(doc_id INTEGER, position INTEGER, is_deletion INTEGER, contents TEXT, id INTEGER)''')
						
		self.conn.commit()
		
	def create_document(self, name, contents):
		self.c.execute('''INSERT INTO documents VALUES (?, ?)''', (name, contents,))
		
		self.conn.commit()
		
	def get_document(self, name):
		self.c.execute("SELECT * FROM documents WHERE name=?", (name,))
		print(self.c.fetchone())
		
		
		
docs = DocumentDB()
docs.create_tables()
docs.create_document("Poopy", '''Poopy made poopy pants everyday''')
docs.get_document("Poopy")
