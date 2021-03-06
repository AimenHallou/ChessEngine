import pygame as p
import ChessEngine


#   Width and height of the screen
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
#   Frames the game runs in 
MAX_FPS = 15
IMAGES = {}

#   Takes all chess piece images and adds them to the array
def loadImages():
    pieces = ["wP","wR","wN","wB","wK","wQ","bP","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMade = gs.getValidMoves()
    moveMade = False

    validMoves = gs.getValidMoves()
    loadImages()
    running = True
    sqSeleted = ()
    playerClicks = []

#   Loop that runs until the game is closed
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
#   Checks if the user has clicked on a square 
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
#   Checks if the same square has been selected twice
                if sqSeleted == (row, col):
                    sqSeleted = ()
                    playerClicks = []
                else:
                    sqSeleted = (row, col)
                    playerClicks.append(sqSeleted)
#   If a second click is registered, makes a move to the board 
                if len(playerClicks) == 2:                    
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True                    
                    sqSeleted = ()
                    playerClicks = [] 

#   Key presses
#   User can press the z key to undo the previous move
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

#   Drawing the game board and the individual pieces
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

#   Draw the squares where the pieces may lie 
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range (DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

#   Draw the pieces in top of the board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


if __name__ == "__main__":
    main()