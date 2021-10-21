

class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []

#   Makes the first square clicked empty and adds the move to the move log
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
    
#   Removes the last move from the move log and undos the move from the board 
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn =="w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == "P":
                        self.getPawnMoves(r,c, moves)
                    elif piece == "R":
                        self.getRookMoves(r,c, moves)
        return moves


    def getPawnMoves(self, r, c, moves):
#   White pawn moves
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c),self.board))
#   Pawn capture to the left
            if c -1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c),(r-1,c-1),self.board))
#   Pawn capture to the right
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        else:
#   Black pawn moves
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c),self.board))
#   Pawn capture to the left
            if c -1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
#   Pawn capture to the right
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))



    def getRookMoves(self, r, c, moves):
        pass



class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

#   Creates the object of a move
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

#   Checks to see if one move is the same as another
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


#   Creates the chess notation of the move
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

#   Getter for rank and file
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
