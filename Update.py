# Handles document updates, deletions and insertions
class Update():
    def __init__(self, doc_id, position, length, contents, count_id=-1):
        self.position = position
        self.length = length
        self.contents = contents
        self.count_id = count_id
        self.doc_id = doc_id
    
