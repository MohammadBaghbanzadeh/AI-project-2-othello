class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, board, result, depth):
        key = hash(str(board))
        self.table[key] = (result, depth)

    def retrieve(self, board, depth):
        key = hash(str(board))
        if key in self.table:
            stored_result, stored_depth = self.table[key]
            if stored_depth >= depth:
                return stored_result
