# Handles document updates, deletions and insertions
class Update():
    def __init__(self, position, length, contents, count=-1):
        self.position = position
        self.length = length
        self.contents = contents
        self.count = count
    
